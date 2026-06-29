from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from security_doctor.utils.risk import CheckResult, status_icon


console = Console()


def print_console_report(results: list[CheckResult], general_risk: str) -> None:
    console.print(
        Panel.fit(
            "[bold cyan]Security Doctor[/bold cyan]\nAnálisis rápido de seguridad para Windows",
            border_style="cyan",
        )
    )

    table = Table(show_header=True, header_style="bold")
    table.add_column("Estado", justify="center")
    table.add_column("Comprobación")
    table.add_column("Resultado")
    table.add_column("Riesgo", justify="center")

    for result in results:
        style = _style_for_status(result.status)

        table.add_row(
            status_icon(result.status),
            result.name,
            result.message,
            str(result.risk_points),
            style=style,
        )

    console.print(table)

    risk_style = {
        "Bajo": "green",
        "Medio": "yellow",
        "Alto": "red",
    }.get(general_risk, "white")

    console.print(f"\n[bold]Riesgo general:[/bold] [{risk_style}]{general_risk}[/{risk_style}]")


def _style_for_status(status: str) -> str:
    styles = {
        "ok": "green",
        "warning": "yellow",
        "critical": "red",
        "info": "cyan",
        "unknown": "dim",
    }

    return styles.get(status, "white")