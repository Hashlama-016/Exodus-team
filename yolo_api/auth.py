from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
from conf import get_conf
header_scheme = APIKeyHeader(name="x-key")


async def handle_api_key(key: str = Security(header_scheme)):
    if key != get_conf()["api_key"]:
        raise HTTPException(status_code=403, detail="Forbidden")
