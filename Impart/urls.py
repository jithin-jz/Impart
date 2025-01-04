
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
]

from django.urls import include
urlpatterns += [path('', include('accounts.urls'))]
