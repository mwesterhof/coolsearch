from django.contrib import admin
from django.urls import include, path

from clubs import urls as clubs_urls
from main import urls as main_urls
from searcher import urls as searcher_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', include(searcher_urls)),
    path('clubs/', include(clubs_urls)),
    path('', include(main_urls)),
]
