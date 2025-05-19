# Getting Started (README.txt)

This document describes the steps to clone the project from GitHub and run it locally. It assumes you have Git and Python 3.8+ installed.

---

## 1. Clone the Repository

```bash
git clone https://github.com/ZJayH/CSIT314.git
cd CSIT314
```

## 2. Create and Activate a Virtual Environment

### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If you encounter an execution policy error, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Configure Environment Variables

Create a `.env` file in the project root with the following content:

```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
```

Or set them in your shell:

```bash
# Windows PowerShell
$env:FLASK_APP="app.py"
$env:FLASK_ENV="development"
$env:SECRET_KEY="your-secret-key"

# macOS / Linux
export FLASK_APP=app.py
export FLASK_ENV=development
export SECRET_KEY=your-secret-key
```

## 5. Initialize the Database

```bash
flask db upgrade
```

## 6. (Optional) Seed Sample Data

```bash
python scripts/seed_accounts.py
python scripts/seed_service_categories.py
python scripts/seed_service_listings.py
python scripts/seed_confirmed_matches.py
```

## 7. Run the Development Server

```bash
flask run
```

Open your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000), which will redirect you to the login page.

## 8. Log In or Register

* Use one of the seeded accounts (e.g., `admin@1.com` / `123456`)
* Or click "Register" to create a new user account.

---

Congratulations! You have successfully set up and launched the Cleaner Matching System on your local machine.
