
import os

EXCLUDED_EXTENSIONS = {
    ".onnx",
    ".pkl",
    ".pptx",
    ".xlsx",
    ".exe",
    ".pfx"
}

EXCLUDED_FILENAMES = {
    ".gitignore",
    ".terraform.lock.hcl"
}

EXCLUDED_DIRECTORIES = {
    ".git",
    ".terraform"
}


def folder_to_text(source_folder, output_file):

    total_processed = 0
    total_skipped = 0

    print("\nStarting folder conversion...\n")

    with open(output_file, "w", encoding="utf-8") as output:

        for root, dirs, files in os.walk(source_folder):

            # Exclude specified directories
            dirs[:] = sorted(
                d for d in dirs
                if d.lower() not in EXCLUDED_DIRECTORIES
            )

            for filename in sorted(files):

                # Check complete filename exclusions
                if filename.lower() in EXCLUDED_FILENAMES:
                    print(f"[SKIPPED - FILENAME] {filename}")
                    total_skipped += 1
                    continue

                # Check file extension exclusions
                extension = os.path.splitext(filename)[1].lower()

                if extension in EXCLUDED_EXTENSIONS:
                    print(f"[SKIPPED - EXTENSION] {filename}")
                    total_skipped += 1
                    continue

                full_path = os.path.join(root, filename)

                relative_path = os.path.relpath(
                    full_path, source_folder
                ).replace("\\", "/")

                print(f"[PROCESSING] {relative_path}")

                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    output.write(
                        f"\n===== FILE: {relative_path} =====\n\n"
                    )

                    output.write(content)
                    output.write("\n\n===== END FILE =====\n")

                    total_processed += 1

                    print(f"[COMPLETED] {relative_path}")

                except (UnicodeDecodeError, OSError) as e:
                    print(f"[SKIPPED - NOT TEXT] {relative_path}: {e}")
                    total_skipped += 1

    print("\n========== SUMMARY ==========")
    print(f"Files processed : {total_processed}")
    print(f"Files skipped   : {total_skipped}")
    print(f"Output file     : {output_file}")
    print("=============================")


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("source")
    parser.add_argument("output")

    args = parser.parse_args()

    folder_to_text(args.source, args.output)