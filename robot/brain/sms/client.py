from __future__ import annotations

import base64
import os
import urllib.error
import urllib.parse
import urllib.request

from ..config import RobotConfig


class SmsClient:
    """Outbound SMS via Twilio REST API (stdlib only)."""

    def __init__(self, config: RobotConfig) -> None:
        self.config = config
        self._sid = os.environ.get("TWILIO_ACCOUNT_SID", config.sms_account_sid)
        self._token = os.environ.get("TWILIO_AUTH_TOKEN", config.sms_auth_token)
        self._from = os.environ.get("TWILIO_FROM_NUMBER", config.sms_from_number)
        self._to = os.environ.get("SCOUT_SMS_TO_NUMBER", config.sms_to_number)

    @property
    def ready(self) -> bool:
        return bool(
            self.config.sms_enabled
            and self._sid
            and self._token
            and self._from
            and self._to
        )

    def send(self, body: str) -> bool:
        if not self.ready:
            print("   [sms] not configured — set sms in config + Twilio env vars")
            return False
        body = body.strip()
        if not body:
            return False
        if len(body) > 1500:
            body = body[:1497] + "..."

        url = f"https://api.twilio.com/2010-04-01/Accounts/{self._sid}/Messages.json"
        data = urllib.parse.urlencode({
            "To": self._to,
            "From": self._from,
            "Body": body,
        }).encode()
        auth = base64.b64encode(f"{self._sid}:{self._token}".encode()).decode()
        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header("Authorization", f"Basic {auth}")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")

        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return 200 <= resp.status < 300
        except urllib.error.HTTPError as exc:
            print(f"   [sms] send failed: {exc.code} {exc.read().decode()[:200]}")
            return False
        except OSError as exc:
            print(f"   [sms] send error: {exc}")
            return False

    def is_allowed_sender(self, phone: str) -> bool:
        allowed = self.config.sms_allowed_numbers or [self._to]
        normalized = _normalize_phone(phone)
        return any(_normalize_phone(n) == normalized for n in allowed if n)


def _normalize_phone(value: str) -> str:
    return "".join(c for c in value if c.isdigit() or c == "+")
