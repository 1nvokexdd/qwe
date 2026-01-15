from operator import mod
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100 , verbose_name = "Название жанра")

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return f"{self.name}"


class  MusicTrack(models.Model):
    title = models.CharField(max_length=100, verbose_name = "Название трека")
    artist  = models.CharField(max_length=100,verbose_name = "Исполнитель")
    genre = models.ForeignKey(Genre , on_delete=models.CASCADE , verbose_name = "Жанр")
    duration = models.DurationField(verbose_name="Длительность",null=True,blank=True)
    bpm = models.IntegerField(verbose_name="BPN" , null=True , blank=True)

    class Meta:
        verbose_name = "Музыкальное произведение"
        verbose_name_plural = "Музыкальные произведения"

    def __str__(self):
        return f"{self.artist} - {self.title}"


class Hall(models.Model):
    name = models.CharField(max_length = 100 , verbose_name = "Название зала")
    capacity = models.IntegerField(verbose_name="Вместимость",null=True,blank=True)


    class Meta:
        verbose_name = "Зал"
        verbose_name_plural = "Залы"


    def __str__(self):
        return f"{self.name}"

class Host(models.Model):
    name  = models.CharField(max_length = 100 , verbose_name = "Имя ведущего")
    experience = models.IntegerField(verbose_name="Опыт (лет)",null=True,blank=True)

    class Meta:
        verbose_name = "Ведущий"
        verbose_name_plural =  "Ведущии"


    def __str__(self):
        return f"{self.name}"


class WeekDay(models.Model):
    name = models.CharField(max_length = 20 , verbose_name = "День недели")
    order  = models.IntegerField(verbose_name="Порядок",unique=True)


    class Meta:
        verbose_name = "День недели"
        verbose_name_plural = "Дни недели"
        ordering = ['order']

    def __str__(self):
        return f"{self.name}" 


class Repertoire(models.Model):
    music_track = models.ForeignKey(MusicTrack , on_delete=models.CASCADE , verbose_name = "Музыкальное произведение")
    hall = models.ForeignKey(Hall , on_delete=models.CASCADE , verbose_name = "Зал")
    host = models.ForeignKey(Host , on_delete=models.CASCADE , verbose_name = "Ведущии")
    day  = models.ForeignKey(WeekDay , on_delete=models.CASCADE , verbose_name = "День недели")
    start_time = models.TimeField(verbose_name="Время начала")
    end_time = models.TimeField(verbose_name="Время окончания")
    date = models.DateField(verbose_name="Дата")


    class Meta:
        verbose_name = "Репертуар"
        verbose_name_plural = "Репертуары"

    def __str__(self):
        return f"{self.date} - {self.music_track} - {self.hall}"
