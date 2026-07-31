from starlette.middleware.base import BaseHTTPMiddleware
from app.core.metrics import metrics


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        metrics["total_requests"] += 1

        try:
            response = await call_next(request)

            if response.status_code >= 400:
                metrics["total_errors"] += 1

            return response

        except Exception:
            metrics["total_errors"] += 1
            raise