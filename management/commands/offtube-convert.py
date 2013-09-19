""" This is the processing daemon for the OffTube project. """
from django.core.management.base import BaseCommand
from offtube.models import Video

from time import sleep

from django.conf import settings
MEDIA_ROOT = settings.MEDIA_ROOT

class Command(BaseCommand):
    """ Standard Django stuff here for the offtube-convert command. """
    def handle(*args, **kwargs):
        print args
        for arg in kwargs:
            print arg
        print MEDIA_ROOT
        while 1:
            jobs = Video.objects.filter(status='pending')

            if len(jobs) == 0:
                sleep(5)
                continue

            for video in jobs:
                if video.convert_all():
                    video.status = 'ready'
                    video.save()
