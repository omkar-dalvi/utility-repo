
import os
import re
import argparse

def text_to_folder(input_file, output_folder):

    total_processed = 0
    total_failed = 0

    print("\nStarting folder reconstruction...")
    print(f"Input file: {input_file}")
    print(f"Output folder: {output_folder}\n")

    # Create output directory
    os.makedirs(output_folder, exist_ok=True)

    # Resolve output root for security validation
    root = os.path.realpath(output_folder)

    # Read the complete text bundle
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Identify file sections
    pattern = re.compile(
        r"===== FILE: (.*?) =====\r?\n(.*?)\r?\n===== END FILE =====",
        re.DOTALL
    )

    matches = list(pattern.finditer(content))

    print(f"Total files found: {len(matches)}\n")

    # Reconstruct each file
    for match in matches:

        relative_path = match.group(1)
        file_content = match.group(2)

        print(f"[PROCESSING] {relative_path}")

        try:
            # Normalize path separators
            relative_path = relative_path.replace("\\", "/")

            # Construct destination path
            destination = os.path.realpath(
                os.path.join(root, relative_path)
            )

            # Security check: prevent directory traversal
            if os.path.commonpath([root, destination]) != root:
                raise ValueError("Invalid file path detected")

            # Create parent directories
            parent_directory = os.path.dirname(destination)

            os.makedirs(parent_directory, exist_ok=True)

            # Write file content
            with open(destination, "w", encoding="utf-8", newline="") as f:
                f.write(file_content)

            total_processed += 1

            print(f"[COMPLETED] {relative_path}\n")

        except Exception as e:

            total_failed += 1

            print(f"[ERROR] {relative_path}: {e}\n")

    # Display summary
    print("\n========== RECONSTRUCTION SUMMARY ==========")
    print(f"Total files found       : {len(matches)}")
    print(f"Files successfully made : {total_processed}")
    print(f"Files failed            : {total_failed}")
    print(f"Output folder           : {output_folder}")
    print("============================================")

    print("\nFolder reconstruction completed!")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Reconstruct folder from plain text bundle"
    )

    parser.add_argument(
        "source",
        help="Path to the plain text bundle"
    )

    parser.add_argument(
        "output",
        help="Destination folder"
    )

    args = parser.parse_args()

    text_to_folder(args.source, args.output)