from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
from .forms import StudentSignupForm, RecruiterSignupForm
from .models import Student, Recruiter
from django.contrib.auth import views as auth_views
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
'''
def student_signup(request):
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            # create a new user
            user = form.save(commit=False)
            user.is_student = True
            user.save()

            # create a new student
            student = Student.objects.create(user=user)

            # log in the user and redirect to the home page
            login(request, user)
            return redirect('login')
    else:
        form = StudentSignupForm()
    return render(request, 'student_signup.html', {'form': form})
    '''

def recruiter_signup(request):
    if request.method == 'POST':
        form = RecruiterSignupForm(request.POST)
        if form.is_valid():
            # create a new user
            form.save()
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password1')
            user=authenticate(username=username, password=password)
            user=User.objects.filter(username=username).first()
            user.is_staff = True
            user.save()

            login(request, user,backend='django.contrib.auth.backends.ModelBackend')

            # create a new recruiter
            #recruiter = Recruiter.objects.create(user=user, company_email=form.cleaned_data.get('company_email'), company_name=form.cleaned_data.get('company_name'))

            current_user=request.user
            data=Recruiter()
            data.user_id=current_user.id
            data.save()
            # log in the user and redirect to the home page
            
            return HttpResponseRedirect('')
    else:
        form = RecruiterSignupForm()
    return render(request, 'recruiter_signup.html', {'form': form})


def recruiter_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active and user.is_recruiter:
                login(request, user)
                messages.success(request, 'Login successfull')
                print("Successfully logged in")
                return redirect('home.html')
            else:
                messages.error(request, 'Invalid login credentials')
        else:
            messages.error(request, 'Invalid login credentials')

    return render(request, 'home.html')


'''
if request.user.is_authenticated and request.user.is_staff:
    
    
else

    '''

def logout_func(request):
    logout(request)
    return HttpResponseRedirect('')