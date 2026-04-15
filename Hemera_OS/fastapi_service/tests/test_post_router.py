import base64
from uuid import uuid4

import httpx
import pytest

from fastapi_service.main import app


def _headers(mode: str = "Cloud") -> dict[str, str]:
    return {
        "Authorization": "Bearer 1234567890abcdefTOKEN",
        "X-Post-Mode": mode,
        "X-ZIOS-Intelligent": "False",
    }


@pytest.mark.anyio
async def test_send_message_accepts_valid_base64_payload():
    payload = {
        "recipient_id": str(uuid4()),
        "content_type": "text/encrypted_blob",
        "payload": base64.b64encode(b"hello").decode(),
        "ephemeral_timer": 60,
    }

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post("/v1/message/send", json=payload, headers=_headers("Secret"))

    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "Secret"
    assert data["zios_intelligent"] is False
    assert data["expires_at"] is not None


@pytest.mark.anyio
async def test_send_message_rejects_invalid_base64_payload():
    payload = {
        "recipient_id": str(uuid4()),
        "content_type": "text/encrypted_blob",
        "payload": "@@@not-base64@@@",
        "ephemeral_timer": 0,
    }

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post("/v1/message/send", json=payload, headers=_headers("Cloud"))

    assert response.status_code == 422
    assert "Base64" in response.json()["detail"]


@pytest.mark.anyio
async def test_send_message_rejects_secret_without_encrypted_content_type():
    payload = {
        "recipient_id": str(uuid4()),
        "content_type": "text/plain",
        "payload": base64.b64encode(b"hello").decode(),
        "ephemeral_timer": 0,
    }

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post("/v1/message/send", json=payload, headers=_headers("Secret"))

    assert response.status_code == 422
    assert "content_type" in response.json()["detail"]
