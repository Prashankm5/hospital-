from django.shortcuts import render,redirect
from django.contrib import messages, auth
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from accounts.utils import send_verification_email, detectUser
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from .models import User



# Create your views here.

def home(request):
    return render(request, 'home.html')



def signUp(request):
     if request.user.is_authenticated:
        messages.warning(request, "You are already logged In!!")
        return redirect('myAccount')
     elif request.method == "POST":
          form = UserForm(request.POST)
          
          if form.is_valid():
               first_name = form.cleaned_data['first_name']
               last_name = form.cleaned_data['last_name']
               email = form.cleaned_data['email']
               username = form.cleaned_data['username']
               password = form.cleaned_data['password']
               role = form.cleaned_data['role']
               profile_picture = form.cleaned_data['profile_picture']
               adress_line1 = form.cleaned_data['adress_line1']
               city = form.cleaned_data['city']
               state = form.cleaned_data['state']
               zip_code = form.cleaned_data['zip_code']
               user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
               user.role = role
               user.profile_picture = profile_picture
               user.adress_line1 = adress_line1
               user.city = city
               user.state = state
               user.zip_code = zip_code
               user.save() 
                 
                 
               # Send verification email
               email_subject = 'Hospital Account verification email'
               email_template = "emails/account_verification_email.html"
               send_verification_email(request, user, email_subject, email_template)

               messages.success(request, "Your acoount has been reated successfuly!!! Check your email for activation link.")
               return redirect("signUp")

          else:
               print("Invalid form")
               print(form.errors)

            
     else:
          form = UserForm()

     context = {
         'form': form
     }
     
     return render(request, 'account/signUp_user.html', context)






def activate(request, uidb64, token):
    # Activate the user by setting is_active status to True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError,OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Congratulations!!! Your account is activated.")
        return redirect("signIn")
    else:
        messages.error(request, "Invailid activation link")
        return redirect("signIn")





def signIn(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged In")
        return redirect("myAccount")
    elif request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are loged In.")
            return redirect("myAccount")
        
        else:
            messages.error(request, "Invailid login credentials.")
            return redirect("signIn")
    
    else:
        form = UserForm()
    
    context = {
        'form': form
    }

    return render(request, 'account/signIn.html', context)


@login_required(login_url='signIn')
def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logout')
    return redirect('signIn')

@login_required(login_url='signIn')
def myAccount(request):
    user = request.user
    user_type = detectUser(user)
    if user_type == '/admin':
        return redirect(user_type)
    else:
        return redirect(f'{detectUser(user)}Dashboard')




def patientDashboard(request):
    user = request.user

    user_type = detectUser(user)
    context = {
        'user': user,
    }
    return render(request,f'{user_type}/dashboard.html', context)

def doctorDashboard(request):
    user = request.user

    user_type = detectUser(user)
    context = {
        'user': user,
    }
    return render(request,f'{user_type}/dashboard.html', context)