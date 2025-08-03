import os
import argparse
import csv

def scan_directory(root_dir, output_csv="file_listing.csv", filter_exts=None):
    entries = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for name in filenames:
            full_path = os.path.join(dirpath, name)
            if filter_exts and os.path.splitext(name)[1].lower() not in filter_exts:
                continue
            try:
                stat = os.stat(full_path)
            except Exception as e:
                print(f"[!] Skipping unreadable file: {full_path} ({e})")
                continue
            ext = os.path.splitext(name)[1].lower()
            if ext in [".txt", ".py", ".tex"]:
                continue

            if ext == ".json":
                category = "1_json"
            elif ext == ".csv":
                category = "2_csv"
            elif ext in [".xlsx", ".xls"]:
                category = "3_excel"
            elif ext == ".pdf":
                category = "4_pdf"
            elif ext in [".doc", ".docx"]:
                category = "5_doc"
            else:
                category = "9_other"

            if category == "9_other":
                continue

            size_mb = round(stat.st_size / (1024 * 1024), 2)

            entries.append({
                "type": "file",
                "path": full_path,
                "size_bytes": stat.st_size,
                "size_mb": size_mb,
                "category": category
            })

    entries.sort(key=lambda x: x["category"])

    with open(output_csv, "w", newline="") as f:
        fieldnames = ["type", "path", "size_bytes", "size_mb", "category"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(entries)

    print(f"[✓] Exported directory listing to: {output_csv}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List all files and directories recursively.")
    parser.add_argument("--root", "-r", default="/Users/jc/Downloads/Uriel", help="Root directory to scan")
    parser.add_argument("--output", "-o", help="Optional path to output CSV")
    parser.add_argument("--filter", "-f", nargs="+",
                        help="Only include files with specified extensions (e.g. --filter .csv .json .xlsx)")
    args = parser.parse_args()

    if not args.output:
        args.output = "file_listing.csv"

    scan_directory(args.root, args.output, args.filter)