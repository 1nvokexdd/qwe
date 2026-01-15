# repertoire/admin.py
from django.contrib import admin
from .models import Genre, MusicTrack, Hall, Host, WeekDay, Repertoire

# Простые модели (справочники)
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ['name', 'capacity']
    list_editable = ['capacity']
    search_fields = ['name']

@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    list_display = ['name', 'experience']
    list_editable = ['experience']
    search_fields = ['name']

@admin.register(WeekDay)
class WeekDayAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    list_editable = ['order']
    ordering = ['order']

# Музыкальные треки
@admin.register(MusicTrack)
class MusicTrackAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'genre', 'duration']
    list_filter = ['genre']
    search_fields = ['title', 'artist']
    list_editable = ['artist', 'genre']
    
    # Группировка полей в форме редактирования
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'artist', 'genre')
        }),
        ('Дополнительно', {
            'fields': ('duration', 'bpm'),
            'classes': ('collapse',)  # Сворачиваемая секция
        }),
    )

# Репертуар - основная таблица
@admin.register(Repertoire)
class RepertoireAdmin(admin.ModelAdmin):
    list_display = ['date', 'day', 'hall', 'host', 'music_track', 'start_time', 'end_time']
    list_filter = ['date', 'day', 'hall', 'host']
    search_fields = ['music_track__title', 'music_track__artist']
    date_hierarchy = 'date'
    
    # Поля для быстрого редактирования в списке
    list_editable = ['start_time', 'end_time']
    
    # Группировка полей в форме
    fieldsets = (
        ('Время и место', {
            'fields': ('date', 'day', 'hall', 'start_time', 'end_time')
        }),
        ('Участники', {
            'fields': ('host', 'music_track')
        }),
    )
    
    # Автозаполнение поля дня недели на основе даты
    def save_model(self, request, obj, form, change):
        if obj.date:
            # Можно добавить автоматическое определение дня недели
            pass
        super().save_model(request, obj, form, change)
