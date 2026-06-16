from django.shortcuts import render , redirect 
from django.http import HttpResponse 
from django.contrib import messages 
from django.contrib.auth.models import User 
from leaves.models import Leave 
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'staff.html')
@login_required
def apply_leave(request):
    if request.method == 'POST':
        username = request.POST['username']
        leave_type = request.POST['leave_type']
        email = request.POST['email']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        reason = request.POST['reason']
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
    return render(request,'leaves/reports.html')




