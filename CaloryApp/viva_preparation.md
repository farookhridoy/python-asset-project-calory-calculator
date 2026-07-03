# CaloryApp - Viva Preparation Guide

## Folder Structure

```
D:\python-server\caloriapp\                   # Project root
│
├── CaloryApp\                                # Django Project Folder
│   ├── CaloryApp\                            # Project Configuration Package
│   │   ├── __init__.py
│   │   ├── settings.py                       # All project settings
│   │   ├── urls.py                           # URL routing (project-level)
│   │   ├── views.py                          # Home & About views
│   │   ├── wsgi.py                           # WSGI config for deployment
│   │   └── asgi.py                           # ASGI config
│   │
│   ├── Backend\                              # Django App (calorie logic)
│   │   ├── __init__.py
│   │   ├── admin.py                          # Register models to admin panel
│   │   ├── apps.py                           # App configuration
│   │   ├── forms.py                          # Django Form classes
│   │   ├── models.py                         # Database models
│   │   ├── views.py                          # All view functions
│   │   ├── tests.py                          # Test stubs
│   │   └── migrations\                       # Database migration files
│   │       ├── __init__.py
│   │       ├── 0001_initial.py
│   │       └── 0002_alter_foodentry_date.py
│   │
│   ├── templates\                            # HTML templates
│   │   ├── index.html                        # Home page
│   │   ├── about.html                        # About page
│   │   ├── login.html                        # Login page
│   │   ├── register.html                     # Registration page
│   │   ├── profile.html                      # User profile form
│   │   └── dashboard.html                    # Main dashboard (SPA)
│   │
│   ├── db.sqlite3                            # SQLite database file
│   └── manage.py                             # Django management script
│
└── v\                                        # Python virtual environment
```

---

## SECTION 1: Project Creation & Commands

### Q1: How was the Django project created?

```bash
django-admin startproject CaloryApp
```

### Q2: How was the Django app (Backend) created?

```bash
cd CaloryApp
python manage.py startapp Backend
```

### Q3: How do you run the development server?

```bash
python manage.py runserver
# Default: http://127.0.0.1:8000/

# Custom port:
python manage.py runserver 0.0.0.0:8000
```

### Q4: How do you create database migrations?

```bash
python manage.py makemigrations
python manage.py migrate
```

### Q5: How do you create a superuser?

```bash
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: 1234
```

### Q6: What is the virtual environment setup?

```bash
# Create
python -m venv v

# Activate (Windows)
v\Scripts\activate

# Activate (PowerShell)
v\Scripts\Activate.ps1

# Install Django
pip install django
```

### Q7: What commands were used to generate the database tables?

```bash
python manage.py makemigrations    # Generate migration files
python manage.py migrate            # Apply migrations to database
```

### Q8: How do you check for project issues?

```bash
python manage.py check
```

---

## SECTION 2: Settings (settings.py)

### Q9: What is BASE_DIR?

**Answer:** `BASE_DIR = Path(__file__).resolve().parent.parent`

- `__file__` = path to settings.py
- `.resolve()` = full absolute path
- `.parent.parent` = goes up 2 levels from `CaloryApp/CaloryApp/settings.py` to `CaloryApp/`

**Result:** `BASE_DIR = D:\python-server\caloriapp\CaloryApp`

### Q10: Which apps are installed?

```python
INSTALLED_APPS = [
    'django.contrib.admin',          # Admin panel
    'django.contrib.auth',           # Authentication system
    'django.contrib.contenttypes',   # Content types framework
    'django.contrib.sessions',       # Session management
    'django.contrib.messages',       # Flash messages
    'django.contrib.staticfiles',    # Static file serving
    'Backend',                       # OUR CUSTOM APP (calorie logic)
]
```

**Viva:** Why did we add `'Backend'`? → So Django knows about our app's models, migrations, templates, etc.

### Q11: What is the ROOT_URLCONF setting?

```python
ROOT_URLCONF = 'CaloryApp.urls'
```

**Answer:** Tells Django to look at `CaloryApp/urls.py` for the main URL configuration.

### Q12: How are templates configured?

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],      # <-- Our template folder
        'APP_DIRS': True,                        # Also search in app/templates/
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

**Viva:** What is `'DIRS': [BASE_DIR / 'templates']`?
- It tells Django to look for HTML files in `CaloryApp/templates/` directory.
- `BASE_DIR / 'templates'` = `D:\python-server\caloriapp\CaloryApp\templates`

**Viva:** What are context processors?
- Functions that add variables to ALL templates automatically (like `request` object, `user` object, messages).

### Q13: What database is used?

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Answer:** SQLite3 database stored at `CaloryApp/db.sqlite3`.

**Viva:** How would you change to MySQL/PostgreSQL?
- Change `ENGINE` to `'django.db.backends.mysql'` or `'django.db.backends.postgresql'`
- Add `'USER'`, `'PASSWORD'`, `'HOST'`, `'PORT'` keys.

### Q14: What is `LOGIN_URL` and why was it added?

```python
LOGIN_URL = '/login/'
```

**Answer:** When a user tries to access a `@login_required` page (like dashboard/profile), Django redirects them to this URL. Without this, it would try to redirect to `/accounts/login/` (default) which doesn't exist.

### Q15: What are the timezone settings?

```python
TIME_ZONE = 'UTC'
USE_TZ = True
```

**Viva:** Why was `auto_now_add=True` removed from FoodEntry.date?
- `auto_now_add` uses `datetime.date.today()` (local system date), but our view queries use `timezone.now().date()` (UTC date). This caused entries to be saved with a different date than what was queried.

---

## SECTION 3: Model Integration & Setup

### Q16: What models did we create?

**Model 1: CalorieProfile**
```python
class CalorieProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[('Male','Male'),('Female','Female')])
    height = models.FloatField(help_text="Height in cm")
    weight = models.FloatField(help_text="Weight in kg")

    def bmr(self):
        if self.gender == 'Male':
            return 66.47 + (13.75 * self.weight) + (5.003 * self.height) - (6.755 * self.age)
        else:
            return 655.1 + (9.563 * self.weight) + (1.850 * self.height) - (4.676 * self.age)
```

**Model 2: FoodEntry**
```python
class FoodEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=200)
    calories = models.FloatField()
    date = models.DateField()   # date set manually in view (not auto_now_add)
```

### Q17: How do you register models in admin?

```python
# admin.py
from django.contrib import admin
from .models import CalorieProfile, FoodEntry

admin.site.register(CalorieProfile)
admin.site.register(FoodEntry)
```

**Viva:** Why register in admin?
- So we can view/manage data from the admin panel at `/admin/`.

### Q18: What is the relationship between User and CalorieProfile?

- **OneToOneField** — Each user has ONE profile. Each profile belongs to ONE user.
- `on_delete=models.CASCADE` — If the User is deleted, their profile is also deleted.

### Q19: What is the relationship between User and FoodEntry?

- **ForeignKey** — One user can have MANY food entries.
- `on_delete=models.CASCADE` — If the User is deleted, all their food entries are deleted.

---

## SECTION 4: URL Patterns

### Q20: List all URL patterns and their purpose.

```python
urlpatterns = [
    path('admin/', admin.site.urls),                           # Admin panel
    path('', home, name='home'),                               # Home page
    path('about/', about, name='about'),                       # About page
    path('register/', backend_views.register, name='register'),# Registration
    path('login/', backend_views.user_login, name='login'),    # Login
    path('logout/', backend_views.user_logout, name='logout'), # Logout
    path('profile/', backend_views.profile, name='profile'),   # User profile form
    path('dashboard/', backend_views.dashboard, name='dashboard'),# Dashboard page
    path('api/dashboard/', backend_views.api_dashboard, name='api_dashboard'), # JSON data
    path('api/add/', backend_views.add_food, name='add_food'),         # AJAX add
    path('api/edit/<int:entry_id>/', backend_views.edit_food, name='edit_food'),  # AJAX edit
    path('api/delete/<int:entry_id>/', backend_views.delete_food, name='delete_food'), # AJAX delete
]
```

**Viva:** Why do we have `/api/` routes?
- The dashboard is a Single Page Application (SPA). All CRUD operations happen via JavaScript `fetch()` calls to these API endpoints, returning JSON instead of HTML.

---

## SECTION 5: View Functions

### Q21: List all views and their purpose.

| View | URL | Auth? | Method | Purpose |
|------|-----|-------|--------|---------|
| `home` | `/` | No | GET | Render index.html |
| `about` | `/about/` | No | GET | Render about.html |
| `register` | `/register/` | No | GET/POST | Registration form + create user |
| `user_login` | `/login/` | No | GET/POST | Login form + authenticate |
| `user_logout` | `/logout/` | No | GET | Logout + redirect to login |
| `profile` | `/profile/` | Yes | GET/POST | Collect age/gender/height/weight |
| `dashboard` | `/dashboard/` | Yes | GET | Render dashboard.html (SPA shell) |
| `api_dashboard` | `/api/dashboard/` | Yes | GET | JSON: entries + stats |
| `add_food` | `/api/add/` | Yes | POST | Add food entry (JSON response) |
| `edit_food` | `/api/edit/<id>/` | Yes | POST | Edit food entry (JSON response) |
| `delete_food` | `/api/delete/<id>/` | Yes | POST | Delete food entry (JSON response) |

### Q22: What does `@login_required` do?

**Answer:** If the user is NOT logged in, redirect them to `LOGIN_URL` (`/login/`) before allowing access to the view.

### Q23: What is the flow from login to dashboard?

1. User submits username/password
2. `user_login` view calls `authenticate()` → `login()`
3. Redirect to `dashboard` URL
4. `dashboard` view loads profile, renders `dashboard.html`
5. JavaScript on page calls `/api/dashboard/` to load stats + entries
6. All add/edit/delete happens via AJAX (no page reload)

### Q24: What is the BMR formula used?

```python
# Male:
BMR = 66.47 + (13.75 × weight_kg) + (5.003 × height_cm) - (6.755 × age)

# Female:
BMR = 655.1 + (9.563 × weight_kg) + (1.850 × height_cm) - (4.676 × age)
```

---

## SECTION 6: Forms

### Q25: What forms did we create?

```python
class RegistrationForm(UserCreationForm):
    # Fields: username, email, password1, password2
    # Used for user registration

class ProfileForm(forms.ModelForm):
    # Model: CalorieProfile
    # Fields: name, age, gender, height, weight
    # Used to collect user body metrics

class FoodEntryForm(forms.ModelForm):
    # Model: FoodEntry
    # Fields: item_name, calories
    # Used for add/edit food entries
```

---

## SECTION 7: Templates

### Q26: Which templates exist and where are they stored?

All templates are in `CaloryApp/templates/`:

| Template | Purpose |
|----------|---------|
| `index.html` | Home/Landing page |
| `about.html` | About the app |
| `login.html` | Login form |
| `register.html` | Registration form |
| `profile.html` | User details form (age, gender, height, weight) |
| `dashboard.html` | **SPA Dashboard** — contains modals + JavaScript |

### Q27: How does the dashboard work as a Single Page Application?

- **No page reload** for any CRUD operation
- Modals (popups) for edit and delete
- JavaScript `fetch()` API calls to `/api/` endpoints
- Stats and entries table refresh dynamically via `loadDashboard()`

```
User Action     →    JavaScript     →    Django API     →    DB     →    UI Update
──────────────────────────────────────────────────────────────────────────────
Click "Add"     →    addEntry()     →    POST /api/add/  →  INSERT   →  loadDashboard()
Click "Edit"    →    openEdit()     →    Show modal                       
Click "Save"    →    saveEdit()     →    POST /api/edit/ →  UPDATE   →  loadDashboard()
Click "Delete"  →    openDelete()   →    Show modal                       
Click "Confirm" →    confirmDelete()->   POST /api/delete/→ DELETE   →  loadDashboard()
```

---

## SECTION 8: Database & Migrations

### Q28: How many migrations were created?

```
0001_initial.py    →  Created CalorieProfile and FoodEntry models
0002_...date.py    →  Changed FoodEntry.date from auto_now_add to regular DateField
```

### Q29: What migration command would you run if you change a model?

```bash
python manage.py makemigrations   # Create migration file
python manage.py migrate           # Apply to database
```

### Q30: How can you view the database content?

```python
# Via Django shell:
python manage.py shell
>>> from Backend.models import FoodEntry, CalorieProfile
>>> FoodEntry.objects.all()
>>> CalorieProfile.objects.all()

# Via admin panel:
# Go to http://127.0.0.1:8000/admin/ and login with superuser
```

---

## SECTION 9: Quick Reference — All Commands

| Task | Command |
|------|---------|
| Create project | `django-admin startproject CaloryApp` |
| Create app | `python manage.py startapp Backend` |
| Run server | `python manage.py runserver` |
| Make migrations | `python manage.py makemigrations` |
| Apply migrations | `python manage.py migrate` |
| Check project | `python manage.py check` |
| Create superuser | `python manage.py createsuperuser` |
| Django shell | `python manage.py shell` |
| Activate venv | `v\Scripts\activate` or `v\Scripts\Activate.ps1` |
| Install Django | `pip install django` |

---

## SECTION 10: Common Viva Questions

### Q: What did you build?
**A:** A Calorie Counter web app. Users register, enter their age/gender/height/weight, and the app calculates their daily BMR (basal metabolic rate). Users can log food items they eat each day, see total consumed calories, and know how many remaining calories they can eat.

### Q: What is the folder structure?
**A:** `CaloryApp/` (project) contains `CaloryApp/` (settings/urls), `Backend/` (models/views/forms), and `templates/` (HTML files).

### Q: What database did you use?
**A:** SQLite3 — Django's default. File is `db.sqlite3`.

### Q: How did you handle login/logout?
**A:** Used Django's built-in `authenticate()`, `login()`, `logout()` functions with session-based auth. `@login_required` decorator protects private pages.

### Q: How did you handle CSRF protection?
**A:** Django's `CsrfViewMiddleware` is enabled. The JavaScript reads the `csrftoken` cookie and sends it in the `X-CSRFToken` header with every fetch request. Templates use `{% csrf_token %}` for regular forms.

### Q: How did you implement the BMR calculation?
**A:** As a method on the `CalorieProfile` model (`models.py:16-20`). Male and female formulas from the specification sheet.

### Q: Why did entries not appear on the dashboard initially?
**A:** `DateField(auto_now_add=True)` uses `datetime.date.today()` (local date), but the dashboard query used `timezone.now().date()` (UTC date). Since the system timezone was ahead of UTC, entries were saved with tomorrow's date and never matched today's query. Fixed by setting the date explicitly in the view.

### Q: How do you add/edit/delete food entries?
**A:** All through the dashboard page — no navigation needed. Inline form to add, modal popups to edit or delete. JavaScript `fetch()` calls to `/api/add/`, `/api/edit/<id>/`, `/api/delete/<id>/` endpoints.

### Q: What is the difference between OneToOneField and ForeignKey?
**A:** `OneToOneField` → each user has exactly one profile (unique). `ForeignKey` → each user can have many food entries (one-to-many).
