from django.shortcuts import render
from generator import views
from django.core.paginator import Paginator
from . models import Song
from . models import Sound
from . models import Channel



# Create your views here.

    
def index(request):
    return render(request, 'index.html')

def piano_view(request):
    return render(request, 'piano.html')


def musicgen(request):
    return render(request, 'generatorv1.html')

def music_player(request):
    paginator = Paginator(Song.objects.all(), 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj}
    return render(request, "music_player.html", context)

    def __str__(self):
        return self.title

def channel_rack(request):
    channels = Channel.objects.all()
    return render(request, 'channel_rack.html', {'channels': channels})
