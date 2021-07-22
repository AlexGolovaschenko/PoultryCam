from django.urls import path

from .views import HomePageView, PhotoListView
from .models import MARKER_NEW, MARKER_GOOD, MARKER_BAD, MARKER_SKIP

app_name = 'photos'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('photos/new/', PhotoListView.as_view(mark=MARKER_NEW), name='new'),
    path('photos/good/', PhotoListView.as_view(mark=MARKER_GOOD), name='good'),
    path('photos/bad/', PhotoListView.as_view(mark=MARKER_BAD), name='bad'),
    path('photos/skiped/', PhotoListView.as_view(mark=MARKER_SKIP), name='skiped'),
]
