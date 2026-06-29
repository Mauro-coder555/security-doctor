import winreg

from security_doctor.utils.risk import CheckResult


def check_uac() -> CheckResult:
    registry_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"

    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path) as key:
            value, _ = winreg.QueryValueEx(key, "EnableLUA")

        if value == 1:
            return CheckResult(
                name="UAC",
                status="ok",
                message="UAC activado.",
                details="User Account Control está activo.",
                risk_points=0,
            )

        return CheckResult(
            name="UAC",
            status="critical",
            message="UAC está desactivado.",
            details="Esto puede permitir cambios sensibles en el sistema con menos controles.",
            risk_points=3,
        )

    except PermissionError:
        return CheckResult(
            name="UAC",
            status="unknown",
            message="No se pudo comprobar UAC por permisos insuficientes.",
            details="Ejecutar como administrador puede permitir una lectura más completa.",
            risk_points=1,
        )

    except Exception as error:
        return CheckResult(
            name="UAC",
            status="unknown",
            message="No se pudo comprobar UAC.",
            details=str(error),
            risk_points=1,
        )