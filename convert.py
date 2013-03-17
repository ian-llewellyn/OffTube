def convertvideo (video):
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
        # Check if file exists and is &gt; 0 Bytes
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
    return None
