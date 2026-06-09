<div align="center">

<img src="logo.png" alt="MINI-XL Logo" width="120" height="120" />

# Installation Guide

**MINI-XL v2.0 — Complete Setup Instructions**

</div>

---

## Table of Contents

- [Requirements](#requirements)
- [Termux (Android)](#termux-android)
- [Linux (Debian/Ubuntu)](#linux-debianubuntu)
- [Linux (Arch)](#linux-arch)
- [macOS](#macos)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

---

## Requirements

| Requirement | Minimum Version |
|-------------|----------------|
| Python | 3.10+ |
| pip | Latest |
| Disk space | ~5 MB (project + openpyxl) |

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

### Step 5 — Clone MINI-XL

```bash
cd ~/storage/downloads
git clone https://github.com/HackerCompagnion7/mini-xl.git
cd mini-xl
```

### Step 6 — Install Dependencies

```bash
pip install openpyxl
```

Or use the Makefile:

```bash
make setup
```

### Step 7 — Run

```bash
python main.py
```

Or:

```bash
make run
```

### Optional — Add to PATH

To run `mini-xl` from anywhere:

```bash
echo 'alias mini-xl="python ~/storage/downloads/mini-xl/main.py"' >> ~/.bashrc
source ~/.bashrc
```

Then simply type:

```bash
mini-xl
```

---

## Linux (Debian/Ubuntu)

### Step 1 — Install Python & pip

```bash
sudo apt update
sudo apt install python3 python3-pip -y
```

### Step 2 — Clone MINI-XL

```bash
git clone https://github.com/HackerCompagnion7/mini-xl.git
cd mini-xl
```

### Step 3 — Install Dependencies

```bash
pip3 install openpyxl
```

Or with the Makefile:

```bash
make setup
```

> If pip warns about externally-managed environment, use:
> ```bash
> pip3 install --user openpyxl
> # or
> pip3 install openpyxl --break-system-packages
> ```

### Step 4 — Create Downloads Directory

By default, MINI-XL scans `~/storage/downloads`. Create it if it doesn't exist:

```bash
mkdir -p ~/storage/downloads
```

Or set a custom directory (see [Custom Directory](#custom-directory)).

### Step 5 — Run

```bash
python3 main.py
```

### Optional — System-wide Alias

```bash
echo 'alias mini-xl="python3 /path/to/mini-xl/main.py"' >> ~/.bashrc
source ~/.bashrc
```

---

## Linux (Arch)

### Step 1 — Install Python & pip

```bash
sudo pacman -Syu python python-pip
```

### Step 2 — Clone & Install

```bash
git clone https://github.com/HackerCompagnion7/mini-xl.git
cd mini-xl
pip install openpyxl
```

### Step 3 — Run

```bash
python main.py
```

---

## macOS

### Step 1 — Install Python via Homebrew

```bash
brew install python
```

### Step 2 — Clone & Install

```bash
git clone https://github.com/HackerCompagnion7/mini-xl.git
cd mini-xl
pip3 install openpyxl
```

### Step 3 — Create Downloads Directory

```bash
mkdir -p ~/storage/downloads
```

### Step 4 — Run

```bash
python3 main.py
```

---

## Verification

After installation, verify everything works:

```bash
make check
```

This runs:
1. **Compilation check** — All modules compile without errors
2. **Lint check** — Static analysis passes
3. **Test suite** — All 34 automated tests pass

Expected output:

```
  ✔ utils.py
  ✔ scanner.py
  ✔ menu.py
  ✔ analyseur.py
  ✔ generateur.py
  ✔ main.py
  Compilation OK ✔

  Results: 34/34 passed, 0 failed
```

### Quick Smoke Test

Create a test CSV file and convert it:

```bash
echo "name,age,city" > ~/storage/downloads/test.csv
echo "Alice,30,NYC" >> ~/storage/downloads/test.csv
echo "Bob,25,LA" >> ~/storage/downloads/test.csv

python3 main.py
# Select [1] test.csv
# Check the generated .xlsx file
```

---

## Custom Directory

MINI-XL defaults to `~/storage/downloads`. To use a custom directory:

Edit `utils.py` and change `REP_DOWNLOADS`:

```python
REP_DOWNLOADS: str = "/your/custom/path"
```

Or create a symlink:

```bash
ln -s /your/custom/path ~/storage/downloads
```

---

## Troubleshooting

### `No module named 'openpyxl'`

```bash
pip install openpyxl
# or
pip3 install openpyxl --user
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

<div align="center">

**Need more help?** Open an [Issue](https://github.com/HackerCompagnion7/mini-xl/issues)

</div>
