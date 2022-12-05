from rest_framework import serializers
from movielist_app.models import StreamPlatform, WatchList, Reviews


class ReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Reviews
        exclude=['watchlist']

class WatchSerializer(serializers.ModelSerializer):
    
    reviews = ReviewSerializer(many=True, read_only=True)
     
    len_names = serializers.SerializerMethodField()
     
    class Meta:
        model = WatchList
        fields = '__all__'
        
    def get_len_names(self, object):
        return len(object.title)
    
    def validate(self, data):
        if data['title'] == data['description']:
            raise serializers.ValidationError('Title and Description should be different!')
        else:
            return data
        
    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('Title is too short !!s')
        else:
            return value
        
        
class StreamPlatformSerializer(serializers.ModelSerializer):
    
    watchlist = WatchSerializer(many=True, read_only=True)
    
    # watchlist = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='watch-detail'
    # )
    
    class Meta:
        model = StreamPlatform
        fields = '__all__'
        