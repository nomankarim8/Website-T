# gallery/models.py

from django.db import models
from django.contrib.auth.models import User

class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.id}"
# gallery/admin.py

from django.contrib import admin
from .models import Photo

admin.site.register(Photo)
# gallery/forms.py

from django import forms
from .models import Photo

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']
# gallery/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PhotoForm
from .models import Photo

@login_required
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            return redirect('gallery:photo_list')
    else:
        form = PhotoForm()
    return render(request, 'gallery/upload_photo.html', {'form': form})

@login_required
def photo_list(request):
    photos = Photo.objects.filter(user=request.user)[:20]
    return render(request, 'gallery/photo_list.html', {'photos': photos})
# gallery/urls.py

from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('upload/', views.upload_photo, name='upload_photo'),
    path('photos/', views.photo_list, name='photo_list'),
]
# photo_album/urls.py

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gallery/', include('gallery.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# photo_album/settings.py

import os

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Login redirection
LOGIN_REDIRECT_URL = 'gallery:photo_list'
LOGOUT_REDIRECT_URL = '/'
