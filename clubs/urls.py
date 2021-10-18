from django.urls import path

from .views import ClubDetail, ClubMemberDetail


urlpatterns = [
    path('club/<int:pk>/', ClubDetail.as_view(), name='club_detail'),
    path('member/<int:pk>/', ClubMemberDetail.as_view(), name='clubmember_detail'),
]
