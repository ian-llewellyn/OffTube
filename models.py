from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Video(models.Model):
    title = models.CharField(max_length=160)
    upload_user = models.ForeignKey(User)
    description = models.TextField(blank=True)
    thumbnail = models.CharField(max_length=100)
    video_file_ogg = models.CharField(max_length=100)
    video_file_src = models.FileField(upload_to='offtube/%Y/%m%d/')
    upload_date = models.DateTimeField(auto_now_add=True)
    hits = models.PositiveIntegerField(default=0)
    #privacy_profile = models.ForeignKey(PrivacyProfile)
    status = models.CharField(max_length=20, choices=[("Uploading", "Uploading"), ("Transcoding", "Transcoding"), ("Ready", "Ready"), ("Pending", "Pending")])
    # A field to measure popularity over time
    # - possibility a one-to-many relationship with a VideoTracker model
    def __unicode__(self):
        # Example:
        # 2013-12-12T14:36:15: Ready: Clip of a Man on a Bridge
        return "%s: %s: %s" % (self.upload_date.ctime(), self.status, self.title)

#class VideoStatsTracker(models.Model):
#    viewer_ip = models.IPAddressField()
#    date = models.DateTimeField()
#    duration = models.PositiveIntegerField()

#class PrivacyProfile(models.Model):
#    title = models.CharField(max_length=160)
#    description = models.TextField(blank=True)

#class UploadQueue(models.Model):
#    pass
"""
From: http://www.360doc.com/content/10/0426/21/11586_25036463.shtml

class VideoSubmission(models.Model):
    videoupload = models.FileField (upload_to='videoupload')
    relatedsubmission = models.ForeignKey(Submission, null=True)
    comment = models.CharField( maxlength=250, blank=True )
    flvfilename = models.CharField( maxlength=250, blank=True, null=True )
"""
