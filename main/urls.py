from django.urls import path

from .views import JobDetail, PersonDetail, HomeView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('person/<int:pk>/', PersonDetail.as_view(), name='person_detail'),
    path('job/<int:pk>/', JobDetail.as_view(), name='job_detail'),
]
