# sudoRocketBot

Automatización de seguimiento de observaciones de auditoría.

El bot:
- Lee observaciones desde un archivo Excel
- Filtra por estado (Atrasado / Regularizado)
- Envía correos automáticos vía Gmail a responsables de observaciones atrasadas
- Carga observaciones regularizadas en un formulario web mediante Playwright
- Registra logs de ejecución y errores

---

## 📂 Estructura del proyecto

```text
sudoRocketBot/
├─ assets/                    # Archivos de entrada (Excel)
│  └─ Base_Seguimiento.xlsx
│
├─ secrets/                   # Credenciales sensibles (NO versionar)
│  ├─ client_secret_*.json    # OAuth Gmail
│  └─ token.json
│
├─ logs/                      # Logs de ejecución
│  └─ app.log
│
├─ src/
│  ├─ config/
│  │  ├─ settings.py          # Variables de entorno
│  │  └─ logging_config.py    # Configuración de logs
│  │
│  ├─ core/
│  │  ├─ excel_loader.py      # Lectura de Excel
│  │  ├─ processing.py        # Lógica de negocio
│  │  └─ validators.py        # Validaciones
│  │
│  ├─ services/
│  │  ├─ gmail_service.py     # Envío de mails (Gmail API)
│  │  └─ playwright/
│  │     ├─ discovery.py      # Descubrimiento dinámico del form
│  │     ├─ mapping.py        # Mapeo Excel → formulario
│  │     ├─ fillers.py        # Llenado de campos
│  │     ├─ submit.py         # Submit del form
│  │     └─ runner.py         # Orquestador Playwright
│  │
│  └─ main.py                 # Punto de entrada
│
├─ .env                       # Variables de entorno (NO versionar)
├─ requirements.txt
├─ .gitignore
└─ README.md
