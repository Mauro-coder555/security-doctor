from datetime import datetime

from security_doctor.utils.powershell import run_powershell
from security_doctor.utils.risk import CheckResult


def check_windows_update() -> CheckResult:
    command = (
        "Get-HotFix | "
        "Sort-Object InstalledOn -Descending | "
        "Select-Object -First 1 HotFixID, InstalledOn, Description | "
        "ConvertTo-Json"
    )

    success, output = run_powershell(command)

    if not success:
        return CheckResult(
            name="Windows Update",
            status="unknown",
            message="No se pudo comprobar la última actualización instalada.",
            details=output,
            risk_points=1,
        )

    if "InstalledOn" not in output:
        return CheckResult(
            name="Windows Update",
            status="unknown",
            message="No se encontró información suficiente sobre actualizaciones.",
            details=output,
            risk_points=1,
        )

    return CheckResult(
        name="Windows Update",
        status="ok",
        message="Se detectaron actualizaciones instaladas recientemente.",
        details=output,
        risk_points=0,
    )