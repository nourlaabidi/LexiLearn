from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import Group

def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('welcomeO')
        elif request.user.is_active:
            return redirect('welcomeC')
    return render(request, "main/home.html")

def welcomeO(request):
    actualGroup=Group.objects.get(owner=request.user)
    members=actualGroup.members.all()
    return render(request,"main/welcomePageOrthophoniste.html" ,{'members':members})
def welcomeC(request):
    return render(request,"main/welcomePageChild.html")
        
def OrthophonistePage(request):
    return render(request,"main/orthophonistePage.html")

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('welcomeP')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password) 
        if user is not None:
            if user.is_staff:
                # Redirection vers la page du panneau d'administration
                login(request, user)
                return redirect('welcomeO')  # Rediriger vers l'interface d'administration Django
            elif user.is_active:
                login(request, user)
                return redirect('welcomeC')  # Rediriger vers la page spécifique pour les orthophonistes
            else:
                messages.error(request, 'Votre compte est désactivé.')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe invalide.')

    return render(request, "main/loginPage.html") 


def registerOrthophoniste(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Création d'un utilisateur de type Doctor
            doctor = User.objects.create_user(username=username, password=password, is_staff=True)
            # Création d'un groupe
            Group.objects.create(owner=doctor)
            # Association de l'utilisateur au groupe
            
            # Redirection vers une page de bienvenue après l'enregistrement
            return redirect('welcomeO')
        else:
            # Gestion des erreurs du formulaire
            messages.error(request, 'Il y a des erreurs dans le formulaire.')
    else:
        # Création d'une instance de formulaire vide pour l'affichage initial
        form = RegisterForm()
    # Rendu du formulaire dans le template avec les données appropriées
    return render(request, "main/register.html", {'form': form})

'''def show_members(request):
    actualGroup=Group.objects.get(owner=request.user)
    members=actualGroup.members.all()
    return render(request,"main/welcomePageOrthiphoniste.html" ,{members:members})'''
def create_child(request):
    if request.method == 'POST':
        if request.user.is_staff:
            form = RegisterForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                User.objects.create_user(username=username, password=password, is_active=True)
                child=User.objects.get(username=username)
                grp=Group.objects.get(owner=request.user)
                grp.members.add(child)
                grp.save()
                
                return JsonResponse({'message': 'Utilisateur créé avec succès!'}, status=201)
            else:
                return JsonResponse({'message': 'Il y a des erreurs dans le formulaire.', 'errors': form.errors}, status=400)
        else:
            return JsonResponse({'message': 'Vous n\'avez pas la permission de créer un utilisateur.'}, status=403)
    else:
        # Création d'une instance de formulaire vide pour l'affichage initial
        form = RegisterForm()
    # Rendu du formulaire dans le template avec les données appropriées
    return render(request, "main/register.html", {'form': form})
def manage_users(request):
    if request.method == 'POST':
        if request.user.is_staff:
            form = RegisterForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                User.objects.create_user(username=username, password=password, is_active=True)
                return JsonResponse({'message': 'Utilisateur créé avec succès!'}, status=201)
            else:
                return JsonResponse({'message': 'Il y a des erreurs dans le formulaire.', 'errors': form.errors}, status=400)
        else:
            return JsonResponse({'message': 'Vous n\'avez pas la permission de créer un utilisateur.'}, status=403)
    elif request.method == 'DELETE':
        if request.user.is_staff:
            username = request.GET.get('username')
            if username:
                try:
                    user = User.objects.get(username=username)
                    user.delete()
                    return JsonResponse({'message': 'Utilisateur supprimé avec succès!'})
                except User.DoesNotExist:
                    return JsonResponse({'message': 'L\'utilisateur spécifié n\'existe pas.'}, status=404)
            else:
                return JsonResponse({'message': 'Veuillez fournir un nom d\'utilisateur à supprimer.'}, status=400)
        else:
            return JsonResponse({'message': 'Vous n\'avez pas la permission de supprimer un utilisateur.'}, status=403)
    else:
        return JsonResponse({'message': 'Méthode non autorisée'}, status=405)
        
        
        
def logoutPage(request):
    logout(request)
    return redirect('home')

#@login_required(login_required='/login')