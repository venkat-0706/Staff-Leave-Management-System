from django.shortcuts import render , redirect 
from django.http import HttpResponse 
from django.contrib import messages 
from django.contrib.auth.models import User 
from leaves.models import Leave 
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from datetime import date


def home(request):
    return render(request, 'staff.html')


@login_required
@csrf_exempt
def apply_leave(request):
    if request.method == 'POST':
        username = request.POST['username']
        leave_type = request.POST['leave_type']
        email = request.POST['email']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        reason = request.POST['reason']

        start_date_obj = date.fromisoformat(start_date)
        end_date_obj = date.fromisoformat(end_date)
        today = date.today()

        if start_date_obj < today:
            messages.error(request, "Invalid start date  !, you can not apply the leave for the previous date")
            return redirect('apply_leave')
        
        if end_date_obj < start_date_obj:
            messages.error(request, "Invalid end Date ! , You cant apply the leave fir the previous date")
            return redirect('apply_leave')
 
        Leave.objects.create(
            username = request.user , 
            leave_type = leave_type ,
            email = email,
            start_date = start_date , 
            end_date = end_date , 
            reason = reason 
        )
        messages.success(request , 'Leave Applied Successfully')
        return redirect('staff_dashboard')
    return render(request, 'leaves/apply_leave.html')

@login_required
def leave_request(request):
    leave_list = Leave.objects.all().order_by('-id')
    return render(request,'leaves/leave_request.html',{'leave_list':leave_list})

@login_required
def approve_leave(request, id):
    leave = Leave.objects.get(id = id)
    leave.status = 'approved'
    leave.save()
    return redirect('leave_request')

@login_required
def reject_leave(request,id):
    leave = Leave.objects.get(id = id)
    leave.status = 'rejected'
    leave.save()
    return redirect('leave_request')

@login_required
def my_leaves(request):
    leaves=Leave.objects.filter(username=request.user)
    return render(request,'leaves/my_leaves.html',{'leaves':leaves})

@login_required
def leave_reports(request):
    result = []
    staff_users = User.objects.filter(profile__role = 'staff')
    for user in staff_users:
        total_leaves = Leave.objects.filter(username = user).count()

        pending_leaves = Leave.objects.filter(
            username = user,
            status = 'pending'
        ).count()

        approved_leaves = Leave.objects.filter(
            username = user, 
            status = 'approved'
        ).count()

        rejected_leaves = Leave.objects.filter(
            username = user, 
            status = 'rejected'
        ).count()

        result.append({
            'username' :  user.username,
            'email': user.email,
            'total_leaves': total_leaves,
            'pending_leaves': pending_leaves,
            'approved_leaves': approved_leaves,
            'rejected_leaves':rejected_leaves
        })

    return render(request, 'leaves/reports.html', {'result': result})


        

        



        





