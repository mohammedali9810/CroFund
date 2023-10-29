from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import ( authenticate,login,logout,get_user_model)
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils import timezone
from datetime import datetime, timedelta
from django.template.loader import render_to_string  
from .token import account_activation_token
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage
from django.contrib import messages





@login_required 
def index(request):
    top_5projects=[]
    admin_choice=[]  
    latest_projects=[]

    #Categories 
    categories=Categories.objects.all()

    #Top rated binding with their images
    top_rated=Rating.objects.values('project_id').annotate(rates=Avg('rating')).order_by('-rates')[:5]  
    for i in top_rated:
        project=Projects.objects.get(pk=i['project_id'])
        images=Images.objects.filter(project_id=i['project_id'])
        top_5projects.append({'project':project,'images':images})

    #Admin choosen projects binding with their images
    admin_choice_query=Choosen_by_Admin.objects.all()[:5]  
    for i in admin_choice_query:
        images=Images.objects.filter(project_id=i.id)
        admin_choice.append({'project':i,'images':images})

    #Latest Added projects
    latest_projects_query=Projects.objects.order_by('-id')[:5]   
    for i in latest_projects_query:
        images=Images.objects.filter(project_id=i.id)
        latest_projects.append({'project':i,'images':images})
    context={'top5':top_5projects,'admin_choice':admin_choice,
            'latest_projects':latest_projects,'categories':categories}
    return  render(request,'home.html',context)



@login_required
def profile(request, username):

    user = User.objects.get(username = username)
    id = user.id
    addtionalinfo = Profile.objects.get(user_id = id)
    user_project = Projects.objects.filter(user_id = id)
    categories=Categories.objects.all()
    donate_sum = Donation.objects.all().filter(user_id=id).values('amount_of_money')

    d_sum = 0

    # overall user donation
    for item in donate_sum:
        print(item)
        d_sum += item['amount_of_money']
        
        
    if user:
        context = {
            'userinfo': user,
            'addtionalinfo': addtionalinfo,
            'userproject': user_project,
            'categories':categories,
            'donate_sum':d_sum
        }
        return render(request, 'profile.html', context)
    else:
        return render(request, '404.html')

@login_required
def editprofile(request, id):
    if request.method == 'POST':
        birthdate_str = request.POST.get('birth', '')
        birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d').date() if birthdate_str else None
        if birthdate and (timezone.now().date() - birthdate) < timedelta(days=365 * 18):
            messages.error(request, 'You must be at least 18 years old.')
            return redirect('profile', username=request.user.username)

        user = User.objects.get(pk=id)

        if request.POST['username'] != user.username:
            messages.success(request, 'Username updated successfully.')
            user.username = request.POST['username']

        if request.POST['email'] != user.email:
            messages.success(request, 'Email updated successfully.')
            user.email = request.POST['email']

        user.save()

        profile = user.profile
        if request.POST['country'] != profile.country:
            messages.success(request, 'Country updated successfully.')
            profile.country = request.POST['country']

        if request.POST['social_media'] != profile.social_media:
            messages.success(request, 'Social Media updated successfully.')
            profile.social_media = request.POST['social_media']

        if request.POST['phone'] != profile.phone:
            messages.success(request, 'Phone Number updated successfully.')
            profile.phone = request.POST['phone']

        if request.POST['birth'] != profile.birth:
            messages.success(request, 'Birth Date updated successfully.')
            profile.birth = request.POST['birth']

        profile.save()

        return redirect('profile', username=user.username)



def user_login(request):
    if request.method == 'POST':
        form = userLogin(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username,password=password)
            login(request,user)
            user_info = User.objects.get(username=username)
            if user_info.is_active == True:
                
                return redirect(index)
    else:
        form = userLogin()        
    return render(request,"login.html",{"form":form})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        form2 = UserProfile(request.POST,request.FILES)
        if form.is_valid() and form2.is_valid():
            pr=form.save(commit=False)
            pr.is_active = False 
            pr.save()
            username = form.cleaned_data.get('username')
            profile = form2.save(commit=False)
            
            current_user = User.objects.get(username=username)
            
            profile.user = current_user
            profile.save()
            current_site = get_current_site(request) 
            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('acc_active_email.html', {
                'user': pr,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(pr.pk)), 
                'token':account_activation_token.make_token(pr),  
            })   
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]
            ) 
            email.send()  
            return HttpResponse('Please confirm your email address to complete the registration')  
        
    else:
        form = UserRegisterForm()
        form2 = UserProfile()
    return render(request,'register.html', {'form': form , 'form2':form2})

@login_required
def delete_profile(request, id):
    user = User.objects.get(pk=id)
    if request.user == user:
        if request.method == 'POST':
            user.delete()
            messages.success(request, 'Your profile has been deleted successfully.')
            return redirect('login')
        else:
            return render(request, 'delprofile.html', {'user': user})
    else:
        messages.error(request, 'You are not authorized to delete this profile.')
        return redirect('login')




@login_required
def logout_profile(request):
    logout(request)
    return redirect('login')


def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return redirect(user_login)  
    else:  
        return HttpResponse('Activation link is invalid!') 
         