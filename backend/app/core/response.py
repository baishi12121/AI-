"""统一响应结构"""
from typing import Any, Optional
from fastapi.responses import JSONResponse


def ok(data: Any = None, msg: str = "ok", request_id: Optional[str] = None) -> dict:
    return {"code": 0, "msg": msg, "data": data, "request_id": request_id}


def fail(code: int, msg: str, http_status: int = 400) -> JSONResponse:
    return JSONResponse(
        status_code=http_status,
        content={"code": code, "msg": msg, "data": None},
    )
