# Create your views here.

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
