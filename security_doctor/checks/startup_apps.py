import winreg

from security_doctor.utils.risk import CheckResult


STARTUP_LOCATIONS = [
    (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", "Usuario actual"),
    (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run", "Equipo"),
]


def _count_registry_values(root, path: str) -> tuple[int, list[str]]:
    items = []

    try:
        with winreg.OpenKey(root, path) as key:
            index = 0

            while True:
                try:
                    name, value, _ = winreg.EnumValue(key, index)
                    items.append(f"{name}: {value}")
                    index += 1
                except OSError:
                    break

    except FileNotFoundError:
        return 0, []

    except PermissionError:
        return 0, ["No se pudo leer una ubicación por permisos insuficientes."]

    return len(items), items


def check_startup_apps() -> CheckResult:
    total = 0
    details = []

    for root, path, label in STARTUP_LOCATIONS:
        count, items = _count_registry_values(root, path)
        total += count

        details.append(f"[{label}] {count} programas")
        details.extend(items)

    details_text = "\n".join(details)

    if total >= 10:
        return CheckResult(
            name="Programas de inicio",
            status="warning",
            message=f"{total} programas inician con Windows.",
            details=details_text,
            risk_points=2,
        )

    if total >= 5:
        return CheckResult(
            name="Programas de inicio",
            status="warning",
            message=f"{total} programas inician con Windows.",
            details=details_text,
            risk_points=1,
        )

    return CheckResult(
        name="Programas de inicio",
        status="ok",
        message=f"{total} programas inician con Windows.",
        details=details_text or "No se detectaron programas de inicio en las ubicaciones revisadas.",
        risk_points=0,
    )