from django.urls import path, include
from rest_framework.routers import DefaultRouter
from movielist_app.api.views import (WatchListAV, WatchDetailAV, StreamPlatformAV,
                                     StreamPlatformDetail, ReviewList, ReviewDetail, 
                                     ReviewPerWatchList, CreateReviewPerWatchList,
                                     SeriesViewSet, SeriesModelViewSet)

router = DefaultRouter()
router.register('series-viewset', SeriesViewSet, basename='series-viewset-list')
router.register('series-list', SeriesModelViewSet, basename='series-list')

urlpatterns = [
    path('list/', WatchListAV.as_view(), name='watch-list'),
    path('<int:pk>', WatchDetailAV.as_view(), name='watch-detail'),
    path('', include(router.urls)),
    path('stream/', StreamPlatformAV.as_view(), name='stream'),
    path('stream/<int:pk>', StreamPlatformDetail.as_view(), name='stream-detail'),
    path('review/', ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>', ReviewDetail.as_view(), name='review-detail'),
    path('<int:pk>/review', ReviewPerWatchList.as_view(), name='review-per-watchlist'),
    path('<int:pk>/review-create', CreateReviewPerWatchList.as_view(), name='create-review-per-watchlist'),
]