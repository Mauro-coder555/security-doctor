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
            )

        lowered_output = output.lower()

        unlimited_keywords = [
            "unlimited",
            "never",
            "nunca",
            "ilimitado",
        ]

        has_unlimited_max_age = any(keyword in lowered_output for keyword in unlimited_keywords)

        if has_unlimited_max_age:
            return CheckResult(
                name="Política de contraseña",
                status="warning",
                message="La contraseña de usuario podría no tener vencimiento.",
                details=output,
                risk_points=1,
            )

        return CheckResult(
            name="Política de contraseña",
            status="ok",
            message="Se detectó una política de contraseña configurada.",
            details=output,
            risk_points=0,
        )

    except Exception as error:
        return CheckResult(
            name="Política de contraseña",
            status="unknown",
            message="No se pudo comprobar la política de contraseña.",
            details=str(error),
            risk_points=1,
        )