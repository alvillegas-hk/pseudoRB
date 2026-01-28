import base64
from email.message import EmailMessage


def build_message(
    sender: str,
    to: str,
    subject: str,
    content: str,
    is_html: bool = False,
) -> str:
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = to
    msg["Subject"] = subject

    if is_html:
        msg.add_alternative(content, subtype="html")
    else:
        msg.set_content(content)

    return base64.urlsafe_b64encode(
        msg.as_bytes()
    ).decode("utf-8")
