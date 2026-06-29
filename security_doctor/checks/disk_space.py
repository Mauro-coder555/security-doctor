import shutil

from security_doctor.utils.risk import CheckResult


def check_disk_space() -> CheckResult:
    total, used, free = shutil.disk_usage("C:\\")

    total_gb = round(total / (1024 ** 3), 2)
    used_gb = round(used / (1024 ** 3), 2)
    free_gb = round(free / (1024 ** 3), 2)

    free_percentage = round((free / total) * 100, 2)

    details = (
        f"Disco C:\\\n"
        f"Total: {total_gb} GB\n"
        f"Usado: {used_gb} GB\n"
        f"Libre: {free_gb} GB\n"
        f"Porcentaje libre: {free_percentage}%"
    )

    explanation = (
        "El espacio libre en disco es importante para que Windows pueda actualizarse, crear archivos temporales "
        "y funcionar con normalidad. Cuando el disco está casi lleno, la PC puede ponerse lenta o fallar al instalar actualizaciones."
    )

    recommendation = (
        "Si tenés poco espacio libre, revisá Descargas, Papelera, archivos grandes, juegos o programas que ya no uses. "
        "También podés usar la herramienta de limpieza de almacenamiento de Windows."
    )

    if free_percentage < 10:
        return CheckResult(
            name="Espacio libre en disco",
            status="critical",
            message=f"Queda muy poco espacio libre en el disco C: {free_gb} GB disponibles.",
            details=details,
            risk_points=3,
            explanation=explanation,
            recommendation=recommendation,
            learn_more_url="https://support.microsoft.com/en-us/windows/free-up-drive-space-in-windows",
            display_data={
                "type": "disk_space",
                "total_gb": total_gb,
                "used_gb": used_gb,
                "free_gb": free_gb,
                "free_percentage": free_percentage,
            },
        )

    if free_percentage < 20:
        return CheckResult(
            name="Espacio libre en disco",
            status="warning",
            message=f"El disco C: tiene poco espacio libre: {free_gb} GB disponibles.",
            details=details,
            risk_points=1,
            explanation=explanation,
            recommendation=recommendation,
            learn_more_url="https://support.microsoft.com/en-us/windows/free-up-drive-space-in-windows",
            display_data={
                "type": "disk_space",
                "total_gb": total_gb,
                "used_gb": used_gb,
                "free_gb": free_gb,
                "free_percentage": free_percentage,
            },
        )

    return CheckResult(
        name="Espacio libre en disco",
        status="ok",
        message=f"El disco C: tiene espacio libre suficiente: {free_gb} GB disponibles.",
        details=details,
        risk_points=0,
        explanation=explanation,
        recommendation="El espacio libre parece saludable. No hace falta hacer cambios por ahora.",
        learn_more_url="https://support.microsoft.com/en-us/windows/free-up-drive-space-in-windows",
        display_data={
            "type": "disk_space",
            "total_gb": total_gb,
            "used_gb": used_gb,
            "free_gb": free_gb,
            "free_percentage": free_percentage,
        },
    )