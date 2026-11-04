
import os
import json
import base64

EXCLUDED_EXTENSIONS = {
    ".onnx",
    ".pkl",
    ".pptx",
    ".xlsx"
}

EXCLUDED_DIRECTORIES = {
    ".git"
}

def folder_to_bundle(source_folder, output_file):

    bundle = {
        "format": "folder-bundle",
        "version": 1,
        "files": []
    }

    total_processed = 0
    total_skipped = 0

    print("\nStarting folder conversion...")
    print(f"Source folder: {source_folder}\n")

    for root, dirs, files in os.walk(source_folder):

        # Exclude specified directories (prune traversal)
        excluded_dirs = [
            d for d in dirs
            if d.lower() in EXCLUDED_DIRECTORIES
        ]

        for directory in excluded_dirs:
            print(f"[SKIPPED DIRECTORY] {os.path.join(root, directory)}")

        dirs[:] = sorted(
            d for d in dirs
            if d.lower() not in EXCLUDED_DIRECTORIES
        )

        for filename in sorted(files):

            extension = os.path.splitext(filename)[1].lower()

            # Skip excluded file extensions
            if extension in EXCLUDED_EXTENSIONS:
                print(f"[SKIPPED FILE] {filename}")
                total_skipped += 1
                continue

            full_path = os.path.join(root, filename)

            relative_path = os.path.relpath(
                full_path, source_folder
            )

            print(f"[PROCESSING] {relative_path}")

            try:
                with open(full_path, "rb") as f:
                    content = base64.b64encode(
                        f.read()
                    ).decode("ascii")

                bundle["files"].append({
                    "path": relative_path.replace("\\", "/"),
                    "content": content
                })

                total_processed += 1

                print(f"[COMPLETED] {relative_path}\n")

            except Exception as e:
                print(f"[ERROR] {relative_path}: {e}\n")

    # Write the final bundle
    print("Writing bundle file...")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2)

    print("\n========== CONVERSION SUMMARY ==========")
    print(f"Files successfully processed : {total_processed}")
    print(f"Files skipped                : {total_skipped}")
    print(f"Bundle output                : {output_file}")
    print("========================================")
    print("\nConversion completed!")


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("source")
    parser.add_argument("output")

    args = parser.parse_args()

    folder_to_bundle(args.source, args.output)
    
# USAGE
# python compress_to_json.py "<complete-path-to-folder>" "details.json"