# Create your views here.
from django.http import HttpResponse
from django.template import Context, loader

def index(request):
    #latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    #context = {'latest_poll_list': latest_poll_list}
    #return render(request, 'polls/index.html', context)
    recent_uploads = {'abc': 'a', 'def': 'b'}
    context = {'recent_uploads', recent_uploads}
    #template = loader.get_template('offtube/index.html')
    return render(request, 'offtube/index.html', context)
    #return HttpResponse(template.render(recent_uploads))
    #return HttpResponse("Hello World - I'm watching you.")

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
