import subprocess

from security_doctor.utils.risk import CheckResult


def check_password_policy() -> CheckResult:
    try:
        completed = subprocess.run(
            ["net", "accounts"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
        )

        output = completed.stdout.strip()

        if completed.returncode != 0:
            return CheckResult(
                name="Política de contraseña",
                status="unknown",
                message="No se pudo comprobar la política de contraseña.",
                details=completed.stderr.strip() or output,
                risk_points=1,
                explanation=(
                    "Windows permite definir reglas locales de contraseña, como longitud mínima, "
                    "vencimiento o bloqueo por intentos fallidos."
                ),
                recommendation="Ejecutá la herramienta como administrador si necesitás una lectura más completa.",
                learn_more_url="https://support.microsoft.com/en-us/accounts-billing/manage/how-to-help-keep-your-microsoft-account-secure",
            )

        lowered_output = output.lower()

        unlimited_keywords = [
            "unlimited",
            "never",
            "nunca",
            "ilimitado",
        ]

        has_unlimited_max_age = any(keyword in lowered_output for keyword in unlimited_keywords)

        explanation = (
            "Esta comprobación revisa reglas locales de contraseña de Windows. "
            "Que una contraseña no tenga vencimiento no siempre es un problema: en equipos personales modernos "
            "puede ser normal, especialmente si usás cuenta Microsoft, Windows Hello, PIN o autenticación adicional. "
            "En empresas, en cambio, conviene revisar esta política junto con MFA, bloqueo por intentos fallidos "
            "y buenas prácticas de acceso."
        )

        recommendation = (
            "Usá una contraseña larga y única, evitá reutilizarla en otros servicios y activá métodos adicionales "
            "como Windows Hello, PIN o verificación en dos pasos cuando estén disponibles. "
            "Si esta PC es de una empresa, seguí la política interna de seguridad."
        )

        if has_unlimited_max_age:
            return CheckResult(
                name="Política de contraseña",
                status="info",
                message="La contraseña local podría no tener vencimiento.",
                details=output,
                risk_points=0,
                explanation=explanation,
                recommendation=recommendation,
                learn_more_url="https://support.microsoft.com/en-us/accounts-billing/manage/how-to-help-keep-your-microsoft-account-secure",
                display_data={
                    "type": "password_policy",
                    "is_password_expiration_unlimited": True,
                },
            )

        return CheckResult(
            name="Política de contraseña",
            status="ok",
            message="Se detectó una política de contraseña configurada.",
            details=output,
            risk_points=0,
            explanation=explanation,
            recommendation=recommendation,
            learn_more_url="https://support.microsoft.com/en-us/accounts-billing/manage/how-to-help-keep-your-microsoft-account-secure",
            display_data={
                "type": "password_policy",
                "is_password_expiration_unlimited": False,
            },
        )

    except Exception as error:
        return CheckResult(
            name="Política de contraseña",
            status="unknown",
            message="No se pudo comprobar la política de contraseña.",
            details=str(error),
            risk_points=1,
            explanation=(
                "Security Doctor intentó revisar la política local de contraseñas, "
                "pero Windows no devolvió información suficiente."
            ),
            recommendation="Probá ejecutar la terminal como administrador o revisá la configuración de inicio de sesión desde Windows.",
            learn_more_url="https://support.microsoft.com/en-us/accounts-billing/manage/how-to-help-keep-your-microsoft-account-secure",
        )