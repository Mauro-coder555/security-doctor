import platform

from security_doctor.checks.bitlocker import check_bitlocker
from security_doctor.checks.defender import check_defender
from security_doctor.checks.disk_space import check_disk_space
from security_doctor.checks.firewall import check_firewall
from security_doctor.checks.password_policy import check_password_policy
from security_doctor.checks.smb import check_smbv1
from security_doctor.checks.startup_apps import check_startup_apps
from security_doctor.checks.uac import check_uac
from security_doctor.checks.windows_update import check_windows_update
from security_doctor.reporting.console_report import print_console_report
from security_doctor.reporting.html_report import generate_html_report
from security_doctor.utils.risk import calculate_general_risk


def main() -> None:
    if platform.system() != "Windows":
        print("Security Doctor está pensado para ejecutarse en Windows.")
        return

    results = [
        check_firewall(),
        check_defender(),
        check_bitlocker(),
        check_password_policy(),
        check_smbv1(),
        check_startup_apps(),
        check_disk_space(),
        check_windows_update(),
        check_uac(),
    ]

    general_risk = calculate_general_risk(results)

    print_console_report(results, general_risk)

    report_path = generate_html_report(results, general_risk)

    print(f"\nReporte HTML generado en: {report_path}")


if __name__ == "__main__":
    main()