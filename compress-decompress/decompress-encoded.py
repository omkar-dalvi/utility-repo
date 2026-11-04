
import os
import json
import base64

def bundle_to_folder(bundle_file, output_folder):

    # Initialize counters
    total_processed = 0
    total_failed = 0

    print("\nStarting folder reconstruction...")
    print(f"Input bundle: {bundle_file}")
    print(f"Output folder: {output_folder}\n")

    # Read the bundle JSON file
    print("[READING] Loading bundle file...")

    with open(bundle_file, "r", encoding="utf-8") as f:
        bundle = json.load(f)

    # Validate bundle format
    if bundle.get("format") != "folder-bundle":
        raise ValueError("Invalid bundle format")

    print("[VALIDATED] Bundle format is valid.")

    # Create the output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    root = os.path.realpath(output_folder)

    # Get the list of files stored in the bundle
    files = bundle.get("files", [])

    print(f"\nTotal files to restore: {len(files)}\n")

    # Process each file in the bundle
    for file_entry in files:

        relative_path = file_entry["path"]

        print(f"[PROCESSING] {relative_path}")

        try:
            # Construct the destination file path
            destination = os.path.realpath(
                os.path.join(root, relative_path)
            )

            # Security check: prevent directory traversal
            if os.path.commonpath([root, destination]) != root:
                raise ValueError("Invalid file path detected")

            # Create parent directories if they don't exist
            parent_directory = os.path.dirname(destination)

            os.makedirs(parent_directory, exist_ok=True)

            # Decode the Base64 file content
            content = base64.b64decode(
                file_entry["content"],
                validate=True
            )

            # Write the original file content
            with open(destination, "wb") as f:
                f.write(content)

            total_processed += 1

            print(f"[COMPLETED] {relative_path}\n")

        except Exception as e:

            total_failed += 1

            print(f"[ERROR] {relative_path}: {e}\n")

    # Display final reconstruction summary
    print("\n========== RECONSTRUCTION SUMMARY ==========")
    print(f"Total files in bundle       : {len(files)}")
    print(f"Files successfully restored : {total_processed}")
    print(f"Files failed                : {total_failed}")
    print(f"Output folder               : {output_folder}")
    print("============================================")
    print("\nFolder reconstruction completed!")


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(
        description="Reconstruct a folder from a JSON bundle"
    )

    parser.add_argument(
        "bundle",
        help="Complete path to the JSON bundle file"
    )

    parser.add_argument(
        "output",
        help="Complete path to the destination folder"
    )

    args = parser.parse_args()

    bundle_to_folder(args.bundle, args.output)

# USAGE
# python decompress-encoded.py  "details.json" "foldername"