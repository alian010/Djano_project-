from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Signup view
def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Password check
        if password1 != password2:
            return render(request, "signin.html", {"msg": "Passwords do not match!"})

        # Username check
        if User.objects.filter(username=username).exists():
            return render(request, "signin.html", {"msg": "Username already exists!"})

        # Email check (optional)
        if User.objects.filter(email=email).exists():
            return render(request, "signin.html", {"msg": "Email already registered!"})

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Account created successfully! Please login.")
        return redirect("/login")

    return render(request, "signin.html")


# Login view
def loginn(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user,{"us":user.username})
            return redirect("/todo", permanent=True)
        else:
            return render(request, "login.html", {"msg": "Invalid credentials!"})

    return render(request, "login.html")


# Todo page (after login)
def todo(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    return render(request, "todo.html")


# Logout view
def log_out(request):
    logout(request)
    return redirect("login")
