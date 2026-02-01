from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Login view
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)  # uses CustomAuthBackend
        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            error_message = "Invalid email or password"
    else:
        error_message = None

    return render(request, 'pouultry_proapp/login.html', {'error_message': error_message})

