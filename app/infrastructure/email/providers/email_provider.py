from abc import ABC, abstractmethod


class EmailProvider(ABC):
    @abstractmethod
    def send_email(self, to: str, subject: str, html_content: str, raw_content: str) -> None:
        """Send an email to the specified recipient."""
        pass
