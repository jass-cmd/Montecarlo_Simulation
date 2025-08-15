# app/schemas/run.py
from __future__ import annotations
from datetime import date
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator


# ===========================
# Domain DTOs
# ===========================
class RiskDTO(BaseModel):
    """Riesgo que afecta al throughput (impacto 0..1 = multiplicador de capacidad)."""
    name: str = Field(..., min_length=1)
    probability: float = Field(..., ge=0.0, le=1.0)
    impact: float = Field(..., ge=0.0, le=1.0)  # 0.8 => -20% capacidad

    @field_validator("name", mode="before")
    @classmethod
    def _strip_name(cls, v: str) -> str:
        v = (v or "").strip()
        if not v:
            raise ValueError("El nombre no puede estar vacío.")
        return v


class ParamsDTO(BaseModel):
    """Parámetros de la distribución triangular de throughput."""
    t_min: float = Field(..., gt=0)
    t_mode: float = Field(..., gt=0)
    t_max: float = Field(..., gt=0)

    @model_validator(mode="after")
    def _check_triangular_order(self) -> "ParamsDTO":
        if not (self.t_min <= self.t_mode <= self.t_max):
            raise ValueError("Triangular inválida: se requiere t_min <= t_mode <= t_max.")
        return self


# ===========================
# Visualization toggles
# ===========================
class VisualizerOptionsDTO(BaseModel):
    """
    Regla: en /run por defecto SOLO histograma.
    El resto se pide con /visualize.
    """
    histogram: bool = True
    cdf: bool = False
    boxplot: bool = False
    convergence: bool = False  # detalles internos en el Visualizer


# ===========================
# Requests
# ===========================
class RunRequest(BaseModel):
    """
    Ejecuta la simulación (modo throughput) y devuelve results + SOLO histograma por defecto.
    """
    iterations: int = Field(5000, ge=1000, description="Número de iteraciones (>= 1000).")
    seed: int | None = Field(None, description="Semilla RNG opcional.")
    params: ParamsDTO
    risks: list[RiskDTO] = Field(default_factory=list)
    backlog: float = Field(..., gt=0, description="Trabajo total a procesar (input del usuario).")

    # Opcionales para que el HISTOGRAMA anote fechas:
    delivery_start_date: date | None = None
    time_unit: Literal["days", "weeks"] = "weeks"
    annotate_percentiles: list[int] | None = Field(
        default=None, description="Percentiles a anotar (ej. [50, 80]). Valores válidos: 1..99."
    )
    date_format: str = Field("%Y-%m-%d", description="Formato de fecha para etiquetas.")

    visual_options: VisualizerOptionsDTO | None = None

    @field_validator("annotate_percentiles")
    @classmethod
    def _validate_percentiles(cls, v: list[int] | None) -> list[int] | None:
        if v is None:
            return v
        bad = [p for p in v if not (1 <= p <= 99)]
        if bad:
            raise ValueError(f"Percentiles fuera de rango (1..99): {bad}")
        # ordena y quita duplicados para estabilidad de UI
        return sorted(set(v))


class OnDemandVisualizerOptionsDTO(BaseModel):
    """
    Genera gráficos adicionales SIN re-simular (usa 'results' de /run).
    Por defecto todo en False para obligar a elegir explícitamente.
    """
    histogram: bool = False
    cdf: bool = False
    boxplot: bool = False
    convergence: bool = False  # detalles internos en el Visualizer


class VisualizeRequest(BaseModel):
    results: list[float] = Field(..., description="Resultados previos de /run (duraciones > 0).")
    options: OnDemandVisualizerOptionsDTO

    # Si querés re-generar histograma con fechas/percentiles distintos:
    delivery_start_date: date | None = None
    time_unit: Literal["days", "weeks"] = "weeks"
    annotate_percentiles: list[int] | None = None
    date_format: str = "%Y-%m-%d"

    @field_validator("results")
    @classmethod
    def _results_must_be_positive(cls, v: list[float]) -> list[float]:
        if not v:
            raise ValueError("Se requiere al menos un resultado para visualizar.")
        if any(x <= 0 for x in v):
            raise ValueError("Todos los resultados deben ser > 0.")
        return v

    @field_validator("annotate_percentiles")
    @classmethod
    def _validate_percentiles(cls, v: list[int] | None) -> list[int] | None:
        if v is None:
            return v
        bad = [p for p in v if not (1 <= p <= 99)]
        if bad:
            raise ValueError(f"Percentiles fuera de rango (1..99): {bad}")
        return sorted(set(v))


# ===========================
# Responses
# ===========================
class ImageDTO(BaseModel):
    kind: Literal["histogram", "cdf", "boxplot", "convergence"]
    image_base64: str


class RunResponse(BaseModel):
    results: list[float] = Field(..., description="Duración por iteración.")
    images: list[ImageDTO] = Field(default_factory=list, description="Por defecto: solo histograma.")

    # ejemplo en OpenAPI
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "results": [12.0, 10.0, 13.0, 11.0, 12.0],
            "images": [{"kind": "histogram", "image_base64": "<BASE64...>"}]
        }
    })


class VisualizeResponse(BaseModel):
    images: list[ImageDTO]


# ===========================
# Error contract (uniforme)
# ===========================
class ErrorResponse(BaseModel):
    error: Literal["validation_error", "bad_request", "server_error"]
    message: str
    fields: dict[str, str] | None = None  # campo -> mensaje
