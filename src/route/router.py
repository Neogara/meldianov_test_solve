from fastapi import APIRouter, Depends
from route.rates.rates import rates_router

api_router = APIRouter(
    responses={404: {"description": "Not found"}},
)

api_router.include_router(rates_router)



