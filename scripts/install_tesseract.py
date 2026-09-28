#!/usr/bin/env python3
import subprocess
import sys


def main() -> None:
    print("Setting up Tesseract OCR...")

    if sys.platform == "win32":
        print("Detected Windows.")
        installed = False
        if shutil.which("winget"):
            print(
                "Running: winget install -e --id UB-Mannheim.TesseractOCR --source winget --accept-package-agreements --accept-source-agreements"
            )
            result = subprocess.run(
                [
                    "winget",
                    "install",
                    "-e",
                    "--id",
                    "UB-Mannheim.TesseractOCR",
                    "--source",
                    "winget",
                    "--accept-package-agreements",
                    "--accept-source-agreements",
                ],
                capture_output=True,
                text=True,
            )
            # winget returns a non-zero exit code if it's already installed or no upgrade is available
            if result.returncode == 0 or "No available upgrade found" in result.stdout:
                installed = True
            else:
                print(f"winget output: {result.stdout}")
                print(f"winget error: {result.stderr}")

        if not installed and shutil.which("choco"):
            print("Trying Chocolatey: choco install tesseract --no-progress -y")
            result = subprocess.run(
                ["choco", "install", "tesseract", "--no-progress", "-y"],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                installed = True
            else:
                print(f"choco output: {result.stdout}")
                print(f"choco error: {result.stderr}")

        if installed:
            print(
                "Tesseract installed (or already installed) successfully to C:\\Program Files\\Tesseract-OCR\\"
            )
        else:
            print(
                "Warning: Tesseract installation failed or package manager unavailable. OCR tests will be skipped."
            )

    elif sys.platform == "darwin":
        print("Detected macOS.")
        if shutil.which("brew"):
            print("Running: brew install tesseract")
            subprocess.run(["brew", "install", "tesseract"], check=True)
            print("Tesseract installed successfully.")
        else:
            print(
                "Homebrew not found. Please install from https://brew.sh/ or install Tesseract manually."
            )
            sys.exit(1)

    elif sys.platform.startswith("linux"):
        print("Detected Linux.")
        if shutil.which("apt-get"):
            print("Running: sudo apt-get update && sudo apt-get install -y tesseract-ocr")
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y", "tesseract-ocr"], check=True)
            print("Tesseract installed successfully.")
        else:
            print(
                "apt-get not found. Please use your package manager (e.g., yum, pacman, apk) to install `tesseract-ocr`."
            )
            sys.exit(1)

    else:
        print(f"Unsupported OS: {sys.platform}. Please install Tesseract manually.")
        sys.exit(1)


if __name__ == "__main__":
    import shutil

    main()
