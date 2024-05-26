from datetime import date
import pronouncing
import Levenshtein
import speech_recognition as sr
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from .models import Group, Child, AudioFile, Word
from django.views.decorators.csrf import csrf_exempt
import os
 
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
def age_distribution_view(request):
    users = User.objects.all()
    
    age_intervals = {
        "6-10": 0,
        "10-14": 0,
        "+14": 0
    }
    
    for user in users:
        age = user.age
        if age is not None:
            if 6 <= age <= 10:
                age_intervals["6-10"] += 1
            elif 10 < age <= 14:
                age_intervals["10-14"] += 1
            elif age > 14:
                age_intervals["+14"] += 1
    
    context = {
        'age_intervals': age_intervals
    }
    return render(request, 'base.html', context)
#@login_required(login_required='/login')
@csrf_exempt
def saveaudio(request):
    print("problem N 1")
    print(request.method)
    if request.method == 'POST':
        print("problem N 2")
        print("Request method is POST")
        print("Files received:", request.FILES)
        if 'audio' in request.FILES:
            audio_file = request.FILES['audio']
            name = request.POST.get('name', 'Unnamed')
            audio_instance = AudioFile(name=name, audio=audio_file)
            audio_instance.save()
            # Transcribe the audio file
            recognizer = sr.Recognizer()
            audio_path = audio_instance.audio.path
            with sr.AudioFile(audio_path) as source:
                audio_data = recognizer.record(source)
                transcription = recognizer.recognize_google(audio_data)
                audio_instance.transcription = transcription
                audio_instance.save()

            return JsonResponse({'message': 'Audio file uploaded successfully.', 'id': audio_instance.id})
        else:
            print("No audio file in request")
    else:
        return render(request, 'main/listen.html')
        #print("Request method is not POST")
    return JsonResponse({'error': 'Invalid request'}, status=400)
def record_audio(request):
    return render(request,'main/record.html')

def listen_audio(request):
    audio_files = AudioFile.objects.all()
    return render(request, 'main/listen.html', {'audio_files': audio_files})

recognizer = sr.Recognizer()
def evaluate_audio(request):
    if request.method == 'POST':
        audio_blob = request.FILES['audio']
        audio_file = AudioFile.objects.create(audio=audio_blob, name='Recorded Audio')
        return JsonResponse({'id': audio_file.id})
    return JsonResponse({'error': 'Invalid request method.'})


def save_audio(request):
    if request.method == 'POST':
        audio_file = request.FILES['audio']
        name = request.POST.get('name', 'Unnamed')
        audio_instance = AudioFile(audio=audio_file, name=name)
        audio_instance.save()
        return JsonResponse({'id': audio_instance.id})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def evaluate_page(request, audio_id):
    audio_file = get_object_or_404(AudioFile, id=audio_id)
    #audio1= audio_file.audio.path
    print(audio_file.audio.url)
    #print(audio1)
    audio="main/static/recordings/important.wav"
    audiotest="main/static/recordings/important.wav"
    
    with sr.AudioFile(audio) as source:
        audio_data = recognizer.record(source)
        voice1 = recognizer.recognize_google(audio_data, language='en')
    
    with sr.AudioFile(audiotest) as source:
        audio_data = recognizer.record(source)
        voice2 = recognizer.recognize_google(audio_data, language='en')
    print("Voice 1:", voice1)
    print("Voice 2:", voice2)
    transcription_mot_attendu = pronouncing.phones_for_word(voice1)
    transcription_audio_enregistre = pronouncing.phones_for_word(voice2)
    # Comparaison de la similarité phonétique avec la distance de Levenshtein
    similarite = Levenshtein.distance(transcription_mot_attendu, transcription_audio_enregistre)
    score=100-88 % 100
    audio_file.score=score
    audio_file.save()
    #score=similarite
    print("score",score)
    return render(request, 'main/evaluation.html', {'audio_url': audio_file.audio.url, 'audio_id': audio_id,'score':score})

def exercicesChild(request):
    levels = Word.objects.values_list('level', flat=True).distinct()
    words_by_level = {}
    for level in levels:
        words_by_level[level] = Word.objects.filter(level=level)
    return render(request, 'main/exercicesChild.html', {'words_by_level': words_by_level})
def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
def profile(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        user=User.objects.get(username=username)
        child=Child.objects.get(user=user)
        age = calculate_age(child.date_of_birth)
        levels = Word.objects.values_list('level', flat=True).distinct()
        words_by_level = {}
        for level in levels:
            words_by_level[level] = Word.objects.filter(level=level)
        return render(request, 'main/profile.html', {'user':user,'child':child,'age':age, 'words_by_level': words_by_level })
        
        
    
            
        
    