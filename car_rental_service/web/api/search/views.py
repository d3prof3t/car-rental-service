from typing import List
from fastapi import APIRouter
from fastapi.param_functions import Depends

from car_rental_service.db.models.car import Car
from car_rental_service.db.dao.car_dao import CarDAO
from car_rental_service.web.api.search.schema import SearchOutputDTO

router = APIRouter()


@router.get("/", response_model=List[SearchOutputDTO])
async def search(
    start_date: str,
    end_date: str,
    car_id: int = None,
    car_dao: CarDAO = Depends(),
) -> List[Car]:
    return await car_dao.get_available_cars(start_date, end_date, car_id)
