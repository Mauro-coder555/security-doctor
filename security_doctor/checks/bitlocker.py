from security_doctor.utils.powershell import run_powershell
from security_doctor.utils.risk import CheckResult


def check_bitlocker() -> CheckResult:
    command = "Get-BitLockerVolume -MountPoint C: | Select-Object MountPoint, ProtectionStatus, VolumeStatus | ConvertTo-Json"

    success, output = run_powershell(command)

    if not success:
        return CheckResult(
            name="BitLocker",
            status="unknown",
            message="No se pudo comprobar BitLocker. Puede requerir permisos o no estar disponible en esta edición de Windows.",
            details=output,
            risk_points=1,
        )

    protection_on = '"ProtectionStatus":  1' in output or '"ProtectionStatus": 1' in output
    fully_encrypted = "FullyEncrypted" in output

    if protection_on and fully_encrypted:
        return CheckResult(
            name="BitLocker",
            status="ok",
            message="Disco cifrado con BitLocker.",
            details=output,
            risk_points=0,
        )

    if protection_on:
        return CheckResult(
            name="BitLocker",
            status="warning",
            message="BitLocker está activo, pero el estado del volumen debería revisarse.",
            details=output,
            risk_points=1,
        )

    return CheckResult(
        name="BitLocker",
        status="warning",
        message="BitLocker no parece estar protegiendo el disco principal.",
        details=output,
        risk_points=2,
    )