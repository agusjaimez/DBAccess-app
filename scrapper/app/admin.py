from django.contrib import admin
from app.models import Hotel, Room, ImageHotel, ImageRoom
from django.utils.html import format_html

# Register your models here.
class ImageHotelInline(admin.TabularInline):
    model = ImageHotel
    readonly_fields=('url','alt','get_image')
    extra=0
    max_num=0
    can_delete = False

    def get_image(self,obj):    
        return format_html(f'<img style="object-fit: contain; width: 500px" src="{obj.url}">')


class ImageRoomInline(admin.ModelAdmin):
    model = ImageRoom
    readonly_fields=('url','alt','get_image')
    extra=0
    max_num=0
    can_delete = False

    def get_image(self,obj):    
        return format_html(f'<img style="object-fit: contain; width: 400px" src="{obj.url}">')


class RoomInline(admin.TabularInline):
    model = Room
    readonly_fields = ('nombre','get_size','facilidades','get_images')
    exclude=('tamaño',)
    extra = 0
    max_num = 0
    can_delete = False
    inlines=(ImageRoomInline,)

    def get_size(self, obj) -> str:
        return f'{obj.tamaño} m²'
    
    def get_images(self,obj):
        images_url=[]
        for imagen in ImageRoom.objects.filter(room=obj):
            images_url.append(f'<img style="object-fit: contain; width: 100px;" src="{imagen.url}" />')
        return format_html(''.join(images_url))

class ImageHotelAdmin(admin.ModelAdmin):
    pass

class HotelAdmin(admin.ModelAdmin):
    inlines = (ImageHotelInline, RoomInline)

class RoomAdmin(admin.ModelAdmin):
    pass

admin.site.register(ImageHotel, ImageHotelAdmin)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(Room, RoomAdmin)