from django.db import models
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.
class PublishStateOptions(models.TextChoices):
        PUBLISH = "PU", "Publish"
        DRAFT = 'DR', 'Draft'
        # UNLISTED = 'UN', 'Unlisted'
        # PRIVATE = 'PR', 'Private'

class VideoQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            state=PublishStateOptions.PUBLISH,
            publish_timestamp__lte = now
        )

class VideoManager(models.Manager):
    def get_queryset(self):
        return VideoQuerySet(self.model,using=self._db) 
    
    def published(self):
        return self.get_queryset().published()
        
class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    video_id = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=2, choices=PublishStateOptions.choices, default=PublishStateOptions.DRAFT)
    publish_timestamp = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    
    objects = VideoManager()
    
    def __str__(self):
        return self.title
    
    @property
    def is_published(self):
        if self.active is False:
            return False
        if self.state != PublishStateOptions.PUBLISH:
            return False
        pub_timestamp = self.publish_timestamp
        if pub_timestamp is None:
            return False
        now = timezone.now()
        return pub_timestamp <=now
    
    def get_video_id(self):
        if not self.is_published:
            return None
        return self.video_id

    def get_playlist_ids(self):
        #self <foreigned_obj>_set.all()
        lists = list(self.featured_playlist.all().values_list("title",flat=True))
        return lists
    
    def save(self, *args, **kwargs):     
        if self.state == PublishStateOptions.PUBLISH and self.publish_timestamp is None:
            self.publish_timestamp = timezone.now()
        elif self.state == PublishStateOptions.DRAFT:
               self.publish_timestamp = None

        return super().save(*args,**kwargs)
    
class VideoAllProxy(Video):
    class Meta:
        proxy = True
        verbose_name = "All Video"
        verbose_name_plural = "All Videos"

class VideoPublishedProxy(Video):
    class Meta:
        proxy = True
        verbose_name = "Published Video"
        verbose_name_plural = "Published Videos"

