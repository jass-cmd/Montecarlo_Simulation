# app/schemas/run.py
from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator


# ===========================
# Domain DTOs (usuario)
# ===========================
class RiskDTO(BaseModel):
    """Riesgo que afecta al throughput (impacto 0..1 = multiplicador de capacidad)."""
    name: str = Field(..., min_length=1)
    probability: float = Field(..., ge=0.0, le=1.0)
    impact: float = Field(..., ge=0.0, le=1.0)  # 0.8 => -20% capacidad

    @field_validator("name", mode="before")
    @classmethod
    def _strip_name(cls, value: str) -> str:
        value = (value or "").strip()
        if not value:
            raise ValueError("El nombre no puede estar vacío.")
        return value

class ParamsDTO(BaseModel):
    """Parámetros de la distribución triangular de throughput + nº de iteraciones."""
    t_min: float = Field(..., gt=0)
    t_mode: float = Field(..., gt=0)
    t_max: float = Field(..., gt=0)
    iterations: int = Field(5000, ge=1000, description="Número de iteraciones (>= 1000).")

    @model_validator(mode="after")
    def _check_triangular_order(self) -> "ParamsDTO":
        if not (self.t_min <= self.t_mode <= self.t_max):
            raise ValueError("Triangular inválida: se requiere t_min <= t_mode <= t_max.")
        return self


# ===========================
# Requests (público)
# ===========================
class RunRequest(BaseModel):
    """
    Ejecuta la simulación (modo throughput).
    - SOLO recibe lo que manda el usuario hoy: params y risks.
    - Iterations, backlog, seed, anotaciones, etc. quedan como config interna del servidor.
    """
    params: ParamsDTO
    risks: list[RiskDTO] = Field(default_factory=list)


# Si vas a permitir gráficos extra bajo demanda vía botón del frontend:
class OnDemandVisualizerOptionsDTO(BaseModel):
    """Qué gráficos generar a partir de 'results' ya calculados (sin re-simular)."""
    histogram: bool = False
    cdf: bool = False
    boxplot: bool = False
    convergence: bool = False  # detalles internos en el Visualizer


class VisualizeRequest(BaseModel):
    """
    Genera gráficos adicionales usando los 'results' devueltos por /run.
    (Si preferís no exponer 'results', cambia esto por un simulation_id.)
    """
    results: list[float] = Field(..., description="Resultados previos de /run (duraciones > 0).")
    options: OnDemandVisualizerOptionsDTO

    @field_validator("results")
    @classmethod
    def _results_must_be_positive(cls, values: list[float]) -> list[float]:
        if not values:
            raise ValueError("Se requiere al menos un resultado para visualizar.")
        if any(x <= 0 for x in values):
            raise ValueError("Todos los resultados deben ser > 0.")
        return values


# ===========================
# Responses (público)
# ===========================
class ImageDTO(BaseModel):
    kind: Literal["histogram", "cdf", "boxplot", "convergence"]
    image_base64: str


class RunResponse(BaseModel):
    # Puedes seguir devolviendo 'results' + histograma por defecto
    results: list[float] = Field(..., description="Duración por iteración.")
    images: list[ImageDTO] = Field(default_factory=list, description="Por defecto: solo histograma.")

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
    fields: dict[str, str] | None = None
