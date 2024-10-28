
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse

from publications.models import Publication
from .models import PasswordReset  
from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage

CustomUser = get_user_model()  # Dynamically get the custom user model


@login_required
def Home(request):
    return render(request, 'home.html')

@login_required
def profile(request):
     if request.method == "POST":
        profile_picture = request.FILES.get('profile_picture')
        print(profile_picture)
        if profile_picture:
            request.user.photo = profile_picture  # Met à jour la photo de l'utilisateur
            request.user.save()  # Enregistre les modifications
            print(request.user.photo)
            return redirect('home')  # Redirige vers la page de profil (ajustez selon vos besoins)

     return render(request, 'profile.html', {'user': request.user})

def RegisterView(request):

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        abonnement = request.POST.get('abonnement')  # Récupérez le type d'abonnement
        photo = request.FILES.get('photo')  # Récupérez la photo téléchargée
        user_data_has_error = False

        if CustomUser.objects.filter(username=username).exists():
            user_data_has_error = True
            messages.error(request, "Username already exists")

        if CustomUser.objects.filter(email=email).exists():
            user_data_has_error = True
            messages.error(request, "Email already exists")

        if len(password) < 5:
            user_data_has_error = True
            messages.error(request, "Password must be at least 5 characters")

        if user_data_has_error:
            return redirect('register')
        else:
            fs = FileSystemStorage()
            filename = fs.save(photo.name, photo)
            # Obtenez le chemin de la photo
            photo_url = fs.url(filename)
            new_user = CustomUser.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email, 
                username=username,
                password=password,
                abonnement=abonnement,  # Assignez le type d'abonnement
                photo=photo_url  # Assignez la photo téléchargée
            )
            messages.success(request, "Account created. Login now")
            return redirect('login')

    return render(request, 'register.html')

def LoginView(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect('home')
        
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')

    return render(request, 'login.html')

def LogoutView(request):

    logout(request)

    return redirect('login')

@login_required
def PublicationsView(request):
    list_publications=Publication.objects.all()
    print(list_publications)
    context = {"list_publications": list_publications}  
    return render(request, "publication.html", context)
@login_required
def GalleryView(request):
    list_publications = Publication.objects.filter(user=request.user)
    context = {"list_publications": list_publications}
    return render(request, "publication.html", context)
def ForgotPassword(request):

    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = CustomUser.objects.get(email=email)

            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

            password_reset_url = reverse('reset-password', kwargs={'reset_id': new_password_reset.reset_id})

            full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'

            email_body = f'Reset your password using the link below:\n\n\n{full_password_reset_url}'
        
            email_message = EmailMessage(
                'Reset your password', # email subject
                email_body,
                settings.EMAIL_HOST_USER, # email sender
                [email] # email  receiver 
            )

            email_message.fail_silently = True
            email_message.send()

            return redirect('password-reset-sent', reset_id=new_password_reset.reset_id)

        except CustomUser.DoesNotExist:
            messages.error(request, f"No user with email '{email}' found")
            return redirect('forgot-password')

    return render(request, 'forgot_password.html')

def PasswordResetSent(request, reset_id):

    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'password_reset_sent.html')
    else:
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')

def ResetPassword(request, reset_id):

    try:
        password_reset_id = PasswordReset.objects.get(reset_id=reset_id)

        if request.method == "POST":
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            passwords_have_error = False

            if password != confirm_password:
                passwords_have_error = True
                messages.error(request, 'Passwords do not match')

            if len(password) < 5:
                passwords_have_error = True
                messages.error(request, 'Password must be at least 5 characters long')

            expiration_time = password_reset_id.created_when + timezone.timedelta(minutes=10)

            if timezone.now() > expiration_time:
                passwords_have_error = True
                messages.error(request, 'Reset link has expired')

                password_reset_id.delete()

            if not passwords_have_error:
                user = password_reset_id.user
                user.set_password(password)
                user.save()

                password_reset_id.delete()

                messages.success(request, 'Password reset. Proceed to login')
                return redirect('login')
            else:
                # redirect back to password reset page and display errors
                return redirect('reset-password', reset_id=reset_id)

    
    except PasswordReset.DoesNotExist:
        
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')

    return render(request, 'reset_password.html')