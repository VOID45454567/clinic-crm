from app.http.exceptions.domain import DomainException
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


async def domain_exception_handler(request: Request, exc: DomainException):
    content = exc.message if isinstance(exc.message, dict) else {"detail": exc.message}

    return JSONResponse(status_code=exc.status_code, content=content)


def setup_exception_handlers(app: FastAPI):
    app.add_exception_handler(DomainException, domain_exception_handler)
