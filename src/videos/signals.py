from django.db.models.signals import pre_save
from django.utils.text import slugify
from playlists.utils import get_unique_slug
from playlists.models import PlayList,MovieProxy,TVShowProxy,TVShowSeasonProxy
from .models import PublishStateOptions, Video
from django.utils import timezone
from django.dispatch import receiver


# @receiver(pre_save,sender=Video)
# def publish_state_pre_save(sender,instance, *args,**kwargs):
#     is_publish = instance.state = PublishStateOptions.PUBLISH
#     is_draft = instance.state = PublishStateOptions.DRAFT
    
#     if (instance.state == PublishStateOptions.PUBLISH) and (instance.publish_timestamp is None):
#         print("save as timestamp for published")
#         instance.publish_timestamp = timezone.now()
        
#     elif instance.state == PublishStateOptions.DRAFT:
#         instance.publish_timestamp = None


def slugify_pre_save(sender,instance,*args,**kwargs):
    title = instance.title
    slug = instance.slug
    if slug is None:
        instance.slug = slugify(title)

@receiver(pre_save,sender=Video)
def unique_slugify_pre_save(sender,instance,*args,**kwargs):
    title = instance.title
    slug = instance.slug
    if slug is None:
        instance.slug = get_unique_slug(instance,size=5)

pre_save.connect(unique_slugify_pre_save,sender=PlayList)
pre_save.connect(unique_slugify_pre_save,sender=MovieProxy)
pre_save.connect(unique_slugify_pre_save,sender=TVShowProxy)
pre_save.connect(unique_slugify_pre_save,sender=TVShowSeasonProxy)