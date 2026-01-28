import logging
from typing import Iterable

from src.services.gmail.client import GmailClient

log = logging.getLogger("auditoria_mailer")


def _s(v) -> str:
    if v is None:
        return ""
    try:
        if v != v:
            return ""
    except Exception:
        pass
    return str(v).strip()


def notify_atrasados(
    gmail: GmailClient,
    rows: Iterable[dict],
) -> None:

    for row in rows:
        to = _s(row.get("Correo responsable"))
        if not to:
            log.warning("Fila sin correo responsable, se omite")
            continue

        proceso = _s(row.get("Auditoria/Proceso"))
        responsable = _s(row.get("Responsable"))
        obs = _s(row.get("Observación"))
        fecha = _s(row.get("Fecha Compromiso"))
        estado = _s(row.get("Estado"))

        subject = f"[Auditoría] Observación ATRASADA - {proceso}"

        html = f"""
<html>
  <body style="font-family: Arial, sans-serif; font-size: 13px; color: #333;">
    <p>Hola <strong>{responsable}</strong>,</p>

    <p>
      Tenés una <strong>observación ATRASADA</strong>.
      A continuación, el detalle:
    </p>

    <table style="border-collapse: collapse; width: 100%; max-width: 600px;">
      <tr>
        <th style="text-align:left; padding:8px; border:1px solid #ddd; background:#f4f4f4;">
          Proceso
        </th>
        <td style="padding:8px; border:1px solid #ddd;">
          {proceso}
        </td>
      </tr>

      <tr>
        <th style="text-align:left; padding:8px; border:1px solid #ddd; background:#f4f4f4;">
          Observación
        </th>
        <td style="padding:8px; border:1px solid #ddd;">
          {obs}
        </td>
      </tr>

      <tr>
        <th style="text-align:left; padding:8px; border:1px solid #ddd; background:#f4f4f4;">
          Fecha compromiso
        </th>
        <td style="padding:8px; border:1px solid #ddd;">
          {fecha}
        </td>
      </tr>

      <tr>
        <th style="text-align:left; padding:8px; border:1px solid #ddd; background:#f4f4f4;">
          Estado
        </th>
        <td style="padding:8px; border:1px solid #ddd; font-weight:bold; color:#c0392b;">
          {estado}
        </td>
      </tr>
    </table>

    <p style="margin-top:16px;">
      Por favor, revisá la observación y regularizá la situación a la brevedad.
    </p>

    <p>
      Saludos,<br>
      <strong>Auditoría Interna</strong>
    </p>
  </body>
</html>
""".strip()

        gmail.send_html(to, subject, html)
        log.info("Notificación enviada a %s | %s", to, subject)
