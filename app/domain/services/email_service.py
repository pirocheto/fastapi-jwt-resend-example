from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.config import settings
from app.infrastructure.email import mailer
from app.infrastructure.email.template_env import envs

base_dir = Path(settings.app_dir)


@dataclass
class EmailData:
    subject: str
    html_content: str
    raw_content: str


class EmailService:
    """Service for sending emails using various providers."""

    def _render_email_template(self, template_name: str, context: dict[str, Any], template_type: str) -> str:
        env = envs[template_type]
        template = env.get_template(template_name)
        return template.render(context)

    def _generate_email(self, template_name: str, context: dict[str, Any], subject: str) -> EmailData:
        html_content = self._render_email_template(template_name + ".html", context, "html")
        raw_content = self._render_email_template(template_name + ".txt", context, "raw")

        return EmailData(subject=subject, html_content=html_content, raw_content=raw_content)

    def send_verification_email(self, email_to: str, token: str) -> None:
        """Send email verification link to the user."""

        subject = "Email Address Verification"
        context = {
            "email": email_to,
            "username": email_to,
            "link": f"{settings.FRONTEND_HOST}/verify-email?token={token}",
            "expiration_hours": settings.VERIFICATION_TOKEN_EXPIRE_HOURS,
            "project_name": settings.PROJECT_NAME,
        }

        email_data = self._generate_email("verify_email", context, subject)
        mailer.send_email(email_to, email_data.subject, email_data.html_content, email_data.raw_content)

    def send_password_reset_email(self, email_to: str, token: str) -> None:
        """Send password reset link to the user."""

        subject = "Password Reset Request"
        context = {
            "email": email_to,
            "username": email_to,
            "link": f"{settings.FRONTEND_HOST}/reset-password?token={token}",
            "expiration_hours": settings.PASSWORD_RESET_TOKEN_EXPIRE_HOURS,
            "project_name": settings.PROJECT_NAME,
        }

        email_data = self._generate_email("reset_password", context, subject)
        mailer.send_email(email_to, email_data.subject, email_data.html_content, email_data.raw_content)
