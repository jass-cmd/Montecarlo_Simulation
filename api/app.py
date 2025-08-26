
from typing import List
import numpy as np
from fastapi import FastAPI, HTTPException

#DTOs
from api.schemas import (ParamsDTO, RiskDTO,
    RunRequest, RunResponse, ErrorResponse, ImageDTO,
)

#domain clases
from src.classes.simulator import Simulator
from src.classes.simulation_visualizer import SimulationVisualizer
from src.classes.simulation_params import SimulationParameters
from src.classes.risk_class import Risk

app = FastAPI(title="Monte Carlo Simulation API", version="0.1.0")

#---------- test routes ----------
@app.get("/")
def root():
    return {"hello": "world"}

@app.get("/health")
def health():
    return {"status": "ok"}

#---------- mapping DTO -> domain ----------
def map_params(dto: ParamsDTO) -> SimulationParameters:
    return SimulationParameters(

        backlog=dto.backlog,
        th_min=dto.t_min,
        th_ex=dto.t_mode,   # <- antes tenías th_ex
        th_max=dto.t_max,
        num_sim=dto.iterations,
    )

def map_risks(dtos: list[RiskDTO]) -> list[Risk]:
    return [Risk(risk_name=r.name, probability=r.probability, impact=r.impact) for r in dtos]

@app.post(
    "/simulate",
    response_model=RunResponse,
    responses={400: {"model": ErrorResponse}, 422: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
def simulate(req: RunRequest) -> RunResponse:
    try:
        params_domain = map_params(req.params)
        risks_domain  = map_risks(req.risks)

        sim = Simulator(       
            parameters=params_domain,        
            risks=risks_domain,
        )

        results: np.ndarray = sim.run_simulation() 

        viz = SimulationVisualizer(results)
        hist_b64 = viz._plot_histogram() 
        cfd_b64  = viz.plot_cdf()
        convergence_b64 = viz.plot_convergence()

        return RunResponse(
        
            images=[
                ImageDTO(kind="histogram", image_base64=hist_b64),
                ImageDTO(kind="cdf", image_base64=cfd_b64),
                ImageDTO(kind="convergence", image_base64=convergence_b64)
            ]
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail={"error": "bad_request", "message": str(e), "fields": None})
    except Exception as e:
        import traceback; traceback.print_exc()  #helps with error tracking
        raise HTTPException(status_code=500, detail={"error": "server_error", "message": f"Unexpected error: {type(e).__name__}", "fields": None})
