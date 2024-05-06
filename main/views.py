from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout , admin
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
def home(request):
    return render(request, "main/home.html")
def welcomePage(request):
    return render(request,"main/welcomePage.html")
def loginOrthophoniste(request):
    if request.user.is_authenticated:
        return redirect('welcomePage')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        is_admin = 'is_admin' in request.POST  # Vérifie si la case à cocher administrateur est cochée
        is_medecin = 'is_medecin' in request.POST  # Vérifie si la case à cocher médecin est cochée
        user = authenticate(request, username=username, password=password) 
        if user is not None:
                if is_admin:
                    # Ajouter la permission de superutilisateur
                    user.is_superuser = True
                    user.save()
                    login(request, user)
                    # Rediriger vers le panneau d'administration de Django
                    return redirect('admin/')
                elif is_medecin:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'Vous n\'avez pas les droits requis pour accéder à cette page.')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe invalide.')
    return render(request,"main/loginOrthophoniste.html")  
def loginPatient(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password) 
        if user is not None:
            login(request, user)
            return redirect('welcomePage')
        else :
            messages.error(request, 'check your username and password!')
    return render(request,"main/loginPatient.html") 
def registerOrthophoniste(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            admin_username = form.cleaned_data['admin_username']
            admin_password = form.cleaned_data['admin_password']
            # verifier si le user a un compte superuser en parallele
            admin_user = authenticate(username=admin_username, password=admin_password)
            if admin_user.is_superuser  :
                # Création du nouvel utilisateur Doctor
                User.objects.create_user(username=username, password=password)
                return redirect('welcomePage')
            else:
                messages.error(request, 'admin nexiste pas veuiller creer votre compte admin')
    else:
        form = RegisterForm()
    return render(request, "main/registerOrthophoniste.html", {'form': form}) 
from django.contrib.auth.models import User  # Assurez-vous d'importer User

'''def registerOrthophoniste(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Création d'un utilisateur en utilisant les données du formulaire
            User.objects.create_user(username=username, password=password, is_staff=True)
            # Redirection vers une page de bienvenue après l'enregistrement
            return redirect('welcomePage')
        else:
            # Gestion des erreurs du formulaire
            messages.error(request, 'Il y a des erreurs dans le formulaire.')
    else:
        # Création d'une instance de formulaire vide pour l'affichage initial
        form = RegisterForm()
    # Rendu du formulaire dans le template avec les données appropriées
    return render(request, "main/registerOrthophoniste.html", {'form': form})'''
           
        
        
        
def logoutPage(request):
    logout(request)
    return redirect('home')

#@login_required(login_required='/login')