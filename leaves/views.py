from django.shortcuts import render , redirect 
from django.http import HttpResponse 
from django.contrib import messages 
from django.contrib.auth.models import User 
from leaves.models import Leave , LeaveBalance
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from django.core.mail import send_mail
from django.conf import settings


def home(request):
    return render(request, 'staff.html')


@login_required
@csrf_exempt
def apply_leave(request):
    if request.method == 'POST':
        print("Form Submitted")
        print(request.POST)
        leave_type = request.POST['leave_type']
        duration = request.POST['duration']
        half_day_session = request.POST.get('half_day_session')
        email = request.POST['email']
        start_date = request.POST['start_date']
        end_date = request.POST.get('end_date')
        reason = request.POST['reason']

        if not start_date:
            messages.error(request,"Start Date is required")
            return redirect('apply_leave')
        
        if duration == 'full' and not end_date:
            messages.error(request, "End Date is required")
            return redirect('apply_leave')

        if duration == 'half':
            end_date = start_date

        start_date_obj = date.fromisoformat(start_date)
        end_date_obj = date.fromisoformat(end_date)
        today = date.today()

        if start_date_obj < today:
            messages.error(request, "Invalid start date  !, you can not apply the leave for the previous date")
            return redirect('apply_leave')
        
        if end_date_obj < start_date_obj:
            messages.error(request, "Invalid end Date ! , You cant apply the leave fir the previous date")
            return redirect('apply_leave')
        
        if duration == 'half':
            if not half_day_session:
                messages.error(request, "Please select morning or Afternoon session")
                return redirect('apply_leave')
            
            if start_date_obj != end_date_obj:
                messages.error(request,"Half-day leave must be for a single day only")
                return redirect('apply_leave')
            
            total_days = 0.5
        else:
            total_days = (end_date_obj - start_date_obj).days+1
 
        Leave.objects.create(
            username = request.user , 
            leave_type = leave_type ,
            email = email,
            duration = duration,
            half_day_session = half_day_session,
            start_date = start_date , 
            end_date = end_date , 
            total_days = total_days,
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
    if leave.status != 'approved':
        balance , created = LeaveBalance.objects.get_or_create( user = leave.username)
        balance.used_leave += leave.total_days
        balance.save()
    leave.status = 'approved'
    leave.save()
    send_mail(
        subject = 'Leave Request Approved',
        message = f'''
        Hello  {leave.username.username},

        Your leave request has been  approved..
        Leave Type: {leave.leave_type}
        Start Date : {leave.start_date}
        End Date : {leave.end_date}

        Regards, 
        SLMS Team
     ''' ,
    from_email = settings.EMAIL_HOST_USER,
    recipient_list = [leave.email],
    fail_silently = False,
    )
    return redirect('leave_request')

@login_required
def reject_leave(request,id):
    leave = Leave.objects.get(id = id)
    leave.status = 'rejected'
    leave.save()
    send_mail(
        subject = 'Leave Request has been Rejected',
        message = f'''
        Hello  {leave.username.username},
        Your leave request has been rejected.
        Leave Type: {leave.leave_type}
        Start Date : {leave.start_date}
        End Date : {leave.end_date}

        Regards,
        SLMS Team
        ''',
        from_email = settings.EMAIL_HOST_USER,
        recipient_list = [leave.email],
        fail_silently = False,
    )
    return redirect('leave_request')

@login_required
def my_leaves(request):
    leaves=Leave.objects.filter(username=request.user).order_by('-id')
    return render(request,'leaves/my_leaves.html',{'leaves':leaves})

@login_required
def leave_reports(request):
    result = []
    staff_users = User.objects.filter(profile__role = 'staff').order_by('-id')
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

        balance , created = LeaveBalance.objects.get_or_create(
            user = user
        )

        result.append({
            'username' :  user.username,
            'email': user.email,
            'applied_leaves': total_leaves,
            'pending_leaves': pending_leaves,
            'approved_leaves': approved_leaves,
            'rejected_leaves':rejected_leaves,
            'total_leaves' : balance.total_leave,
            'used_leaves' : balance.used_leave , 
            'remaining_leaves' : balance.remaining_leave,

        })

    return render(request, 'leaves/reports.html', {'result': result})


        

        



        





