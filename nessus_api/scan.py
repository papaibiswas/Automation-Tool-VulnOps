import time
import requests

from vulnops.utils.logger import logger
from vulnops.nessus_api.auth import HEADERS, NESSUS_URL


def get_template_uuid():
    try:
        response = requests.get(
            f"{NESSUS_URL}/editor/scan/templates",
            headers=HEADERS,
            verify=False
        )
        response.raise_for_status()

        templates = response.json().get("templates", [])

        for template in templates:
            # 🔥 Use Advanced Scan (important for credentials)
            if template.get("title") == "Advanced Scan":
                return template.get("uuid")

        raise Exception("Advanced Scan template not found")

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch templates: {e}")
        raise


def create_scan(target_ip, ssh_creds=None, windows_creds=None):
    uuid = get_template_uuid()

    settings = {
        "name": f"VulnOps Scan - {target_ip}",
        "text_targets": target_ip
    }

    # 🔐 SSH Credentials (FIXED)
    # if ssh_creds:
    #     settings.update({
    #         "auth_method": "password",
    #         "ssh_username": ssh_creds.get("username"),
    #         "ssh_password": ssh_creds.get("password"),
    #         "ssh_port": ssh_creds.get("port", 22),

    #         "ssh_use_key": "no",
    #         "ssh_password_auth": "yes",

    #         "ssh_elevate_privileges": "sudo",
    #         "ssh_elevate_method": "sudo",
    #         "ssh_elevate_password": ssh_creds.get("password"),

    #         "ssh_known_hosts": ""
    #     })

    # # 🪟 Windows Credentials
    # if windows_creds:
    #     settings.update({
    #         "smb_username": windows_creds.get("username"),
    #         "smb_password": windows_creds.get("password"),
    #         "smb_domain": windows_creds.get("domain", "")
    #     })

    data = {
        "uuid": uuid,
        "settings": settings
    }

    try:
        response = requests.post(
            f"{NESSUS_URL}/scans",
            headers=HEADERS,
            json=data,
            verify=False
        )
        response.raise_for_status()

        scan_id = response.json()["scan"]["id"]

        logger.info(f"Scan created with ID: {scan_id}")
        return scan_id

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to create scan: {e}")
        raise


def launch_scan(scan_id):
    try:
        response = requests.post(
            f"{NESSUS_URL}/scans/{scan_id}/launch",
            headers=HEADERS,
            verify=False
        )
        response.raise_for_status()

        logger.info(f"Scan {scan_id} launched successfully")

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to launch scan {scan_id}: {e}")
        raise


def wait_for_completion(scan_id):
    logger.info(f"Waiting for scan {scan_id} to complete...")

    while True:
        try:
            response = requests.get(
                f"{NESSUS_URL}/scans/{scan_id}",
                headers=HEADERS,
                verify=False
            )
            response.raise_for_status()

            status = response.json().get("info", {}).get("status")

            logger.info(f"Scan status: {status}")

            if status in ["running", "pending", "processing"]:
                time.sleep(15)

            elif status == "completed":
                logger.info("Scan completed. Waiting for backend processing...")
                time.sleep(90)
                return True

            elif status in ["canceled", "paused", "stopped"]:
                raise Exception(f"Scan failed: {status}")

            else:
                time.sleep(10)

        except requests.exceptions.RequestException as e:
            logger.error(f"Error checking scan status: {e}")
            raise
