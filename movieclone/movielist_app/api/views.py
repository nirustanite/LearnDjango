from django.shortcuts import render
from movielist_app.api.serializers import WatchSerializer, StreamPlatformSerializer, ReviewSerializer
from movielist_app.models import WatchList, StreamPlatform, Reviews
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics, mixins

# Create your views here.
 
# Concrete View Classes   
class ReviewList(generics.ListCreateAPIView):
    queryset = Reviews.objects.all()
    serializer_class= ReviewSerializer
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reviews.objects.all()
    serializer_class= ReviewSerializer



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