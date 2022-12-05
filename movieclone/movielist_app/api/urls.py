from django.urls import path, include
from movielist_app.api.views import MovieListAV, MovieDetailAV

urlpatterns = [
    path('list/', MovieListAV.as_view(), name='movie-list'),
    path('<int:pk>', MovieDetailAV.as_view(), name='movie-detail')
]