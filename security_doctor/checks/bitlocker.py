from security_doctor.utils.powershell import run_powershell
from security_doctor.utils.risk import CheckResult


BITLOCKER_EXPLANATION = (
    "BitLocker es una función de Windows que cifra el disco. En palabras simples: "
    "ayuda a proteger tus archivos si alguien roba la notebook, saca el disco o intenta leerlo "
    "desde otra computadora. Sin la clave correcta, los datos quedan mucho más difíciles de acceder."
)

BITLOCKER_RECOMMENDATION = (
    "Si usás una notebook o guardás información importante, conviene tener cifrado de disco activado. "
    "Antes de activar BitLocker o Device Encryption, asegurate de guardar bien la clave de recuperación, "
    "porque puede ser necesaria para recuperar el acceso al equipo."
)

BITLOCKER_URL = "https://support.microsoft.com/en-US/Windows/Security/Encryption/bitlocker-overview"


def check_bitlocker() -> CheckResult:
    command = (
        "Get-BitLockerVolume -MountPoint C: | "
        "Select-Object MountPoint, ProtectionStatus, VolumeStatus, EncryptionPercentage | "
        "ConvertTo-Json"
    )

    success, output = run_powershell(command)

    if not success:
        return CheckResult(
            name="BitLocker / cifrado de disco",
            status="unknown",
            message="No se pudo comprobar BitLocker en el disco principal.",
            details=output,
            risk_points=0,
            explanation=BITLOCKER_EXPLANATION,
            recommendation=(
                "Esto no significa necesariamente que tu PC esté mal. Algunas ediciones de Windows o algunos equipos "
                "usan Device Encryption en vez de BitLocker clásico, o no muestran esta información sin permisos. "
                "Podés revisar manualmente en Configuración de Windows > Privacidad y seguridad > Cifrado de dispositivo."
            ),
            learn_more_url=BITLOCKER_URL,
            display_data={
                "type": "bitlocker",
                "available": False,
                "protected": None,
            },
        )

    protection_on = '"ProtectionStatus":  1' in output or '"ProtectionStatus": 1' in output
    fully_encrypted = "FullyEncrypted" in output

    if protection_on and fully_encrypted:
        return CheckResult(
            name="BitLocker / cifrado de disco",
            status="ok",
            message="El disco principal parece estar cifrado y protegido.",
            details=output,
            risk_points=0,
            explanation=BITLOCKER_EXPLANATION,
            recommendation=(
                "Buen estado. Asegurate de saber dónde está guardada tu clave de recuperación de BitLocker, "
                "especialmente si esta PC es personal y no está administrada por una empresa."
            ),
            learn_more_url=BITLOCKER_URL,
            display_data={
                "type": "bitlocker",
                "available": True,
                "protected": True,
            },
        )

    if protection_on:
        return CheckResult(
            name="BitLocker / cifrado de disco",
            status="warning",
            message="BitLocker parece estar activo, pero el estado del volumen debería revisarse.",
            details=output,
            risk_points=1,
            explanation=BITLOCKER_EXPLANATION,
            recommendation=BITLOCKER_RECOMMENDATION,
            learn_more_url=BITLOCKER_URL,
            display_data={
                "type": "bitlocker",
                "available": True,
                "protected": "partial",
            },
        )

    return CheckResult(
        name="BitLocker / cifrado de disco",
        status="warning",
        message="El disco principal no parece estar protegido con BitLocker.",
        details=output,
        risk_points=1,
        explanation=BITLOCKER_EXPLANATION,
        recommendation=BITLOCKER_RECOMMENDATION,
        learn_more_url=BITLOCKER_URL,
        display_data={
            "type": "bitlocker",
            "available": True,
            "protected": False,
        },
    )