import logging
from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.responses import Response


def setup_logging(app: FastAPI):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        filename="app.log"
    )
    logger = logging.getLogger("senama")

    @app.middleware("http")
    async def log_requests(request: Request, call_next) -> Response:
        start_time = datetime.now(timezone.utc)
        response = await call_next(request)
        duration = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000  # ms

        logger.info(
            f"Method={request.method} Path={request.url.path} "
            f"Status={response.status_code} Duration={duration:.2f}ms"
        )
        return response
