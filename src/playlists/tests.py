from django.test import TestCase

from django.utils import timezone
from django.test import TestCase
from .models import PlayList,PublishStateOptions
from django.utils.text import slugify
from videos.models import Video


# Create your tests here.
class PlayListModelTestCase(TestCase):
    def create_show_with_seasons(self):
        the_office = PlayList.objects.create(title="The Office Series")
        season_1 = PlayList.objects.create(title="The Office Series season_1",parent=the_office,order=1)
        season_2 = PlayList.objects.create(title="The Office Series season_2",parent=the_office,order=1)
        season_2 = PlayList.objects.create(title="The Office Series season_3",parent=the_office,order=1)
        self.show = the_office
        
    def create_video(self):
        video_a = Video.objects.create(title="My title",video_id="abc123")
        video_b = Video.objects.create(title="My title",video_id="abc1")
        video_c = Video.objects.create(title="My title",video_id="abc2")
        self.video_a = video_a
        self.video_b = video_b
        self.video_c = video_c
        self.video_qs = Video.objects.all()
        
    def setUp(self):
        self.create_video()
        self.create_show_with_seasons()
        self.obj_a = PlayList.objects.create(title="This title for test", video=self.video_a)
        obj_b = PlayList.objects.create(title="This title\
        for test",state=PublishStateOptions.PUBLISH, video=self.
        video_a)
        obj_b.videos.set([self.video_a,self.video_b,self.video_c])
        obj_b.save()
        self.obj_b = obj_b
    
    def test_show_has_seasons(self):
        season = self.show.playlist_set.all()
        self.assertTrue(season.exists())
    
    def test_playlist_video_items(self):
        count = self.obj_b.videos.all().count()
        self.assertEqual(count,3)
        
    def test_playlist_video_through_model(self):
        v_qs = sorted(list(self.video_qs.values_list("id")))
        print(v_qs)
        video_qs = sorted(list(self.obj_b.videos.all().values_list("id")))
        playlist_item_qs = sorted(list(self.obj_b.playlistitem_set.all().values_list("id")))
        self.assertEqual(v_qs,video_qs,playlist_item_qs)
    
    def test_video_playlist(self):
        qs = self.video_a.featured_playlist.all()
        self.assertTrue(qs.count(),2)
        
    def test_video_playlist_ids_propery(self):
        ids = self.obj_a.video.get_playlist_ids()
        actual_ids = list(PlayList.objects.filter(video=self.video_a).
        values_list('title',flat=True)) 
        self.assertEqual(ids,actual_ids)
    
    def test_playlists_video(self):
        self.assertEqual(self.obj_a.video,self.video_a)
    
    def test_slug_field(self):  
        title = self.obj_a.title
        test_slug = slugify(title)
        self.assertEqual(test_slug,self.obj_a.slug)
        
    def test_valid_title(self):
        title = "This title for test"
        qs = PlayList.objects.filter(title=title)
        self.assertTrue(qs.exists())
        
    def test_created_count(self):
        qs = PlayList.objects.all()
        self.assertEqual(qs.count(),6)
        
    def test_draft_case(self):
        qs = PlayList.objects.filter(state=PublishStateOptions.DRAFT)
        self.assertEqual(qs.count(),5)
        
    def test_publish_case(self):
        qs = PlayList.objects.filter(state=PublishStateOptions.PUBLISH)
        now = timezone.now()
        published_qs = PlayList.objects.filter(
            state=PublishStateOptions.PUBLISH,
            publish_timestamp__lte=now
            )
        self.assertTrue(published_qs.exists())

    def test_publish_manager(self):
        published_qs = PlayList.objects.all().published()
        published_qs_2 = PlayList.objects.published()
        self.assertEqual(published_qs.count(),published_qs_2.count())