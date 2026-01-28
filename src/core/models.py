from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class Observacion:
    auditoria_proceso: str
    observacion: str
    tipo_riesgo: str
    severidad: str
    plan_accion: str
    fecha_compromiso: Optional[date]
    responsable: str
    area_responsable: str
    correo_responsable: str
    estado: str
