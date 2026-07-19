import csv

def parse_nessus_csv(file_path):
    critical, high, medium = [], [], []

    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            severity = row.get("Risk", "").strip().lower()

            vuln = {
                "name": row.get("Name"),
                "host": row.get("Host"),
                "port": row.get("Port"),
                "severity": severity,
                "description": row.get("Description"),
                "solution": row.get("Solution"),
            }

            if severity == "critical":
                critical.append(vuln)
            elif severity == "high":
                high.append(vuln)
            elif severity == "medium":
                medium.append(vuln)

    return critical, high, medium