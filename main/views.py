from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from .models import Group, Child

def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff and request.user.is_superuser==False:
            return redirect('welcomeO')
        elif request.user.is_active and request.user.is_superuser==False :
            return redirect('welcomeC')
    return render(request, "main/home.html")
def test(request):
    return render(request,"main/test.html")
def welcomeO(request):
    actualGroup=Group.objects.get(owner=request.user)
    members=actualGroup.members.all()
    return render(request, 'main/welcomePageOrthophoniste.html',{'members':members, 'actualGroup' : actualGroup})
def searchUser(request):
    if request.method == 'GET':
        search_query = request.GET.get('search_query')
        if search_query:
            group=Group.objects.get(owner=request.user)
            users = group.members.filter(username__icontains=search_query)
        else:
            users = []
        return render(request, 'main/welcomePageOrthophoniste.html', {'users': users, 'query': search_query})
    return render(request, 'main/welcomePageOrthophoniste.html' )
        
def welcomeC(request):
    return render(request,"main/welcomePageChild.html")
        


def loginPage(request):
    if request.user.is_authenticated:
        if user.is_staff:
            return redirect('welcomeO') 
        elif user.is_active:
            return redirect('welcomeC')
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
        

    return render(request, "main/loginPage.html") 

def loginPageChild(request):
    if request.user.is_authenticated: 
        if user.is_active and user.is_staff==False:
            return redirect('welcomeC')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password) 
        if user is not None:
            if user.is_active and user.is_staff==False:
                login(request, user)
                return redirect('welcomeC')  # Rediriger vers la page spécifique pour les orthophonistes
            else:
                messages.error(request, 'Votre compte est désactivé.')

    return render(request, "main/loginPageChild.html") 


def registerOrthophoniste(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        if username and password:
            # Création d'un utilisateur de type Doctor
            doctor = User.objects.create_user(username=username, password=password,email=email, is_staff=True)
            # Création d'un groupe
            Group.objects.create(owner=doctor)
            # Association de l'utilisateur au groupe
            
            # Redirection vers une page de bienvenue après l'enregistrement
            return redirect('home')
        else:
            # Gestion des erreurs du formulaire
            messages.error(request, 'Veuillez fournir un nom d\'utilisateur et un mot de passe valides.')
    # Rendu du formulaire dans le template avec les données appropriées
    return render(request, "main/register.html")


def create_child(request):
    if request.method == 'POST':
        if request.user.is_staff:
            username = request.POST.get('username')
            password = request.POST.get('password')
            date_of_birth = request.POST.get('date_of_birth')
            phone_number = request.POST.get('phone_number')

            if username and password:
                try:
                    # Créer l'utilisateur
                    user = User.objects.create_user(username=username, password=password)
                    child=User.objects.get(username=username)
                    # Créer l'enfant
                    Child.objects.create(
                        user=user,
                        date_of_birth=date_of_birth,
                        phone_number=phone_number
                    )
                    # Associer l'enfant au groupe
                    group = Group.objects.get(owner=request.user)
                    group.members.add(child)
                    group.save()
                    messages.success(request, 'Message de réussite!')
                    return redirect('home')
                except Exception as e:
                    return JsonResponse({'message': 'Erreur lors de la création de l\'utilisateur.', 'error': str(e)}, status=500)
            else:
                return JsonResponse({'message': 'Certains champs requis sont manquants.'}, status=400)
        else:
            return JsonResponse({'message': 'Vous n\'avez pas la permission de créer un utilisateur.'}, status=403)
    return render(request, "main/register.html")
def accounts(request):
    actualGroup=Group.objects.get(owner=request.user)
    members=actualGroup.members.all()
    return render(request, 'main/accounts.html',{'members':members, 'actualGroup' : actualGroup})
def DeleteChild(request):
    if request.method == 'POST':
            username = request.POST.get('username')
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
        return JsonResponse({'message': 'Méthode non autorisée'}, status=405)
        
        
        
def logoutPage(request):
    logout(request)
    return redirect('home')

#@login_required(login_required='/login')