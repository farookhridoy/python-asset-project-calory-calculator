from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from .forms import RegistrationForm, ProfileForm, FoodEntryForm
from .models import CalorieProfile, FoodEntry

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')

@login_required
def profile(request):
    try:
        profile = CalorieProfile.objects.get(user=request.user)
    except CalorieProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            p = form.save(commit=False)
            p.user = request.user
            p.save()
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form})

@login_required
def dashboard(request):
    try:
        profile = CalorieProfile.objects.get(user=request.user)
    except CalorieProfile.DoesNotExist:
        return redirect('profile')

    today = timezone.now().date()
    food_entries = FoodEntry.objects.filter(user=request.user, date=today)
    total_consumed = food_entries.aggregate(Sum('calories'))['calories__sum'] or 0
    required_calories = profile.bmr()

    if request.method == 'POST':
        form = FoodEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.date = timezone.now().date()
            entry.save()
            return redirect('dashboard')
    else:
        form = FoodEntryForm()

    context = {
        'profile': profile,
        'required_calories': round(required_calories, 2),
        'total_consumed': round(total_consumed, 2),
        'remaining': round(required_calories - total_consumed, 2),
        'food_entries': food_entries,
        'form': form,
    }
    return render(request, 'dashboard.html', context)

@login_required
def edit_food(request, entry_id):
    entry = FoodEntry.objects.get(id=entry_id, user=request.user)
    if request.method == 'POST':
        form = FoodEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = FoodEntryForm(instance=entry)
    return render(request, 'edit_food.html', {'form': form, 'entry': entry})

@login_required
def delete_food(request, entry_id):
    entry = FoodEntry.objects.get(id=entry_id, user=request.user)
    if request.method == 'POST':
        entry.delete()
        return redirect('dashboard')
    return render(request, 'delete_food.html', {'entry': entry})

def user_logout(request):
    logout(request)
    return redirect('login')
