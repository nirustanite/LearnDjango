
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from movielist_app.api.serializers import WatchSerializer, StreamPlatformSerializer, ReviewSerializer, SeriesSerializer
from movielist_app.models import WatchList, StreamPlatform, Reviews, Series
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework import status, generics, mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from movielist_app.api.permissions import ReviewUserOrReadOnly
# Create your views here.

#ModelViewSet
class SeriesModelViewSet(viewsets.ModelViewSet):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer

#ViewSets
class SeriesViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Series.objects.all()
        serializer = SeriesSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Series.objects.all()
        series = get_object_or_404(queryset, pk=pk)
        serializer = SeriesSerializer(series)
        return Response(serializer.data)

#Creating Review per WatchList
class CreateReviewPerWatchList(generics.CreateAPIView):
    serializer_class= ReviewSerializer
    
    def get_queryset(self):
        return Reviews.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        watchlist = WatchList.objects.get(pk=pk)
        review_user = self.request.user
        print(review_user)
        review_queryset = Reviews.objects.filter(watchlist = watchlist, review_user = review_user)
        print(review_queryset)
        if review_queryset:
            raise ValidationError("You have already reviewed this watchlist")
        
        if watchlist.number_rating == 0: 
            watchlist.avg_rating = serializer.validated_data["rating"]
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data["rating"])/2
        
        watchlist.number_rating += 1
        watchlist.save()
        serializer.save(watchlist=watchlist)

#Overwriting QuerySet
class ReviewPerWatchList(generics.ListAPIView):
    serializer_class= ReviewSerializer
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Reviews.objects.filter(watchlist = pk)

 
# Concrete View Classes   
class ReviewList(generics.ListCreateAPIView):
    queryset = Reviews.objects.all()
    serializer_class= ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reviews.objects.all()
    serializer_class= ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]

# Generic API VIEW and Mixins
class StreamPlatformAV(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
        
class StreamPlatformDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    
    def get(self, request, *args, **kwargs):
     return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
        
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

#class based views
class WatchListAV(APIView):
    
    def get(self, request):
        watchList = WatchList.objects.all()
        serializer = WatchSerializer(watchList, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class WatchDetailAV(APIView):
    
    def get(self, request, pk):
        try:
           watchList = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error': 'Movie Not Found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchSerializer(watchList)
        return Response(serializer.data)
    
    def put(self, request, pk):
       watchList = WatchList.objects.get(pk=pk)
       serializer = WatchSerializer(watchList, data=request.data)
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data)
       else:
           return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, pk):
        watchList = WatchList.objects.get(pk=pk)
        watchList.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)