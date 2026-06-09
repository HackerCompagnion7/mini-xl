<div align="center">

<img src="logo.png" alt="MINI-XL Logo" width="120" height="120" />

# Installation Guide

**MINI-XL v2.0 — Complete Setup Instructions**

</div>

---

## Table of Contents

- [Quick Install](#quick-install)
- [Termux (Android)](#termux-android)
- [Linux (Debian/Ubuntu)](#linux-debianubuntu)
- [Linux (Arch)](#linux-arch)
- [macOS](#macos)
- [From Source](#from-source)
- [From Wheel](#from-wheel)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

---

## Quick Install

The fastest way to install MINI-XL:

```bash
pip install git+https://github.com/HackerCompagnion7/mini-xl.git
```

After installation, the `mini-xl` command is available everywhere:

```bash
mini-xl
```

---

## Termux (Android)

### Step 1 — Install Termux

Download Termux from [F-Droid](https://f-droid.org/en/packages/com.termux/) (recommended) or the Google Play Store.

> **Important**: The F-Droid version is actively maintained. The Play Store version is outdated.

### Step 2 — Update Packages

```bash
pkg update && pkg upgrade -y
```

### Step 3 — Install Python

```bash
pkg install python -y
```

Verify the installation:

```bash
python --version
# Python 3.10.x or higher
```

### Step 4 — Grant Storage Access

```bash
termux-setup-storage
```

This creates the `~/storage/downloads` directory that MINI-XL scans by default. A permission dialog will appear — tap **Allow**.

> If the dialog doesn't appear, go to **Settings → Apps → Termux → Permissions → Storage** and enable it.

### Step 5 — Install MINI-XL

```bash
pip install git+https://github.com/HackerCompagnion7/mini-xl.git
```

### Step 6 — Run

```bash
mini-xl
```

### Optional — Add to PATH

If the `mini-xl` command is not found, add the pip bin directory to your PATH:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

---

## Linux (Debian/Ubuntu)

### Step 1 — Install Python & pip

```bash
sudo apt update
sudo apt install python3 python3-pip -y
```

### Step 2 — Install MINI-XL

```bash
pip3 install git+https://github.com/HackerCompagnion7/mini-xl.git
```

> If pip warns about externally-managed environment, use:
> ```bash
> pip3 install --user git+https://github.com/HackerCompagnion7/mini-xl.git
> # or
> pip3 install git+https://github.com/HackerCompagnion7/mini-xl.git --break-system-packages
> ```

### Step 3 — Create Downloads Directory

By default, MINI-XL scans `~/storage/downloads`. Create it if it doesn't exist:

```bash
mkdir -p ~/storage/downloads
```

### Step 4 — Run

```bash
mini-xl
```

---

## Linux (Arch)

### Step 1 — Install Python & pip

```bash
sudo pacman -Syu python python-pip
```

### Step 2 — Install MINI-XL

```bash
pip install git+https://github.com/HackerCompagnion7/mini-xl.git
```

### Step 3 — Run

```bash
mini-xl
```

---

## macOS

### Step 1 — Install Python via Homebrew

```bash
brew install python
```

### Step 2 — Install MINI-XL

```bash
pip3 install git+https://github.com/HackerCompagnion7/mini-xl.git
```

### Step 3 — Create Downloads Directory

```bash
mkdir -p ~/storage/downloads
```

### Step 4 — Run

```bash
mini-xl
```

---

## From Source

For development or customization:

```bash
git clone https://github.com/HackerCompagnion7/mini-xl.git
cd mini-xl

# Install in editable mode (changes are live)
pip install -e .

# Or install normally
pip install .
```

Build from source using the Makefile:

```bash
make setup      # install editable + verify
make build      # build .whl and .tar.gz
```

---

## From Wheel

If you have a `.whl` file:

```bash
pip install mini_xl-2.0.0-py3-none-any.whl
```

---

## Verification

After installation, verify everything works:

```bash
# Check package is installed
pip show mini-xl

# Check CLI is available
which mini-xl

# Run test suite
git clone https://github.com/HackerCompagnion7/mini-xl.git
cd mini-xl
python3 tests/test_mini_xl.py
```

### Quick Smoke Test

Create a test CSV file and convert it:

```bash
mkdir -p ~/storage/downloads
echo "name,age,city" > ~/storage/downloads/test.csv
echo "Alice,30,NYC" >> ~/storage/downloads/test.csv
echo "Bob,25,LA" >> ~/storage/downloads/test.csv

mini-xl
# Select [1] test.csv
# Check the generated .xlsx file
```

---

## Troubleshooting

### `mini-xl: command not found`

The pip bin directory is not in your PATH:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

Or run via Python:

```bash
python3 -m mini_xl
```

### `No module named 'mini_xl'`

Reinstall the package:

```bash
pip install git+https://github.com/HackerCompagnion7/mini-xl.git
```

### `No module named 'openpyxl'`

This should be installed automatically as a dependency. If not:

```bash
pip install openpyxl
```

### `Permission denied` when writing

Check write permissions on the output directory:

```bash
ls -la ~/storage/downloads/
# If needed:
chmod 755 ~/storage/downloads/
```

### `python3: command not found`

Install Python 3.10+:

```bash
# Termux
pkg install python

# Debian/Ubuntu
sudo apt install python3

# Arch
sudo pacman -S python
```

### `No compatible files found`

Ensure your files have one of these extensions: `.csv`, `.tsv`, `.json`, `.txt`

Check that the files are in `~/storage/downloads/`:

```bash
ls ~/storage/downloads/*.csv ~/storage/downloads/*.tsv ~/storage/downloads/*.json ~/storage/downloads/*.txt 2>/dev/null
```

### `termux-setup-storage` fails

1. Go to **Settings → Apps → Termux → Permissions**
2. Enable **Storage** permission
3. Run `termux-setup-storage` again

### JSON file not recognized

MINI-XL only supports **arrays of objects**. This is valid:

```json
[{"key": "value"}]
```

This is **not** supported:

```json
{"key": "value"}
```

### Large files are slow

Files over 100 MB will trigger a warning. For best performance, keep files under 100 MB.

---

## Uninstall

To remove MINI-XL:

```bash
pip uninstall mini-xl
```

---

<div align="center">

**Need more help?** Open an [Issue](https://github.com/HackerCompagnion7/mini-xl/issues)

</div>
