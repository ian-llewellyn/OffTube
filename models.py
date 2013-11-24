""" models.py for OffTube Project. """

from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
# Create your models here.


class Format(models.Model):
    """ Media formats are defined using instances of the Format class.
    A ffmpeg transcode string is provided to define how to convert to that
    target format.
    """
    name = models.CharField(max_length=20)
    transcode_string = models.CharField(max_length=1000)
    file_extension = models.CharField(max_length=10)

    def __unicode__(self):
        return self.name


class Video(models.Model):
    """ Video class
    An instance of this class relates to a particular source video. It can
    reference a number of target formats inherently through the ManyToMany
    'delivery_formats' field. """

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

    from django.db.models.signals import pre_delete
    from django.dispatch import receiver

    @receiver(pre_delete)
    def delete_files(sender, instance, **kwargs):
        """ Used primarily when deletes are called on Video objects. This method
            deletes the files associated with a Video. """
        if sender != Video:
            return
        import os
        from django.conf import settings
        media_root = settings.MEDIA_ROOT.rstrip(os.path.sep)

        # Build a list of files associated with this Video object
        associated_files = [instance.source_file.path]
        for fmt in instance.delivery_formats.all():
            extension = fmt.file_extension
            associated_files.append(os.path.sep.join(
                [media_root, getattr(instance, 'get_' + extension + '_file')]))

        # Deleta files associated with this Video object (if they exist)
        for f in associated_files:
            if os.path.exists(f):
                os.unlink(f)

    def get_format_func(fmt):
        """ Produce a function that returns the file for a given format. """
        def format_func(self):
            """ A functino that returns the file for a given format. """
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
        """ Based on the delivery formats associated with the Video,
        convert the video to each format in series. """
        import subprocess
        import os
        from django.conf import settings
        media_root = settings.MEDIA_ROOT

        input_file = self.source_file
        for delivery_format in self.delivery_formats.all():
            output_file = getattr(self,
              'get_' + delivery_format.file_extension + '_file')
            # Ensure the containing directory exists
            if not os.path.exists(os.path.dirname(media_root + output_file)):
                os.makedirs(os.path.dirname(media_root + output_file))
            # Prepare the command with substitutions
            command = delivery_format.transcode_string \
                .replace('%in_file%', input_file.name) \
                .replace('%out_file%', output_file)
            try:
                # Run the transcode command
                print command
                status = subprocess.call(command.split(' '), cwd=media_root)
            except:
                # Log an error if it fails
                print 'Return code: %d from command: %s' % (status, command)
        # Transcoding complete - the video is ready to be watched
        return True

    def __unicode__(self):
        # Example:
        # 2013-12-12T14:36:15: Ready: Clip of a Man on a Bridge
        return "%s: %s: %s" % (
            self.upload_date.ctime(), self.status, self.title)


class PartialVideoForm(ModelForm):
    """ We don't need to see all fields in the automgically generated
    Video submission form. """
    class Meta:
        """ Django suggests that we identify the fields we want to be
        visible in this way. """
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
