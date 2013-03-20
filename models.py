from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from time import strftime
from os.path import splitext
# Create your models here.

class Video(models.Model):
    title = models.CharField(max_length=160, verbose_name="Video Title")
    upload_user = models.ForeignKey(User,
        help_text="The user that uploaded the video.")
    description = models.TextField(blank=True,
        help_text="An optional description for the video")
    thumbnail = models.CharField(max_length=100,
        help_text="An automatically generated thumbnail for the video")
    video_file_ogg = models.CharField(max_length=100,
        help_text="The transmografied file - ready for consumption")
    video_file_src = models.FileField(upload_to='offtube/upload/%Y/%m%d/',
        help_text="The user-uploaded file")
    upload_date = models.DateTimeField(auto_now_add=True,
        help_text="The dat and time the video was uploaded")
    #duration = models.PositiveIntegerField()
    hits = models.PositiveIntegerField(default=0,
        help_text="The number of views the video has received")
    #privacy_profile = models.ForeignKey(PrivacyProfile)
    status = models.CharField(max_length=20,
        help_text="The current status of the video file",
        choices=[("Uploading", "Uploading"),
            ("Transcoding", "Transcoding"),
            ("Ready", "Ready"),
            ("Pending", "Pending")])
    # A field to measure popularity over time
    # - possibility a one-to-many relationship with a VideoTracker model

    def get_location(self, extension):
        # Put offtube/ogg/%Y/%m%d/ at the start
        datepart = strftime('%Y/%m%d')
        output_file = 'offtube/%s/%s/%s' % (extension, datepart, self.video_file_src)
        # Strip .* from the end
        output_file = splitext(output_file)[0]
        # Put .ogg at the end
        output_file += '.' + extension
        return output_file

    def __unicode__(self):
        # Example:
        # 2013-12-12T14:36:15: Ready: Clip of a Man on a Bridge
        return "%s: %s: %s" % (self.upload_date.ctime(), self.status, self.title)

class PartialVideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file_src']

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
