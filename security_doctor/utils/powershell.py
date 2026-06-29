import subprocess


def run_powershell(command: str, timeout: int = 20) -> tuple[bool, str]:
    """
    Executes a PowerShell command and returns:
    - success status
    - stdout or stderr text

    This helper avoids crashing the app if a command fails.
    """
    try:
        completed = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-Command",
                command,
            ],
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
        )

        if completed.returncode == 0:
            return True, completed.stdout.strip()

        return False, completed.stderr.strip() or completed.stdout.strip()

    except subprocess.TimeoutExpired:
        return False, "The PowerShell command timed out."

    except FileNotFoundError:
        return False, "PowerShell was not found on this system."

    except Exception as error:
        return False, f"Unexpected error while running PowerShell: {error}"