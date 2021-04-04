from django.shortcuts import render , redirect , get_object_or_404 , HttpResponse
from . forms import UserLogInForm , UserRegistrationForm , EditProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from post.models import Post
from django.contrib.auth.decorators import login_required
from . models import Profile , Follow
from django.contrib.auth.hashers import make_password
from .forms import PhoneLoginForm , VerifyForm
from kavenegar import *
import random


def user_login(request):
    if request.method == 'POST':
        form = UserLogInForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request , username=cd['username'] , password=cd['password'])
            if user is not None:
                login(request,user)
                messages.success(request,'you logged in succesfully', extra_tags='success')
                return redirect('post:all_posts')
            else:
                messages.error(request,'please Enter correct username or password')
        
    else:
        form = UserLogInForm()
    return render(request,'account/login.html',context={'form':form})

def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                user = User.objects.get(email=cd['email'])
                if user is not None:
                    form = UserRegistrationForm()
                    messages.error(request,'This email is already exist')
                    return render(request,'account/registration.html',{'form':form})
            except:
                if cd['password']==cd['password2']:    
                    user = User(username=cd['username'],email=cd['email'],password=cd['password'])
                    user.password = make_password(cd['password'])
                    user.save()
                    login(request,user)
                    messages.success(request ,'You registered successfully')
                    return redirect('post:all_posts')
                else:
                    messages.error(request,'Confirm password is not match.Please try again.' , 'error')
                    return redirect('account:user_registration')
    else:
        form = UserRegistrationForm()
        return render(request,'account/registration.html',{'form':form})

@login_required
def user_logout(request):
        logout(request)
        messages.success(request,'you logged out succesfully',extra_tags='success')
        return redirect('account:first_page')

@login_required
def user_dashboard(request , user_id):
    user = get_object_or_404(User,id=user_id)
    posts = Post.objects.filter(user=user)
    profile = Profile.objects.get(user=user)
    if request.user == user:
        owner = True
    else:
        owner = False

    from_user = get_object_or_404(User,id=request.user.id)
    to_user = get_object_or_404(User ,id = user_id)
    try:
        follow = Follow.objects.get(from_user=from_user , to_user=to_user)
        tag = 'warning'
        value = 'Unfollow'
    except:
        tag = 'primary'
        value = 'Follow'            
    return render(request,'account/dashboard.html',{'user':user , 'posts':posts ,'profile':profile , 'owner':owner , 'tag':tag ,'value':value})

        


@login_required
def edit_profile(request,user_id):
    if request.method =='POST':
        form = EditProfileForm(data = request.POST , files=request.FILES)
        if form.is_valid():
            user = get_object_or_404(User,id = user_id)
            profile = get_object_or_404(Profile,user = user)
            e = form.save(commit=False)
            e.id = profile.id
            e.user = profile.user
            e.bio = form.cleaned_data['bio']
            e.phone = form.cleaned_data['phone']
            e.save()
            messages.success(request,'Your profile edited successfully','success')
            return redirect('account:user_dashboard',user_id)

    else:
        user = get_object_or_404(User , id = user_id)
        profile = get_object_or_404(Profile, user = user)
        email = user.email
        form = EditProfileForm(instance = profile, initial = {'email':email})
        return render (request,'account/edit_profile.html',{'form':form})


def first_page(request):
    return render(request , 'account/first_page.html')

@login_required
def follow_user(request , from_user , to_user):
    from_user = get_object_or_404(User,id = from_user)
    to_user = get_object_or_404(User,id = to_user)   
    try:
        follow = Follow.objects.get(from_user=from_user , to_user= to_user)
        follow.delete()
        messages.success(request , f'You unfollowed {to_user} successfully')
        return redirect ('account:user_dashboard',to_user.id)
    except:
        follow=Follow.objects.create(from_user=from_user , to_user= to_user)
        messages.success(request,f'You followed {to_user} successfully')
        return redirect ('account:user_dashboard',to_user.id)
    
def phone_login(request):
    if request.method=='POST':
        form = PhoneLoginForm(request.POST)
        if form.is_valid():
            global rand , phone
            phone = form.cleaned_data["phone"]
            rand = random.randint(1000,9999)
            print (rand , phone)
            try:
                profile = Profile.objects.get(phone=phone)
                phone = f'0{phone}'
                api = KavenegarAPI('645942497458414E454A3246684C443964424C4642682F4F612F6245756D354C67534D6D445049537243303D')
                params = { 'sender' : '1000596446', 'receptor': phone , 'message' : f'به شبکه اجتماعی رادمهر خوش امدید.کد تایید شما {rand}میباشد' }
                response = api.sms_send(params)
                form = VerifyForm()
                return render(request , 'account/verify.html' , {'form':form})
            except:
                messages.error(request,'Your phone is not available.First you must add your phone by editing your profile.Please choose another login method','warning')
                return redirect('account:user_login')
    else:
        form = PhoneLoginForm()
        return render(request,'account/phone_login.html',{'form':form}) 


def verify_code(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if rand == cd ['code']:
                profile = Profile.objects.get(phone=phone)
                user = profile.user
                login(request,user)
                messages.success(request,'You login successfully' , 'success')
                return redirect('post:all_posts')
            else:
                form = VerifyForm()
                messages.error(request,'Your code not match','warning')
                return redirect ('account:phone_login')

        



        


