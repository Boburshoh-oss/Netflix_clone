from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from .models import TaggedItem
from django.db.utils import IntegrityError
from playlists.models import PlayList
from categories.models import Category

class TaggedItemTestCase(TestCase):
    def setUp(self):
        cat = Category.objects.first()
        self.ply_obj = PlayList.objects.create(title='New title',category=cat)

    def test_content_type_is_not_null(self):
        with self.assertRaises(IntegrityError):
            TaggedItem.objects.create(tag="my-new-tag")

    def test_create_via_content_type(self):
        c_type = ContentType.objects.get(app_label='playlists', model='playlist')
        tag_a = TaggedItem.objects.create(content_type=c_type, object_id=1, tag='new-tag')
        self.assertIsNotNone(tag_a.pk)
        tag_a = TaggedItem.objects.create(content_type=c_type, object_id=100, tag='new-tag2')
        self.assertIsNotNone(tag_a.pk)

    def test_create_via_model_content_type(self):
        c_type = ContentType.objects.get_for_model(PlayList)
        tag_a = TaggedItem.objects.create(content_type=c_type, object_id=1, tag='new-tag')
        self.assertIsNotNone(tag_a.pk)

    def test_create_via_model_content_type(self):
        PlayListKlass = apps.get_model(app_label='playlists',model_name='PlayList')
        c_type = ContentType.objects.get_for_model(PlayList)
        tag_a = TaggedItem.objects.create(content_type=c_type, object_id=1, tag='new-tag')
        self.assertIsNotNone(tag_a.pk)