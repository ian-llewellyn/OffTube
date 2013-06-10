from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
# Create your models here.


class Format(models.Model):
    name = models.CharField(max_length=20)
    transcode_string = models.CharField(max_length=1000)
    file_extension = models.CharField(max_length=10)

    def __unicode__(self):
        return self.name


class Video(models.Model):
    STATUS_CHOICES = [("uploading", "Uploading"),
            ("transcoding", "Transcoding"),
            ("ready", "Ready"),
            ("pending", "Pending")]
    title = models.CharField(max_length=160, verbose_name="Video Title")
    upload_user = models.ForeignKey(User,
        help_text="The user that uploaded the video.")
    description = models.TextField(blank=True,
        help_text="An optional description for the video")
    source_file = models.FileField(upload_to='offtube/upload/%Y/%m%d/',
        help_text="The user-uploaded file")
    delivery_formats = models.ManyToManyField(Format, blank=False,
        help_text="Which formats are available for this video",
        default=[i.id for i in Format.objects.all()])
    upload_date = models.DateTimeField(auto_now_add=True,
        help_text="The dat and time the video was uploaded")
    #duration = models.PositiveIntegerField()
    #privacy_profile = models.ForeignKey(PrivacyProfile)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,
        help_text="The current status of the video file")
    hits = models.PositiveIntegerField(default=0,
        help_text="The number of views the video has received")
    # A field to measure popularity over time
    # - possibility a one-to-many relationship with a VideoTracker model

    def get_format_func(fmt):
        def format_func(self):
            if not self.upload_date:
                return None
            return 'offtube/%s/%s/%i.%s' % (fmt,
                self.upload_date.strftime('%Y/%m%d'),
                self.id, fmt)
        format_func.__name__ = 'get_' + str(fmt) + '_file'
        return format_func

    for fmt in Format.objects.all():
        extension = fmt.file_extension
        locals()['get_' + extension + '_file'] = property(
            get_format_func(extension))

    def convert_all(self):
        import subprocess
        import os
        from django.conf import settings
        MEDIA_ROOT = settings.MEDIA_ROOT

        input_file = self.source_file
        for delivery_format in self.delivery_formats.all():
            output_file = getattr(self,
              'get_' + delivery_format.file_extension + '_file')
            # Ensure the containing directory exists
            if not os.path.exists(os.path.dirname(MEDIA_ROOT + output_file)):
                os.makedirs(os.path.dirname(MEDIA_ROOT + output_file))
            # Prepare the command with substitutions
            command = delivery_format.transcode_string \
                .replace('%in_file%', input_file.name) \
                .replace('%out_file%', output_file)
            try:
                # Run the transcode command
                print command
                status = subprocess.call(command.split(' '), cwd=MEDIA_ROOT)
            except:
                # Log an error if it fails
                print 'Return code: %d from command: %s' % (status, command)
                pass
        # Transcoding complete - the video is ready to be watched
        return True

    def __unicode__(self):
        # Example:
        # 2013-12-12T14:36:15: Ready: Clip of a Man on a Bridge
        return "%s: %s: %s" % (
            self.upload_date.ctime(), self.status, self.title)


class PartialVideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'source_file', 'delivery_formats']

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
