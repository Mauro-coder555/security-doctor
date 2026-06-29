from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from security_doctor.utils.risk import CheckResult


def generate_html_report(
    results: list[CheckResult],
    general_risk: str,
    output_path: str = "reports/reporte.html",
) -> Path:
    template_dir = Path("templates")

    environment = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(["html", "xml"]),
    )

    template = environment.get_template("report.html")

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    total_points = sum(result.risk_points for result in results)

    status_counts = {
        "ok": sum(1 for result in results if result.status == "ok"),
        "warning": sum(1 for result in results if result.status == "warning"),
        "critical": sum(1 for result in results if result.status == "critical"),
        "info": sum(1 for result in results if result.status == "info"),
        "unknown": sum(1 for result in results if result.status == "unknown"),
    }

    html = template.render(
        results=results,
        general_risk=general_risk,
        total_points=total_points,
        status_counts=status_counts,
    )

    output_file.write_text(html, encoding="utf-8")

    return output_file