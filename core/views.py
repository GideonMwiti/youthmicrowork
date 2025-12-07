from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def home(request):
    return render(request, "home.html")

def tasks(request):
    task_list = ["Data Entry", "Surveys", "AI Training", "Research", "Content Writing", "Image Annotation"]
    return render(request, "tasks.html", {"task_list": task_list})

def training(request):
    return render(request, "training.html")

def register(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        role = request.POST.get("role", "microworker")  

        if not full_name or not email or not password1:
            messages.error(request, "Please fill in all required fields.")
            return redirect("register")
        
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("register")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("register")
        
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("register")

        try:
            
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password1,
                first_name=full_name  
            )
            
            if role == "admin":
                user.is_staff = True
                user.save()
                messages.success(request, "Admin account created successfully! Please login.")
            else:
                messages.success(request, "Account created successfully! Please login.")
            
            return redirect("login")
            
        except Exception as e:
            messages.error(request, f"Error creating account: {str(e)}")
            return redirect("register")

    return render(request, "register.html")

def login_view(request):
   
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("admin_dashboard")
        return redirect("dashboard")
    
    if request.method == "POST":
        email = request.POST.get("username")  
        password = request.POST.get("password")
        
        if not email or not password:
            messages.error(request, "Please enter both email and password.")
            return render(request, "login.html")
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name}!")
            
            if user.is_staff:
                return redirect("admin_dashboard")
            else:
                return redirect("dashboard")
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, "login.html")
    
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("home")

@login_required
def user_dashboard(request):
    if request.user.is_staff:
        return redirect("admin_dashboard")
    return render(request, "user_dashboard.html")

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        messages.warning(request, "Access denied. Admin privileges required.")
        return redirect("dashboard")
    return render(request, "admin_dashboard.html")

@login_required
def generate_cv(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "Anonymous")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        location = request.POST.get("location", "")
        summary = request.POST.get("summary", "")
        experience = request.POST.get("experience", "")
        education = request.POST.get("education", "")
        skills = request.POST.get("skills", "")

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{full_name}_CV.pdf"'

        p = canvas.Canvas(response, pagesize=A4)
        width, height = A4
        y = height - 50

        def write(text, spacing=18):
            nonlocal y
            if y < 50:
                p.showPage()
                y = height - 50
            p.drawString(40, y, text)
            y -= spacing

        p.setFont("Helvetica-Bold", 16)
        write(full_name)

        p.setFont("Helvetica", 10)
        if email: write(f"Email: {email}")
        if phone: write(f"Phone: {phone}")
        if location: write(f"Location: {location}")
        y -= 10

        if summary:
            p.setFont("Helvetica-Bold", 14)
            write("Professional Summary")
            p.setFont("Helvetica", 10)
            for line in summary.split("\n"):
                write(line)
            y -= 10

        if experience:
            p.setFont("Helvetica-Bold", 14)
            write("Work Experience")
            p.setFont("Helvetica", 10)
            for line in experience.split("\n"):
                write(line)
            y -= 10

        if education:
            p.setFont("Helvetica-Bold", 14)
            write("Education")
            p.setFont("Helvetica", 10)
            for line in education.split("\n"):
                write(line)
            y -= 10

        if skills:
            p.setFont("Helvetica-Bold", 14)
            write("Skills")
            p.setFont("Helvetica", 10)
            for skill in skills.split(","):
                write(f"• {skill.strip()}")

        p.showPage()
        p.save()
        return response

    return render(request, "generate_cv.html")

def contact(request):
    return render(request, "contact.html")

@login_required
def manage_users(request):
    if not request.user.is_staff:
        messages.warning(request, "Access denied. Admin privileges required.")
        return redirect("dashboard")
    
    # Get all users
    all_users = User.objects.all().order_by('-date_joined')
    
    # Get user count by type
    total_users = User.objects.count()
    admin_users = User.objects.filter(is_staff=True).count()
    micro_workers = User.objects.filter(is_staff=False).count()
    
    context = {
        'all_users': all_users,
        'total_users': total_users,
        'admin_users': admin_users,
        'micro_workers': micro_workers,
    }
    return render(request, "manage_users.html", context)  # CHANGED from "admin/manage_users.html"

@login_required
def reports(request):
    if not request.user.is_staff:
        messages.warning(request, "Access denied. Admin privileges required.")
        return redirect("dashboard")
    
    # Sample report data
    user_growth = {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'data': [10, 15, 25, 40, 60, 85]
    }
    
    task_stats = {
        'total_tasks': 156,
        'completed_tasks': 120,
        'pending_tasks': 36,
        'success_rate': 77
    }
    
    context = {
        'user_growth': user_growth,
        'task_stats': task_stats,
    }
    return render(request, "reports.html", context)  # CHANGED from "admin/reports.html"

@login_required
def admin_settings(request):
    if not request.user.is_staff:
        messages.warning(request, "Access denied. Admin privileges required.")
        return redirect("dashboard")
    
    return render(request, "admin_settings.html")  # CHANGED from "admin/settings.html"