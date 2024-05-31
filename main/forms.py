from django import forms
from .models import AudioFile, Word

class AudioFileForm(forms.ModelForm):
    class Meta:
        model = AudioFile
        fields = ['name', 'audio']
        

class WordSelectionForm(forms.Form): 
    def __init__(self, *args, **kwargs):
        super(WordSelectionForm, self).__init__(*args, **kwargs)
        levels = Word.objects.values_list('level', flat=True).distinct()
        for level in levels:
            words = Word.objects.filter(level=level)
            self.fields[f'level_{level}'] = forms.ModelMultipleChoiceField(
                queryset=words,
                required=False,
                label=f'Level {level}',
                widget=forms.CheckboxSelectMultiple
            )
            self.fields[f'new_word_level_{level}'] = forms.CharField(
                max_length=20,
                required=False,
                label=f'Add new word for Level {level}'
            )