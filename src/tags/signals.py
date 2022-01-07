from django.db.models.signals import pre_save
from django.utils.text import slugify

from playlists.models import PlayList
from .models import TaggedItem
from django.utils import timezone
from django.dispatch import receiver


