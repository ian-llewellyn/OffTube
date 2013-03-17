# Create your views here.
from django.http import HttpResponse # Probably won't need this eventually
#from django.template import Context, loader
from django.shortcuts import render
from offtube.models import Video

def index(request):
    # Simplest way:
    #return HttpResponse("Hello World - I'm watching you.")

    # Verbose way:
    #latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
    #template = loader.get_template('polls/index.html')
    #context = Context({
    #    'latest_poll_list': latest_poll_list,
    #})
    #return HttpResponse(template.render(context))

    # The shortcut way:
    recent_uploads = Video.objects.all()[0:1]
    context = {'recent_uploads': recent_uploads}
    return render(request, 'offtube/index.html', context)

def play(request, **kwargs):
    if kwargs['video_id']:
        vid_id = kwargs['video_id']
        return HttpResponse("This is the play page for video: %s." % vid_id)
    return HttpResponse("Error: You need the video_id to play.")

def upload(request):
    return HttpResponse("This is the upload page.")

"""
From: http://www.360doc.com/content/10/0426/21/11586_25036463.shtml

def v_addvideo(request, submissionid):
    manipulator = VideoSubmission.AddManipulator()
    form = FormWrapper(manipulator,{},{})
    params = {'userAccount':request.user,'form':form,}
    c = Context(request, params)
    t = loader.get_template('video/addvideo.html')
    sub = Submission.objects.get(pk=submissionid)
    params['submission'] = sub
    return HttpResponse( t.render( c ) )
"""
