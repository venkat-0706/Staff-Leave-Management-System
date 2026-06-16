from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse 
from django.contrib import messages 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,  login , logout
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from leaves.models import Leave


def home(request):
    return render(request,'home.html')

@csrf_exempt
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        role = request.POST['role']

        if User.objects.filter(username = username).exists():
            messages.error(request,'User name Already Existed in the Database')
            return redirect('register')
        if User.objects.filter(email = email).exists():
            messages.error(request,'Email Already Existed in the Database')
            return redirect('register')
        
        if password != confirm_password:
            messages.error(request,'Password mismatching , please check again')
            return redirect('register')
        user = User.objects.create_user(
            username = username,
            email = email ,
            password = password
        )
        Profile.objects.create(
            user = user , 
            role = role 
        )
        messages.success(request, "Account Created Successfully")
        return redirect('login')
    return render(request, 'register.html')
@csrf_exempt
def loginview(request):
    if request.method == 'POST':
        username_or_email = request.POST['username_or_email']
        password = request.POST['password']

        if '@' in username_or_email:
            try:
                user_obj = User.objects.get(email=username_or_email)
                username = user_obj.username
            except User.DoesNotExist:
                username = username_or_email
        else:
            username = username_or_email

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)

            if user.profile.role == 'admin':
                return redirect('admin_dashboard')
            elif user.profile.role == 'staff':
                return redirect('staff_dashboard')

            return redirect('home')

        messages.error(request, "Invalid username/email or password")

    return render(request, 'login.html')

@login_required
def admin_dashboard(request):
    if request.user.profile.role != 'admin':
        return redirect('staff_dashboard')

    total_staff = User.objects.filter(
        profile__role='staff'
    ).count()

    total_leaves = Leave.objects.count()

    pending_leaves = Leave.objects.filter(
        status='pending'
    ).count()

    approved_leaves = Leave.objects.filter(
        status='approved'
    ).count()

    rejected_leaves = Leave.objects.filter(
        status='rejected'
    ).count()

    ctx = {
        'total_staff': total_staff,
        'total_leaves': total_leaves,
        'pending_leaves': pending_leaves,
        'approved_leaves': approved_leaves,
        'rejected_leaves': rejected_leaves,
    }

    return render(request, 'admin.html', ctx)


@login_required
def staff_dashboard(request):
    total_leaves = Leave.objects.filter(username = request.user).count()
    pending_leaves = Leave.objects.filter(username = request.user, status = 'pending').count()
    approved_leaves = Leave.objects.filter(username = request.user ,  status = 'approved').count()
    rejected_leaves = Leave.objects.filter(username = request.user , status = 'rejected').count()
    ctx = {
        'total_leaves':total_leaves , 
        'pending_leaves': pending_leaves,
        'approved_leaves': approved_leaves,
        'rejected_leaves' : rejected_leaves
    }
    return render(request, 'staff.html', ctx)



def logoutview(request):
    logout(request)
    return redirect('login')
    
@login_required
def manage_staff(request):
    if request.user.profile.role != 'admin':
        return redirect('staff_dashboard')

    query = request.GET.get('q', '')

    staff_list = User.objects.filter(profile__role='staff')

    if query:
        staff_list = staff_list.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query)
        )

    context = {
        'staff_list': staff_list,
        'query': query
    }

    return render(request, 'accounts/manage_staff.html', context)


@login_required
def add_staff(request):
    if request.user.profile.role != 'admin':
        return redirect('staff_dashboard')
    if request.method == "POST":
        username =  request.POST['username']
        email  = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username =  username).exists():
            messages.error(request , "USer name Already Existed")
            return redirect('manage_staff')
        
        if User.objects.filter(email = email).exists():
            messages.error(request, "Email Already Existed")
            return redirect('manage_staff')

        user = User.objects.create_user(
            username = username , 
            email = email ,
            password = password,
        )
        Profile.objects.create(
            user = user,
            role='staff'
        )
        messages.success(request,"Staff Added Successfully")
        return redirect('manage_staff')
    return render(request , 'accounts/add_Staff.html')


@login_required
def edit_staff(request , id):
    if request.user.profile.role != 'admin':
        return redirect('staff_dashboard')
    user = User.objects.get(id = id)
    if request.method == "POST":
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.save()
        return redirect('manage_staff')
    return render(request, 'accounts/edit_staff.html' ,{'user': user})


@login_required
def delete_staff(request, id):
    if request.user.profile.role != 'admin':
        return redirect('staff_dashboard')
    user = get_object_or_404(User, id=id)
    user.delete()
    return redirect('manage_staff')






    
    
    



        