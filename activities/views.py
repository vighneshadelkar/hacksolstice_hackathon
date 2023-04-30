from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.utils import timezone
from .models import Active
from core.models import Profile

def activity(request):
    active = list(Active.objects.filter(user=request.user).values_list('active_time', flat=True))[-7:]
    date_datetime = list(Active.objects.filter(user=request.user).values_list('date', flat=True))[-7:]
    dates = list(map(returnDate, date_datetime))
    return render(request, 'activity-1.html', {'active':active, 'dates':dates})

@receiver(user_logged_out)
def sig_user_logged_out(sender, user, request, **kwargs):
    if(Profile.objects.filter(user=user).exists()):
        profile = Profile.objects.get(user=user)
        profile.last_logout = timezone.now()

    else:
        profile = Profile(user=user, last_logout=timezone.now())

    last_login = user.last_login
    last_logout = profile.last_logout
    time_diff = (last_logout-last_login).total_seconds() / 60
    profile.time_diff = time_diff
    profile.save()
    if(Active.objects.filter(user=user, date=timezone.now().date()).exists()):
        active = Active.objects.get(user=user, date=timezone.now().date())
        active.active_time += time_diff
    else:
        active = Active(user=user, active_time=time_diff)
    active.save()

def returnDate(x):
    return int(x.strftime("%d"))