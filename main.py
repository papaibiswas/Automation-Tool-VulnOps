from vulnops.nessus_api.scan import create_scan, launch_scan, wait_for_completion
from vulnops.nessus_api.report import generate_and_download_report
from vulnops.integrations.telegram import send_report
from vulnops.reporting.parser import parse_nessus_csv
from vulnops.reporting.pdf_generator import generate_pdf
from vulnops.utils.logger import logger

from datetime import datetime


def main():
    target_ip = input("Enter Target IP: ").strip()

    if not target_ip:
        print("❌ Target IP cannot be empty")
        return

    try:
        logger.info(f"Starting scan for target: {target_ip}")
        print(f"Starting scan for target: {target_ip}")

        # 🔥 Create scan (no creds)
        scan_id = create_scan(target_ip=target_ip)

        launch_scan(scan_id)
        wait_for_completion(scan_id)

        # 🔥 Get CSV report
        csv_path = generate_and_download_report(scan_id)

        # 🔥 Parse CSV
        critical, high, medium = parse_nessus_csv(csv_path)

        # 🔥 Scan info (always unauthenticated now)
        scan_info = {
            "target": target_ip,
            "scan_type": "Unauthenticated",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        # 🔥 Generate final PDF
        final_pdf = csv_path.replace(".csv", "_final.pdf")
        generate_pdf(final_pdf, scan_info, critical, high, medium)

        # 🔥 Send to Telegram
        send_report(final_pdf)

        print("✅ VulnOps Completed Successfully")
        logger.info("VulnOps completed successfully")

    except Exception as e:
        print(f"❌ Error: {e}")
        logger.exception("Unhandled exception occurred")


if __name__ == "__main__":
    main()