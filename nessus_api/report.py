import time
import requests
import os
import urllib3

from vulnops.config import REPORT_DIR
from vulnops.utils.logger import logger
from vulnops.nessus_api.auth import HEADERS, NESSUS_URL

# 🔇 Disable SSL warning (since you're using verify=False)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

os.makedirs(REPORT_DIR, exist_ok=True)


def generate_and_download_report(scan_id):

    logger.info(f"Generating report for scan {scan_id}")

    try:
        # ✅ FIX 1: Remove template_id (very important)
        export = requests.post(
            f"{NESSUS_URL}/scans/{scan_id}/export",
            headers=HEADERS,
            json={
                "format": "csv",
                "template_id": 61
            },
            verify=False
        )

        if export.status_code != 200:
            raise Exception(f"Export failed: {export.text}")

        export_json = export.json()
        logger.info(f"Export response: {export_json}")

        file_id = export_json.get("file")

        if not file_id:
            raise Exception(f"No file ID returned: {export.text}")

        logger.info(f"Export started. File ID: {file_id}")

        start_time = time.time()

        while True:
            if time.time() - start_time > 600:
                raise Exception("Report generation timeout")

            status_res = requests.get(
                f"{NESSUS_URL}/scans/{scan_id}/export/{file_id}/status",
                headers=HEADERS,
                verify=False
            )

            try:
                status_json = status_res.json()
            except Exception:
                logger.warning("Invalid JSON response, retrying...")
                time.sleep(5)
                continue

            logger.info(f"Raw status response: {status_json}")

            status = status_json.get("status")

            if status == "ready":
                logger.info("Report is ready for download")
                break

            elif status in ["loading", "processing"]:
                time.sleep(5)

            # ❌ FIX 2: DO NOT RETRY ON ERROR
            elif status == "error":
                raise Exception(f"Report generation failed: {status_json}")

            # ❌ FIX 3: Handle "file not found" properly
            elif "error" in status_json:
                raise Exception(f"Nessus error: {status_json}")

            else:
                logger.warning(f"Unknown status: {status}")
                time.sleep(5)

        # 📥 Download
        download = requests.get(
            f"{NESSUS_URL}/scans/{scan_id}/export/{file_id}/download",
            headers=HEADERS,
            verify=False
        )

        if download.status_code != 200:
            raise Exception(f"Download failed: {download.text}")

        path = os.path.join(REPORT_DIR, f"VulnOps_{scan_id}.csv")

        with open(path, "wb") as f:
            f.write(download.content)

        logger.info(f"Report downloaded successfully: {path}")

        return path

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        raise

    except Exception as e:
        logger.error(f"Error: {e}")
        raise


# result = generate_and_download_report(scan_id=29)
# print(result)

# templates = requests.get(
#     f"{NESSUS_URL}/reports/custom/templates",
#     headers=HEADERS,
#     verify=False
# )

# print(templates.json())