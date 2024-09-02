from django.http import HttpResponse
from django.shortcuts import render
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import urllib
from scipy.io.wavfile import write

# Create your views here.
def generate_sine_wave(frequency, duration=1, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    x = 0.5 * np.sin(2 * np.pi * frequency * t)
    return x, t

def index(request):
    frequency = float(request.GET.get('frequency', 440))
    x, t = generate_sine_wave(frequency)
    
    plt.figure()
    plt.plot(t, x)
    plt.title(f'Sine Wave at {frequency}')
    plt.xlabel('Time [s]')
    plt.ylabel('Amplitude')
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)
    
    audio_buf = io.BytesIO()
    write(audio_buf, 44100, x.astype(np.float32))
    audio_buf.seek(0)
    audio_string = base64.b64encode(audio_buf.read()).decode('utf-8')
    audio_uri = 'data:audio/wav;base64,' + audio_string
    
    context = {'image_uri': uri, 'audio_uri': audio_uri}
    return render(request, 'sinusoid/index.html', context)
    

