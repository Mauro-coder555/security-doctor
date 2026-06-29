from security_doctor.utils.powershell import run_powershell
from security_doctor.utils.risk import CheckResult


def check_defender() -> CheckResult:
    command = (
        "Get-MpComputerStatus | "
        "Select-Object AntivirusEnabled, RealTimeProtectionEnabled, AntivirusSignatureLastUpdated | "
        "ConvertTo-Json"
    )

    success, output = run_powershell(command)

    if not success:
        return CheckResult(
            name="Microsoft Defender",
            status="unknown",
            message="No se pudo comprobar Microsoft Defender.",
            details=output,
            risk_points=1,
        )

    antivirus_enabled = '"AntivirusEnabled":  true' in output or '"AntivirusEnabled": true' in output
    realtime_enabled = '"RealTimeProtectionEnabled":  true' in output or '"RealTimeProtectionEnabled": true' in output

    if not antivirus_enabled:
        return CheckResult(
            name="Microsoft Defender",
            status="critical",
            message="Microsoft Defender parece estar desactivado.",
            details=output,
            risk_points=3,
        )

    if not realtime_enabled:
        return CheckResult(
            name="Microsoft Defender",
            status="warning",
            message="La protección en tiempo real parece estar desactivada.",
            details=output,
            risk_points=2,
        )

    return CheckResult(
        name="Microsoft Defender",
        status="ok",
        message="Microsoft Defender está activo.",
        details=output,
        risk_points=0,
    )