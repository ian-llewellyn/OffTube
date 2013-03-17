from django.db import models

# Create your models here.

class Video(models.Model):
    title
    uploader
    description
    thumbnail
    video_file

class UploadQueue(models.Model):
    
"""
From: http://www.360doc.com/content/10/0426/21/11586_25036463.shtml

class VideoSubmission(models.Model):
    videoupload = models.FileField (upload_to='videoupload')
    relatedsubmission = models.ForeignKey(Submission, null=True)
    comment = models.CharField( maxlength=250, blank=True )
    flvfilename = models.CharField( maxlength=250, blank=True, null=True )
"""
