from django.core.management.base import BaseCommand, CommandError
from offtube.models import Video

from time import sleep
from subprocess import call

import os

from django.conf import settings
MEDIA_ROOT = settings.MEDIA_ROOT

class Command(BaseCommand):
    def handle(*args, **kwargs):
        print args
        for arg in kwargs:
            print arg
        print MEDIA_ROOT
        while 1:
            jobs = Video.objects.filter(status='Pending')

            if len(jobs) == 0:
                sleep(5)
                continue

            for video in jobs:
                os_src_file = MEDIA_ROOT + video.video_file_src.name
                os_thumb_file = MEDIA_ROOT + video.thumbnail
                os_out_file = MEDIA_ROOT + video.video_file_ogg

                # Create the thumbnail container directory
                if not os.path.exists(os.path.dirname(os_thumb_file)):
                    os.makedirs(os.path.dirname(os_thumb_file))

                # Create thumbnail
                ffmpeg = "ffmpeg -y -i %s -vframes 1 -ss 00:00:10 -an -vcodec png -f rawvideo -s 320x180 %s" % (os_src_file, os_thumb_file)
                status = call(ffmpeg.split(' '))
                print "Thumbnail return status: %d" % status

                # Create the output container directory
                if not os.path.exists(os.path.dirname(os_out_file)):
                    os.makedirs(os.path.dirname(os_out_file))

                # Create ogg video
                ffmpeg = "ffmpeg -y -i %s -r 25 -b 2M -bt 4M -vcodec libx264 -strict experimental -acodec aac -ac 2 -ar 48000 -ab 192k -f mp4 %s" % (os_src_file, os_out_file)
                print ffmpeg
                try:
                    status = call(ffmpeg.split(' '))
                except:
                    pass
                else:
                    print "Main ffmpeg return status: %d" % status
                    video.status = 'Ready'
                    video.save()
"""
    if video is None:
        return "Kein Video im Upload gefunden"

    filename = video.videoupload
    print "Konvertiere Quelldatei: %s" + filename
    if filename is None:
        return "Video mit unbekanntem Dateinamen"

    sourcefile = "%s%s" % (settings.MEDIA_ROOT,filename)
    flvfilename = "%s.flv" % video.id
    thumbnailfilename = "%svideos/flv/%s.png" % (settings.MEDIA_ROOT, video.id)
    targetfile = "%svideos/flv/%s" % (settings.MEDIA_ROOT, flvfilename)
    ffmpeg = "ffmpeg -i %s -acodec mp3 -ar 22050 -ab 32 -f flv -s 320x240 %s" % (sourcefile,  targetfile)
    grabimage = "ffmpeg -y -i %s -vframes 1 -ss 00:00:02 -an -vcodec png -f rawvideo -s 320x240 %s " % (sourcefile, thumbnailfilename)
    flvtool = "flvtool2 -U %s" % targetfile
    print ("Source : %s" % sourcefile)
    print ("Target : %s" % targetfile)
    print ("FFMPEG: %s" % ffmpeg)
    print ("FLVTOOL: %s" % flvtool)

    try:
        ffmpegresult = commands.getoutput(ffmpeg)
        print "-------------------- FFMPEG ------------------"
        print ffmpegresult

        # Check if file exists and is > 0 Bytes
        try:
            s = os.stat(targetfile)
            print s
            fsize = s.st_size
            if (fsize == 0):
                print "File is 0 Bytes gross"
                os.remove(targetfile)
                return ffmpegresult

            print "Dateigroesse ist %i" % fsize

        except:
            print sys.exc_info()
            print "File %s scheint nicht zu existieren" % targetfile
            return ffmpegresult

        flvresult = commands.getoutput(flvtool)
        print "-------------------- FLVTOOL ------------------"
        print flvresult
        grab = commands.getoutput(grabimage)
        print "-------------------- GRAB IMAGE ------------------"
        print grab

    except:
        print sys.exc_info()
        return sys.exc_info[1]

    video.flvfilename = flvfilename
    video.save()
    return None"""
