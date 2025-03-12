from __future__ import annotations

from dice_lib.host import HOST_INFO_PROPERTIES, execute_local_commands
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/host",
    tags=["host"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{property_name}")
async def host_info(property_name: str) -> JSONResponse:
    if property_name == "all":
        properties = execute_local_commands(
            commands=HOST_INFO_PROPERTIES,
        )
        return JSONResponse(properties)
    if property_name not in HOST_INFO_PROPERTIES:
        return JSONResponse(
            status_code=404,
            content={"message": f"Property {property_name} not found"},
        )
    property = execute_local_commands(
        commands={property_name: HOST_INFO_PROPERTIES[property_name]},
    )
    return JSONResponse(property)
