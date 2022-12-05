from django.contrib import admin
from movielist_app.models import WatchList, StreamPlatform, Reviews, Series

# Register your models here.
admin.site.register(WatchList)
admin.site.register(StreamPlatform)
admin.site.register(Reviews)
admin.site.register(Series)
