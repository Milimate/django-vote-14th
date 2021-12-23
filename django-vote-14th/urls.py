from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ceos-15th-partzzang/', include('signup.urls'))
]
