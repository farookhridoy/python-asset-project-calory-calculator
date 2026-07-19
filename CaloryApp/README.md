# CaloryApp - Calorie Counter

A Django-based web application to calculate daily calorie needs (BMR), track food intake, and manage nutrition goals.

## Live Repository

```
https://github.com/farookhridoy/python-asset-project-calory-calculator
```

---

## How to Set Up on a New PC

### Step 1: Clone the Repository

```bash
git clone https://github.com/farookhridoy/python-asset-project-calory-calculator.git
cd python-asset-project-calory-calculator
```

### Step 2: Create a Virtual Environment

```bash
# Windows (Command Prompt)
python -m venv v
v\Scripts\activate

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Windows (PowerShell)
python -m venv v
v\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv v
source v/bin/activate
```

You should see `(v)` in your terminal prompt, indicating the virtual environment is active.

### Step 3: Install Dependencies

```bash

python -m venv v --clear

\v\Scripts\activate

pip install django
```

### Step 4: Navigate to the Project Folder

```bash
cd CaloryApp
```

### Step 5: Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create a Superuser (Admin)

```bash
python manage.py createsuperuser
```

Use these credentials when prompted:

| Field    | Value              |
|----------|--------------------|
| Username | `admin`            |
| Email    | `admin@example.com`|
| Password | `1234`             |

### Step 7: Run the Development Server

```bash
python manage.py runserver
```

### Step 8: Open in Browser

```
http://127.0.0.1:8000/
```

---

## App Features & Pages

| URL | Page | Description |
|-----|------|-------------|
| `/` | Home | Landing page with app overview |
| `/about/` | About | About the app and team |
| `/register/` | Register | Create a new account |
| `/login/` | Login | Sign in with username/password |
| `/profile/` | Profile | Enter age, gender, height, weight |
| `/dashboard/` | Dashboard | **Main page** — track calories, add/edit/delete food entries |
| `/admin/` | Admin Panel | Manage users and data (superuser only) |

---

## How to Use the App

1. **Register** an account at `/register/`
2. **Login** at `/login/`
3. **Fill your profile** (name, age, gender, height, weight) — the app calculates your **BMR** (Basal Metabolic Rate)
4. **Dashboard** shows:
   - Required calories per day (BMR)
   - Calories consumed today
   - Remaining calories
5. **Add food entries** using the inline form
6. **Edit or delete** entries using the buttons in the table — all within the same page (no reload)

---

## BMR Formulas Used

| Gender | Formula |
|--------|---------|
| Male | `66.47 + (13.75 × weight in kg) + (5.003 × height in cm) - (6.755 × age)` |
| Female | `655.1 + (9.563 × weight in kg) + (1.850 × height in cm) - (4.676 × age)` |

---

## Project Structure

```
CaloryApp/
├── CaloryApp/                # Project settings & URLs
│   ├── settings.py
│   ├── urls.py
│   └── views.py
├── Backend/                  # Main app
│   ├── models.py             # CalorieProfile & FoodEntry
│   ├── views.py              # All view functions
│   ├── forms.py              # Django forms
│   ├── admin.py              # Admin registration
│   └── migrations/
├── templates/                # HTML templates
│   ├── index.html
│   ├── about.html
│   ├── login.html
│   ├── register.html
│   ├── profile.html
│   └── dashboard.html        # Single-page app with modals
├── db.sqlite3                # Database
├── manage.py                 # Django management script
└── README.md
```

---

## Useful Commands

| Command | Purpose |
|---------|---------|
| `python manage.py runserver` | Start development server |
| `python manage.py makemigrations` | Create database migration files |
| `python manage.py migrate` | Apply migrations to database |
| `python manage.py createsuperuser` | Create an admin user |
| `python manage.py check` | Check for project issues |
| `python manage.py shell` | Open Django interactive shell |

---

## Tech Stack

- **Backend:** Python, Django 5.2
- **Frontend:** HTML, CSS, JavaScript (vanilla)
- **Database:** SQLite3
- **Authentication:** Django built-in auth
