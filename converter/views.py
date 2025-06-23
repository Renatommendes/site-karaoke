from django.shortcuts import render
from .forms import YouTubeForm
from .utils import baixar_audio, alterar_tom

def home(request):
    audio_url = None
    if request.method == 'POST':
        form = YouTubeForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            pitch = form.cleaned_data['pitch_shift']
            caminho = baixar_audio(url)
            if pitch != 0:
                caminho = alterar_tom(caminho, pitch)
            audio_url = caminho.replace('media/', '/media/')
    else:
        form = YouTubeForm()
    return render(request, 'converter/home.html', {'form': form, 'audio_url': audio_url})
