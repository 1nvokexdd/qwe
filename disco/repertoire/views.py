# views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView
from .models import Repertoire, MusicTrack, Genre
from .forms import RepertoireForm, SearchForm
from django.utils import timezone

class RepertoireListView(ListView):
    model = Repertoire
    template_name = 'disco/repertoire_list.html'
    context_object_name = 'repertoire'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Repertoire.objects.all().order_by('date', 'start_time')
        
        date_filter = self.request.GET.get('date')
        if date_filter:
            queryset = queryset.filter(date=date_filter)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm(self.request.GET or None)
        return context

class RepertoireCreateView(CreateView):
    """Добавление новой записи в репертуар"""
    model = Repertoire
    form_class = RepertoireForm
    template_name = 'disco/repertoire_form.html'
    success_url = '/repertoire/'

def repertoire_search(request):
    """Расширенный поиск по репертуару"""
    form = SearchForm(request.GET or None)
    repertoire = Repertoire.objects.all()
    
    if form.is_valid():
        genre = form.cleaned_data.get('genre')
        date = form.cleaned_data.get('date')
        hall = form.cleaned_data.get('hall')
        
        if genre:
            repertoire = repertoire.filter(music_track__genre=genre)
        if date:
            repertoire = repertoire.filter(date=date)
        if hall:
            repertoire = repertoire.filter(hall=hall)
    
    context = {
        'form': form,
        'repertoire': repertoire.order_by('date', 'start_time'),
    }
    return render(request, 'disco/repertoire_search.html', context)

class MusicTrackListView(ListView):
    """Список музыкальных произведений"""
    model = MusicTrack
    template_name = 'disco/music_tracks.html'
    context_object_name = 'tracks'
    
    def get_queryset(self):
        genre_id = self.request.GET.get('genre')
        if genre_id:
            return MusicTrack.objects.filter(genre_id=genre_id)
        return MusicTrack.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        return context

def dashboard(request):
    """Главная страница - дашборд"""
    today_repertoire = Repertoire.objects.filter(date=timezone.now().date())
    upcoming_events = Repertoire.objects.filter(date__gt=timezone.now().date())[:5]
    
    context = {
        'today_repertoire': today_repertoire,
        'upcoming_events': upcoming_events,
        'total_tracks': MusicTrack.objects.count(),
    }
    return render(request, 'disco/dashboard.html', context)
