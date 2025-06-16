import resend

from app.config import settings

resend.api_key = settings.RESEND_API_KEY


def send_email(to: str, subject: str, html_content: str, raw_content: str) -> None:
    if not settings.emails_enabled:
        raise RuntimeError("Email sending is disabled in the settings.")

    params: resend.Emails.SendParams = {
        "from": f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>",
        "to": [to],
        "subject": subject,
        "html": html_content,
        "text": raw_content,
    }

    resend.Emails.send(params)
