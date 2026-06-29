import winreg

from security_doctor.utils.risk import CheckResult


STARTUP_LOCATIONS = [
    (
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        "Usuario actual",
    ),
    (
        winreg.HKEY_LOCAL_MACHINE,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        "Equipo",
    ),
]


def _read_startup_location(root, path: str, location_label: str) -> list[dict[str, str]]:
    apps = []

    try:
        with winreg.OpenKey(root, path) as key:
            index = 0

            while True:
                try:
                    name, command, _ = winreg.EnumValue(key, index)

                    apps.append(
                        {
                            "name": str(name),
                            "command": str(command),
                            "location": location_label,
                            "registry_path": path,
                        }
                    )

                    index += 1

                except OSError:
                    break

    except FileNotFoundError:
        return []

    except PermissionError:
        apps.append(
            {
                "name": "Ubicación no accesible",
                "command": "No se pudo leer esta ubicación por permisos insuficientes.",
                "location": location_label,
                "registry_path": path,
            }
        )

    return apps


def check_startup_apps() -> CheckResult:
    apps = []

    for root, path, location_label in STARTUP_LOCATIONS:
        apps.extend(_read_startup_location(root, path, location_label))

    total = len(apps)

    human_list = "\n".join(
        f"- {app['name']} ({app['location']})"
        for app in apps
    )

    technical_details = "\n".join(
        f"{app['name']}\n"
        f"  Ubicación: {app['location']}\n"
        f"  Registro: {app['registry_path']}\n"
        f"  Comando: {app['command']}\n"
        for app in apps
    )

    explanation = (
        "Estas son aplicaciones que Windows intenta abrir automáticamente al iniciar sesión. "
        "No significa que sean virus ni que estén mal, pero muchas apps de inicio pueden hacer "
        "que la PC tarde más en arrancar y consuma más memoria en segundo plano."
    )

    recommendation = (
        "Revisá la lista y desactivá solo las apps que reconozcas y que no necesites al iniciar. "
        "No conviene desactivar antivirus, drivers de audio, drivers de video, sincronización importante "
        "o herramientas de trabajo sin estar seguro."
    )

    if total >= 10:
        return CheckResult(
            name="Programas de inicio",
            status="warning",
            message=f"{total} programas inician con Windows.",
            details=technical_details or "No se encontraron detalles técnicos.",
            risk_points=2,
            explanation=explanation,
            recommendation=recommendation,
            learn_more_url="https://support.microsoft.com/en-US/Windows/Experience/Startup-Boot/configure-startup-applications-in-windows",
            display_data={
                "type": "startup_apps",
                "apps": apps,
                "summary": human_list,
            },
        )

    if total >= 5:
        return CheckResult(
            name="Programas de inicio",
            status="warning",
            message=f"{total} programas inician con Windows.",
            details=technical_details or "No se encontraron detalles técnicos.",
            risk_points=1,
            explanation=explanation,
            recommendation=recommendation,
            learn_more_url="https://support.microsoft.com/en-US/Windows/Experience/Startup-Boot/configure-startup-applications-in-windows",
            display_data={
                "type": "startup_apps",
                "apps": apps,
                "summary": human_list,
            },
        )

    return CheckResult(
        name="Programas de inicio",
        status="ok",
        message=f"{total} programas inician con Windows.",
        details=technical_details or "No se detectaron programas de inicio en las ubicaciones revisadas.",
        risk_points=0,
        explanation=explanation,
        recommendation="La cantidad de apps de inicio parece razonable. No hace falta cambiar nada si la PC funciona bien.",
        learn_more_url="https://support.microsoft.com/en-US/Windows/Experience/Startup-Boot/configure-startup-applications-in-windows",
        display_data={
            "type": "startup_apps",
            "apps": apps,
            "summary": human_list,
        },
    )