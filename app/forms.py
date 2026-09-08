import os
import smtplib
from email.message import EmailMessage

from fastapi import APIRouter, Form
from fastapi.responses import PlainTextResponse
from starlette.concurrency import run_in_threadpool

router = APIRouter()


def _send(to_addr: str, subject: str, fields: list[tuple[str, str]], reply_to: str) -> None:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = os.environ["SMTP_FROM"]
    msg["To"] = to_addr
    msg["Reply-To"] = reply_to
    msg.set_content("\n".join(f"{label}: {value}" for label, value in fields))

    with smtplib.SMTP(os.environ["SMTP_HOST"], int(os.environ.get("SMTP_PORT", 587))) as server:
        server.starttls()
        server.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
        server.send_message(msg)


@router.post("/contact")
async def contact(
    name: str = Form(...),
    email: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...),
) -> PlainTextResponse:
    try:
        await run_in_threadpool(
            _send,
            os.environ["CONTACT_TO_EMAIL"],
            subject,
            [("Nombre", name), ("Email", email), ("Mensaje", message)],
            email,
        )
    except Exception:
        return PlainTextResponse("No se pudo enviar el mensaje, intenta de nuevo más tarde.", status_code=500)
    return PlainTextResponse("OK")


@router.post("/appointment")
async def appointment(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    date: str = Form(...),
    department: str = Form(...),
    doctor: str = Form(...),
    message: str = Form(""),
) -> PlainTextResponse:
    try:
        await run_in_threadpool(
            _send,
            os.environ["APPOINTMENT_TO_EMAIL"],
            "Nueva solicitud de cita",
            [
                ("Nombre", name),
                ("Email", email),
                ("Teléfono", phone),
                ("Fecha solicitada", date),
                ("Especialidad", department),
                ("Ciudad", doctor),
                ("Mensaje", message),
            ],
            email,
        )
    except Exception:
        return PlainTextResponse("No se pudo agendar la cita, intenta de nuevo más tarde.", status_code=500)
    return PlainTextResponse("OK")
