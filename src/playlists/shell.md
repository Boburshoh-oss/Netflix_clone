from playlists.models import PlayList
from videos.models import Video

video_a = Video.objects.create(title="My title",video_id="abc123")
playlist_a = PlayList.objects.create(title="This title for test", video=video_a)

obj = PlayList.objects.first()
obj.playlistitem_set.all()
