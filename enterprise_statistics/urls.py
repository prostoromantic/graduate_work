from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainpage.urls'))
]

handler404 = "mainpage.views.page_not_found_view"