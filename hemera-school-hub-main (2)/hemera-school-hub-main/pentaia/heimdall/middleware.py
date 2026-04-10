from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from .audit import AuditLogger, SecurityEvent
from .config import HeimdallSettings
from .network import extract_client_ip
from .rate_limit import SlidingWindowRateLimiter
from .threats import ThreatDetector


class HeimdallMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, settings: HeimdallSettings):
        super().__init__(app)
        self.settings = settings
        self.detector = ThreatDetector.from_cidrs(settings.blocked_networks)
        self.limiter = SlidingWindowRateLimiter(
            requests=settings.rate_limit.requests,
            window_seconds=settings.rate_limit.window_seconds,
        )
        self.audit = AuditLogger(settings.sensitive_fields)

    async def dispatch(self, request: Request, call_next):
        client_ip = extract_client_ip(
            headers={k.lower(): v for k, v in request.headers.items()},
            remote_addr=request.client.host if request.client else "0.0.0.0",
            trusted_proxies=self.settings.trusted_proxies,
        )

        verdict = self.detector.evaluate_ip(client_ip)
        if not verdict.allowed:
            self.audit.log(
                SecurityEvent(
                    event_type="blocked_request",
                    actor_id=None,
                    source_ip=client_ip,
                    outcome="blocked",
                    details={"path": request.url.path, "reason": verdict.reason},
                )
            )
            return JSONResponse({"detail": verdict.reason}, status_code=403)

        limit_key = f"{client_ip}:{request.url.path}"
        limit_result = self.limiter.check(limit_key)
        if not limit_result.allowed:
            return JSONResponse(
                {
                    "detail": "Muitas requisições",
                    "reset_seconds": limit_result.reset_seconds,
                },
                status_code=429,
            )

        response = await call_next(request)
        response.headers["X-RateLimit-Remaining"] = str(limit_result.remaining)
        return response
