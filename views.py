""" This is the views.py file for the OffTube project. """

# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
#from django.template import Context, loader
from django.shortcuts import render
from offtube.models import Video, PartialVideoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as djlogout

def logout(request):
    """ Very simple view to logout of the site. """
    djlogout(request)
    return HttpResponseRedirect('/offtube/')

def index(request):
    """ This is the view for the main OffTube homepage. It simply finds
    a list of all uploaded Videos and puts the latest first. """
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
    # FIXME: Limit required here.
    recent_uploads = Video.objects.order_by('-upload_date').exclude(
        status='pending')
    total_vids = Video.objects.count()
    context = {'recent_uploads': recent_uploads,
        'total_vids': total_vids,
        'request': request}
    return render(request, 'offtube/index.html', context)

def play(request, **kwargs):
    """ This view grabs everything necessary for the main Video view page. """
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
    form = PartialVideoForm(instance=video)

    total_vids = Video.objects.count()

    from django.contrib.sites.models import Site

    current_site = Site.objects.get_current()

    context = {'video': video,
        'video_form': form,
        'referer': referer,
        'total_vids': total_vids,
        'domain': current_site.domain,
        'request': request}
    if request.path.split('/')[-2] == 'play':
        return render(request, 'offtube/play.html', context)
    if request.path.split('/')[-2] == 'embed':
        return render(request, 'offtube/embed.html', context)

def search(request):
    """ This view searches for any Videos with the query in their title. """
    if not request.GET.has_key('q'):
        return HttpResponseRedirect('/offtube/')
    vids = Video.objects.filter(title__icontains=request.GET['q'].lower())
    total_vids = Video.objects.count()
    context = {'results': vids,
        'total_vids': total_vids,
        'request': request}
    return render(request, 'offtube/list.html', context)

def popular(request, **kwargs):
    """ This view obtains the most popular videos of all time, or in the past
    X number of days (provided by the period kwarg. """
    if kwargs['period']:
        from datetime import datetime, timedelta

        cutoff = datetime.now() - timedelta(days=int(kwargs['period']))
        vids = Video.objects.filter(upload_date__gte=cutoff).order_by('-hits')
    else:
        vids = Video.objects.order_by('-hits')

    total_vids = Video.objects.count()
    context = {'results': vids,
        'total_vids': total_vids,
        'request': request}
    return render(request, 'offtube/list.html', context)

def videos(request, **kwargs):
    """ This view lists all Videos uploaded by a certain user. """
    if not kwargs['username']:
        return HttpResponse('Error: You need to specify a username.')

    username = kwargs['username']
    vids = Video.objects.filter(
        upload_user__username=username).order_by('upload_date')

    total_vids = Video.objects.count()
    context = {'results': vids,
        'total_vids': total_vids,
        'request': request}
    return render(request, 'offtube/list.html', context)

def delete(request, video_id=None):
    """ This view deleted the video and associated files when called. """
    original_video = Video.objects.get(id=video_id)
    if request.user != original_video.upload_user:
        return HttpResponse('Error: You do not have permission to edit '
            'this video')

    original_video.delete()
    return HttpResponseRedirect('/offtube/')

def edit(request, video_id=None):
    """ This view modifies the metadata of a video some time after it has been
        uploaded. """
    if request.method != 'POST':
        return HttpResponse('Error: You must select a video and then edit it.')

    # The form has been submitted...
    original_video = Video.objects.get(id=video_id)
    form = PartialVideoForm(request.POST, request.FILES,
        instance=original_video)

    if not form.is_valid():
        return HttpResponse('Error: The data you submitted is not valid.')

    if request.user != original_video.upload_user:
        return HttpResponse('Error: You do not have permission to edit '
            'this video')

    video = form.save()
    return HttpResponseRedirect('/offtube/play/' + str(video_id))

# FIXME: Looks ugly - is there a better way to do this?
@login_required(login_url='../login/')
def upload(request):
    """ This is the view that handles the upload stages of a Video, both
    before and after the POST has occurred. """
    if request.method != 'POST':
        # First visit - display the form only
        form = PartialVideoForm()
        total_vids = Video.objects.count()
        context = {'video_form': form,
            'total_vids': total_vids,
            'request': request}
        return render(request, 'offtube/upload.html', context)

    # The form has been submitted...
    form = PartialVideoForm(request.POST, request.FILES)
    if not form.is_valid():
        # The POSTed form is invalid
        return HttpResponse('Error: You need to specify a username. %s' % form.errors)

    # The form is valid
    video = form.save(commit=False)
    video.upload_user = request.user
    video.status = 'pending'
    video.save()
    form.save_m2m()
    return HttpResponseRedirect('/offtube/')
    # Would be nice to see the output of ffmpeg after upload...
