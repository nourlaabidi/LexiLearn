# audio_app/views.py
from gtts import gTTS
import pronouncing
import Levenshtein
from django.shortcuts import get_object_or_404, render, redirect

from record_vocal import settings
from .models import AudioFile, Word
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import speech_recognition as sr
import os

@csrf_exempt
def record_audio(request, word_id):
    word = get_object_or_404(Word, pk=word_id)
    language = 'en'
    print("My Text:", word.word)
    output = gTTS(text=word.word, lang=language, slow=False)
    file_name = f'{word_id}_output.wav'
    file_path = os.path.join('/static/recordings/', file_name)
    
    print("File path:", file_path)  # Add logging
    
    try:
        output.save(file_path)
        print("Audio has been saved at:", file_path)
        word.word_vocal = file_path
        word.save()
    except Exception as e:
        print("Error saving audio file:", str(e))  
    
    return render(request, 'record.html', {'word': word, 'audio_path': file_path})

def home_page(request):
    return render(request,'home_page.html')

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
    print("test 1 ")
    audio_file = get_object_or_404(AudioFile, id=audio_id)
    word = get_object_or_404(AudioFile, pk=5)
    recognizer = sr.Recognizer()
    audio_path = os.path.join(settings.MEDIA_ROOT, audio_file.audio.name)
    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            voice1 = recognizer.recognize_google(audio_data, language='en')
        print("Voice 1:", voice1)

        transcription_mot_attendu = pronouncing.phones_for_word(voice1)
        transcription_audio_enregistre = pronouncing.phones_for_word(word.word)
        similarite = Levenshtein.distance(transcription_mot_attendu[0], transcription_audio_enregistre[0])
        score = 75
        audio_file.score = score
        audio_file.save()
        print("word 1", transcription_audio_enregistre)
        print("word 2", transcription_mot_attendu)
        print("score", score)
    except Exception as e:
        print("Error processing audio file:", str(e))
        score = 0
    print("test 2 ")
    return render(request, 'evaluation.html', {
        'audio_url': audio_file.audio.url,
        'audio_id': audio_id,
        'score': score,
        'word': word
    })
def list_words(request):
    words = Word.objects.all()
    return render(request,'list_words.html', {'words': words})

