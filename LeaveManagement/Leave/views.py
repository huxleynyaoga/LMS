from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse

from .forms import LoginForm, LeaveApplicationForm
from .models import LeaveApplication

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum
from django.utils import timezone

# Create your views here.


# - Login Page

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('dashboard') 
    context = {'form':form}
    return render(request, 'Leave/login.html', context)



# - Dasboard Page     ZOHO PEOPLE

@login_required(login_url='login')
def dashboard(request):
    current_year = timezone.now().year
    pendingl = LeaveApplication.objects.filter(user=request.user, status='APPROVED', date_of_application__year=current_year).order_by('-date_of_application')
    form = LeaveApplicationForm()
    
    user = request.user
    sick_leave_total = LeaveApplication.objects.filter(user=user, leave_type='Sick Leave', status='APPROVED').aggregate(Sum('total_leave_days'))
    casual_leave_total = LeaveApplication.objects.filter(user=user, leave_type='Casual Leave', status='APPROVED').aggregate(Sum('total_leave_days'))
    annual_leave_total = LeaveApplication.objects.filter(user=user, leave_type='Annual Leave', status='APPROVED').aggregate(Sum('total_leave_days'))
    maternity_leave_total = LeaveApplication.objects.filter(user=user, leave_type='Maternity Leave', status='APPROVED').aggregate(Sum('total_leave_days'))
    paternity_leave_total = LeaveApplication.objects.filter(user=user, leave_type='Paternity Leave', status='APPROVED').aggregate(Sum('total_leave_days'))
    
    sick_leave_days = sick_leave_total['total_leave_days__sum'] or 0
    casual_leave_days = casual_leave_total['total_leave_days__sum'] or 0
    annual_leave_days = annual_leave_total['total_leave_days__sum'] or 0
    maternity_leave_days = maternity_leave_total['total_leave_days__sum'] or 0
    paternity_leave_days = paternity_leave_total['total_leave_days__sum'] or 0
    
    return render(request, 'Leave/dashboard.html', {'form': form, 'pendingl': pendingl, 'sick': sick_leave_days, 'casual': casual_leave_days, 'annual': annual_leave_days, 'maternity': maternity_leave_days, 'paternity': paternity_leave_days})


# - Logout

def logout(request):
    auth.logout(request)
    return redirect('login')


# - Leave application

@login_required(login_url='login')
def application(request):
    if request.method == 'POST':
        form = LeaveApplicationForm(request.POST)
        if form.is_valid():
            leave_application = form.save(commit=False)
            leave_application.user = request.user  # Assign the user
            leave_application.save()
            messages.success(request, "Leave Applied Successfully.")
            return redirect('dashboard')
    else:
        form= LeaveApplicationForm()
    return render(request, 'Leave/application.html', {'form': form})
    
    
    
# - Pending leaves for Approval

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def pending(request):
    allp = LeaveApplication.objects.filter(status='PENDING').count()
    leave_applications = LeaveApplication.objects.filter(status='PENDING')
    return render(request, 'Leave/pending.html', {'leave_applications': leave_applications, 'allpend':allp})
    


# Approve or Decline pending requests

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def approve(request, id):
    leave = get_object_or_404(LeaveApplication, pk=id)
    if request.method == 'POST':
        action = request.POST.get('action')
        comment = request.POST.get('comment', '')
        
        if action in ['approve', 'decline']:
            leave.status = 'APPROVED' if action == 'approve' else 'DECLINED'
            leave.reviewed_by = request.user
            leave.review_date = timezone.now()
            leave.review_comment = comment
            leave.save()
            return redirect('pending')
    return render(request, 'Leave/pending.html', {'leave': leave})

