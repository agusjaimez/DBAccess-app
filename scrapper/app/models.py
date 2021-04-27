from django.db import models
from .scrap import search

# Create your models here.
class ImageRoom(models.Model):
    url = models.URLField(unique=True)
    alt = models.CharField(max_length = 30, null = True)
    room = models.ForeignKey('Room', on_delete = models.CASCADE)

    def __str__(self) -> str:
        return f'{self.url}'


class Room(models.Model):
    nombre = models.CharField(unique=True ,max_length=100)
    tamaño = models.FloatField()
    facilidades = models.TextField()
    hotel = models.ForeignKey('Hotel', on_delete = models.CASCADE)

    def __str__(self) -> str:
        return f'{self.nombre}'

class ImageHotel(models.Model):
    url = models.URLField()
    alt = models.CharField(max_length=30, null=True)
    hotel = models.ForeignKey('Hotel', on_delete = models.CASCADE)
    
    def __str__(self) -> str:
        return f'{self.url}'

        

class Hotel(models.Model):
    url = models.URLField()
    nombre = models.CharField(max_length=100, null=True, blank=True)
    ubicacion = models.CharField(max_length=100, null=True, blank=True)
    puntuacion = models.FloatField(null=True, blank=True)
    cant_reviews = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.nombre}'
    
    def get_data(self):
        return search(self.url)

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        response = self.get_data()
        self.nombre = response['nombre']
        self.ubicacion = response['ubicacion']
        fotos = []
        for foto in response['fotos1']:
            fotos.append(ImageHotel(url=foto, hotel=self))
        ImageHotel.objects.bulk_create(fotos, ignore_conflicts=True)
        self.puntuacion = float(response['puntuacion'].replace(',', '.'))
        self.cant_reviews = int(response['cant_puntuaciones'])
        fotos_room=[]
        for room in response['habitaciones']:
            facilities=''
            for i in room['facilidades']:
                facilities += i+', '
            facilities = facilities[:-1]
            try:
                room_obj=Room.objects.create(nombre=room['nombre'],tamaño=float(room['tamaño'][0]),facilidades=facilities, hotel=self)
                for foto in room['fotos']:
                    fotos_room.append(ImageRoom(url=foto, room=room_obj))
                ImageRoom.objects.bulk_create(fotos_room,ignore_conflicts=True)
            except:
                print('No hay Habitaciones para mostrar')
        super().save(*args, **kwargs)

