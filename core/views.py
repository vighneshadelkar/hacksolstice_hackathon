from django.contrib import messages as msg
from django.shortcuts import render, redirect
import messages
from django.shortcuts import render
from django.core.mail import send_mail
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
import uuid, os, requests
from django.conf import settings
from pip._vendor import cachecontrol
from django.contrib.auth.models import User, auth
from .models import Profile
import google.auth.transport.requests as req

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

flow = Flow.from_client_config(
        settings.GOOGLE_OAUTH_CLIENT_CONFIG,
        scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", 'openid'],
        redirect_uri="http://localhost:8000/callback"
        # redirect_uri=request.build_absolute_uri('/auth/google/callback')
)

def google_login(request):

    authorization_url, state = flow.authorization_url()

    request.session['state'] = state
    return redirect(authorization_url)

def google_callback(request):
    state = request.session.pop('state', None)
    if state is None:
        return redirect('/')

    flow.fetch_token(authorization_response=request.build_absolute_uri())
    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = req.Request(session=cached_session)

    # Get the user's profile information from the Google API

    client_id = "1004661201964-bhqa08thvacbl9k1eg7lpfgm6cafob32.apps.googleusercontent.com"
    idinfo = id_token.verify_oauth2_token(
        credentials.id_token, token_request, client_id
    )

    # Log in the user
    # print(idinfo)
    # print(idinfo['name'], idinfo['sub'])
    user = auth.authenticate(username = idinfo['name'], password=idinfo['sub'])
    if user is not None:
        request.session['username'] = idinfo['name']
        auth.login(request, user)
        return redirect('home')
    else:
        newuser = User.objects.create_user(username=idinfo['name'], password=idinfo['sub'])
        newuser.save()
        profile = Profile.objects.create(user=newuser, email=idinfo['email'])
        profile.save()

        auth.login(request, newuser)
        return redirect('home')

def send_forgot_password(email, token):
    subject = 'Your forgot password link'
    msg = f'Hi there, click on the link to reset your password http://127.0.0.1:8000/change-password/{token}/'
    email_from = settings.EMAIL_HOST_USER
    receipient_list = [email]
    print(subject, msg, email_from, receipient_list)
    send_mail(subject, msg, email_from, receipient_list)
    return True

def change_password(request, token):
    context = {}
    try:
        profile_obj = Profile.objects.filter(forgot_password_token = token).first()
        context = {'user_id' : profile_obj.user.id }

        if request.method == "POST":
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            user_id = request.POST.get('user_id')

            if user_id is None:
                messages.success(request, 'No user id found')
                return redirect('change-password/{token}/')
            
            if new_password != confirm_password:
                messages.success(request, 'Both password should be equal')
                return redirect('change-password/{token}/')
            
        user_obj = User.objects.get(id = user_id)
        user_obj.set_password(new_password)
        user_obj.save()
        
        return redirect('login')
        
    except Exception as e:
        print(e)
    return render(request, "change-password.html", context)

def forgot_password(request):
    # try:
    if request.method == "POST":
        username = request.POST['username']
        if not User.objects.filter(username = username).first():
            # messages.success(request, 'User does not exist')
            print('User does not exist')
            return redirect('forgot-password/')
        
        user_obj = User.objects.get(username = username)
        token = str(uuid.uuid4())
        profile_obj = Profile.objects.get(user = user_obj)
        profile_obj.forget_password_token = token
        profile_obj.save()
        send_forgot_password(user_obj, token)
        # messages.success(request, 'An email is sent')
        print('An email is sent')
        return redirect('forgot-password/')

    # except Exception as e:
    #     print(e)
    return render(request, "forgot-password.html")

def signup(request):
    # print(request.POST)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        phone = request.POST['phone']
        email = request.POST['email']
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already taken')
            return redirect('signup')
        else:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            profile = Profile.objects.create(user=user, email=email, phone=phone)
            profile.save()
            return redirect('/')
    else:
        return render(request, 'signup.html')
    
def login(request, user = "None"):
    print(request.POST)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            request.session['username'] = username
            auth.login(request, user)
            return redirect('home')
        else:
            msg.info(request, 'Incorrect credentials')
            return redirect('/')
    else:
        return render(request, 'login.html')
    
def logout(request):
    auth.logout(request)
    return redirect('/')

def frontpage(request):
    return redirect('login')

def home(request):
    return render(request, 'home.html')

def activity(request):
    return render(request, 'activity.html')

def info(request):
    return render(request, 'info.html')

def contact(request):
    return render(request, 'doctor.html')
