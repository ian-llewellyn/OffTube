# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
#from django.template import Context, loader
from django.shortcuts import render
from offtube.models import Video, PartialVideoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as djlogout

def logout(request):
    djlogout(request)
    return HttpResponseRedirect('/offtube/')

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
    recent_uploads = Video.objects.order_by('-upload_date').exclude(status='pending') # FIXME: Limit required here.
    context = {'recent_uploads': recent_uploads, 'request': request}
    return render(request, 'offtube/index.html', context)

def play(request, **kwargs):
    if not kwargs['video_id']:
        return HttpResponse('Error: You need the video_id to play.')
    vid_id = kwargs['video_id']
    try:
        video = Video.objects.get(id=vid_id)
    except Video.DoesNotExist:
        return HttpResponseNotFound('Nope.')
    try:
        referer = request.META['HTTP_REFERER']
    except KeyError:
        referer = None
    video.hits += 1
    video.save()
    context = {'video': video, 'request': request, 'referer': referer}
    if request.path.split('/')[-2] == 'play':
        return render(request, 'offtube/play.html', context)
    if request.path.split('/')[-2] == 'embed':
        return render(request, 'offtube/embed.html', context)

def search(request):
    msg = ''
    if not request.GET.has_key('q'):
        return HttpResponseRedirect('/offtube/')
    vids = Video.objects.filter(title__icontains=request.GET['q'].lower())
    context = {'results': vids, 'request': request}
    return render(request, 'offtube/list.html', context)

def popular(request, **kwargs):
    if kwargs['period']:
        from datetime import datetime, timedelta

        cutoff = datetime.now() - timedelta(days=int(kwargs['period']))
        vids = Video.objects.filter(upload_date__gte=cutoff).order_by('-hits')
    else:
        vids = Video.objects.order_by('-hits')

    context = {'results': vids, 'request': request}
    return render(request, 'offtube/list.html', context)

# FIXME: Looks ugly - is there a better way to do this?
@login_required(login_url='../login/')
def upload(request):
    if request.method == 'POST':
        # The form has been submitted...
        form = PartialVideoForm(request.POST, request.FILES)
        if form.is_valid():
            # The form is valid
            video = form.save(commit=False)
            video.upload_user = request.user
            video.status = 'pending'
            video.save()
            form.save_m2m()
            print video
            return HttpResponseRedirect('/offtube/')
            # See the output of ffmpeg
        # The POSTed form is invalid
        #j = 5
        #ak = "abc: %s :cba" % type(j)
        #raise Ecxeption
        #return HttpResponse(ak)
    else:
        # First visit - display the form only
        form = PartialVideoForm()
    context = {'video_form': form, 'request': request}
    return render(request, 'offtube/upload.html', context)

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
