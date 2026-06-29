from security_doctor.utils.powershell import run_powershell
from security_doctor.utils.risk import CheckResult


def check_firewall() -> CheckResult:
    command = "Get-NetFirewallProfile | Select-Object Name, Enabled | ConvertTo-Json"

    success, output = run_powershell(command)

    if not success:
        return CheckResult(
            name="Firewall de Windows",
            status="unknown",
            message="No se pudo comprobar el estado del Firewall.",
            details=output,
            risk_points=1,
        )

    disabled_profiles = []

    for line in output.splitlines():
        if '"Enabled":  false' in line or '"Enabled": false' in line:
            disabled_profiles.append(line)

    if disabled_profiles:
        return CheckResult(
            name="Firewall de Windows",
            status="critical",
            message="Hay perfiles del Firewall desactivados.",
            details=output,
            risk_points=3,
        )

    return CheckResult(
        name="Firewall de Windows",
        status="ok",
        message="Firewall activado.",
        details="Todos los perfiles del Firewall parecen estar activos.",
        risk_points=0,
    )