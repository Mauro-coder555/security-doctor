import winreg

from security_doctor.utils.risk import CheckResult


def check_smbv1() -> CheckResult:
    registry_path = r"SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters"

    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path) as key:
            try:
                value, _ = winreg.QueryValueEx(key, "SMB1")
            except FileNotFoundError:
                value = 0

        if value == 1:
            return CheckResult(
                name="SMBv1",
                status="critical",
                message="SMBv1 está habilitado.",
                details="SMBv1 es un protocolo antiguo y riesgoso. Se recomienda deshabilitarlo salvo que exista una necesidad muy específica.",
                risk_points=3,
            )

        return CheckResult(
            name="SMBv1",
            status="ok",
            message="SMBv1 no parece estar habilitado.",
            details="No se detectó SMBv1 habilitado en el registro del sistema.",
            risk_points=0,
        )

    except PermissionError:
        return CheckResult(
            name="SMBv1",
            status="unknown",
            message="No se pudo comprobar SMBv1 por permisos insuficientes.",
            details="Ejecutar como administrador puede permitir una lectura más completa.",
            risk_points=1,
        )

    except Exception as error:
        return CheckResult(
            name="SMBv1",
            status="unknown",
            message="No se pudo comprobar SMBv1.",
            details=str(error),
            risk_points=1,
        )