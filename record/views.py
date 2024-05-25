# audio_app/views.py
import pronouncing
import Levenshtein
from django.shortcuts import get_object_or_404, render, redirect
from .models import AudioFile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import speech_recognition as sr
import os


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
        return render(request, 'listen.html')
        #print("Request method is not POST")
    return JsonResponse({'error': 'Invalid request'}, status=400)


def record_audio(request):
    return render(request,'record.html')

def listen_audio(request):
    audio_files = AudioFile.objects.all()
    return render(request, 'listen.html', {'audio_files': audio_files})

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
    audio="static/recordings/important.wav"
    audiotest="static/recordings/important.wav"
    
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
    return render(request, 'evaluation.html', {'audio_url': audio_file.audio.url, 'audio_id': audio_id,'score':score})