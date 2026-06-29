# 🩺 Security Doctor

**Security Doctor** es una aplicación en Python que analiza una PC con Windows y genera un informe de seguridad simple, visual y entendible.

El objetivo del proyecto es ayudar a usuarios, técnicos de soporte y perfiles help desk a revisar rápidamente el estado básico de seguridad de un equipo sin necesidad de realizar una auditoría compleja.

Al finalizar el análisis, la herramienta muestra un resumen en consola y genera un archivo HTML con explicaciones, recomendaciones y detalles técnicos.

---

## 📌 Índice

- [Descripción](#-descripción)
- [Alcance del proyecto](#-alcance-del-proyecto)
- [Herramientas utilizadas](#-herramientas-utilizadas)
- [Comprobaciones actuales](#-comprobaciones-actuales)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Reporte generado](#-reporte-generado)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Mejoras posibles](#-mejoras-posibles)
- [Aviso importante](#-aviso-importante)

---

## 📖 Descripción

Security Doctor revisa distintas configuraciones importantes de Windows, como firewall, antivirus, cifrado de disco, programas de inicio, espacio libre y políticas básicas del sistema.

La idea principal es que el resultado no sea solo técnico, sino también comprensible para una persona sin experiencia avanzada.

Ejemplo de salida:

```text
✔ Firewall activado
✔ Microsoft Defender activo
⚠ 10 programas inician con Windows
ℹ Contraseña local sin vencimiento detectado
✔ UAC activado

Riesgo general: Medio
```

Además, genera un archivo:

```text
reports/reporte.html
```

con colores, explicaciones y recomendaciones.

---

## 🎯 Alcance del proyecto

Este proyecto está pensado como una herramienta de diagnóstico rápido para:

- soporte técnico;
- help desk;
- auditorías básicas;
- revisión inicial de equipos Windows;
- portfolio personal de IT, soporte o sysadmin junior.

No busca reemplazar una auditoría profesional completa, sino ofrecer una primera lectura clara del estado general del equipo.

---

## 🛠 Herramientas utilizadas

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Windows](https://img.shields.io/badge/Windows-Security-0078D6?logo=windows)
![PowerShell](https://img.shields.io/badge/PowerShell-Commands-5391FE?logo=powershell)
![Rich](https://img.shields.io/badge/Rich-Console-purple)
![Jinja2](https://img.shields.io/badge/Jinja2-Templates-red)
![HTML](https://img.shields.io/badge/HTML-Report-orange?logo=html5)

Tecnologías y módulos principales:

- **Python**: lenguaje principal del proyecto.
- **PowerShell**: consultas al sistema Windows.
- **winreg**: lectura de claves del Registro de Windows.
- **subprocess**: ejecución de comandos del sistema.
- **platform**: validación del sistema operativo.
- **shutil**: revisión de espacio libre en disco.
- **Rich**: salida visual en consola.
- **Jinja2**: generación del reporte HTML.
- **HTML/CSS**: presentación del informe final.

---

## 🔍 Comprobaciones actuales

Security Doctor revisa actualmente:

- estado del Firewall de Windows;
- estado de Microsoft Defender;
- protección de disco con BitLocker;
- política local de contraseña;
- estado de SMBv1;
- programas que inician con Windows;
- espacio libre en disco;
- estado básico de Windows Update;
- estado de UAC.

Cada comprobación incluye:

- estado visual;
- mensaje simple;
- puntos de riesgo;
- explicación para usuarios no técnicos;
- recomendación práctica;
- detalles técnicos opcionales.

---

## ⚙️ Instalación

Clonar el repositorio:

```powershell
git clone https://github.com/tu-usuario/security-doctor.git
cd security-doctor
```

Crear entorno virtual:

```powershell
python -m venv .venv
```

Activar entorno virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar dependencias:

```powershell
pip install -r requirements.txt
```

---

## ▶️ Uso

Ejecutar el análisis:

```powershell
python -m security_doctor.main
```

Al finalizar, se mostrará un resumen en consola y se generará el reporte HTML.

Abrir el reporte:

```powershell
start reports\reporte.html
```

---

## 📄 Reporte generado

El reporte HTML incluye:

- resumen del riesgo general;
- cantidad de comprobaciones correctas, con advertencia o críticas;
- explicación simple de cada punto;
- recomendaciones para el usuario;
- links a guías oficiales cuando corresponde;
- detalles técnicos expandibles.

Ejemplo de secciones incluidas:

- **¿Qué significa?**
- **Recomendación**
- **Leer guía oficial**
- **Ver detalles técnicos**

---

## 🗂 Estructura del proyecto

```text
security-doctor/
│
├── security_doctor/
│   ├── main.py
│   │
│   ├── checks/
│   │   ├── firewall.py
│   │   ├── defender.py
│   │   ├── bitlocker.py
│   │   ├── smb.py
│   │   ├── uac.py
│   │   ├── startup_apps.py
│   │   ├── disk_space.py
│   │   ├── windows_update.py
│   │   └── password_policy.py
│   │
│   ├── reporting/
│   │   ├── console_report.py
│   │   └── html_report.py
│   │
│   └── utils/
│       ├── powershell.py
│       └── risk.py
│
├── templates/
│   └── report.html
│
├── reports/
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Mejoras posibles

Algunas ideas para futuras versiones:

- exportar también el resultado en JSON;
- agregar un modo `--quick` y un modo `--full`;
- detectar versión y edición de Windows;
- revisar Secure Boot y TPM;
- mejorar la detección de Windows Update;
- agregar recomendaciones según nivel de riesgo;
- mostrar gráficos más visuales en el reporte HTML;
- permitir ejecutar checks individuales;
- generar un historial de reportes;
- crear un instalador o ejecutable `.exe`;
- agregar tests unitarios;
- agregar soporte básico para logs.

---

## ⚠️ Aviso importante

Security Doctor es una herramienta orientativa.

Los resultados pueden variar según la edición de Windows, permisos del usuario, configuración del equipo y políticas de empresa.

No reemplaza una auditoría profesional de seguridad, pero puede servir como una primera revisión rápida y clara del estado general de una PC.

---

## 👤 Autor

Proyecto desarrollado como práctica de Python, soporte IT, Windows y automatización de diagnósticos de seguridad.