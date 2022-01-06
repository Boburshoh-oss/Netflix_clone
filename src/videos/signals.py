from django.db.models.signals import pre_save
from django.utils.text import slugify

from playlists.models import PlayList
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

@receiver(pre_save,sender=Video)
def slugify_pre_save(sender,instance,*args,**kwargs):
    title = instance.title
    slug = instance.slug
    if slug is None:
        instance.slug = slugify(title)

pre_save.connect(slugify_pre_save,sender=PlayList)