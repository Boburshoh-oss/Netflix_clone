from django.test import TestCase
from django.contrib.auth import get_user_model
import random
from playlists.models import PlayList
from .models import Rating, RatingChoices
from django.db.models import Avg

# Create your tests here.

User = get_user_model()

class RatingTestCase(TestCase):
    def create_playlist(self):
        items = []
        self.playlist_count = random.randint(10,500)
        for i in range(0,self.playlist_count):
            items.append(PlayList(title=f'TV show_{i}'))
        PlayList.objects.bulk_create(items)
        self.playlists = PlayList.objects.all()

    def create_users(self):
        items = []
        self.user_count = random.randint(10,500)
        for i in range(0,self.user_count):
            items.append(User(username=f'user_{i}'))
        User.objects.bulk_create(items)
        self.users = User.objects.all()

    def create_ratings(self):
        items = []
        self.rating_totals = []
        self.rating_count = 1000
        for i in range(0,self.rating_count):
            user_obj = self.users.order_by("?").first()
            ply_obj = self.playlists.order_by("?").first()
            rating_value = random.choice(RatingChoices.choices)[0]
            if rating_value is not None:
                self.rating_totals.append(rating_value)
            items.append(
                Rating(
                    user=user_obj,
                    content_object=ply_obj,
                    value=rating_value
                )
            )
        Rating.objects.bulk_create(items)
        self.ratings = Rating.objects.all()

    def setUp(self):
        self.create_users()
        self.create_playlist()
        self.create_ratings()

    def test_user_count(self):
        qs = User.objects.all()
        self.assertTrue(qs.exists())
        self.assertEqual(qs.count(),self.user_count)
        self.assertEqual(self.users.count(),self.user_count)
    
    def test_playlist_count(self):
        qs = PlayList.objects.all()
        self.assertTrue(qs.exists())
        self.assertEqual(qs.count(),self.playlist_count)
        self.assertEqual(self.playlists.count(),self.playlist_count)

    def test_rating_count(self):
        qs = Rating.objects.all()
        self.assertTrue(qs.exists())
        self.assertEqual(qs.count(),self.rating_count)
        self.assertEqual(self.ratings.count(),self.rating_count)
    
    def test_rating_random_choices(self):
        value_set = set(Rating.objects.values_list('value',flat=True))
        self.assertTrue(len(value_set)>1)
    
    def test_rating_agg(self):
        db_avg = Rating.objects.aggregate(Avg('value'))['value__avg']
        self.assertIsNotNone(db_avg)
        self.assertTrue(db_avg>0)
        total_sum = sum(self.rating_totals)
        passed_avg = total_sum / (len(self.rating_totals)*1)
        self.assertEqual(passed_avg,db_avg)
    
    def test_rating_playlist_agg(self):
        item_1 = PlayList.objects.aggregate(average=Avg('ratings__value'))['average']
        self.assertIsNotNone(item_1)
        self.assertTrue(item_1>0)