from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from .logic import My_AI


from .feedback import EmailHandler

def answer(request):
    question = request.GET.get('question')
    ai = My_AI(question)
    response, source = ai.answer()
    return JsonResponse({"answer":response,"source":source},json_dumps_params={"ensure_ascii":False}, safe=False)

def feedback(request):
    feed = request.GET.get('feed')
    name = request.GET.get('name')
    email = request.GET.get('email',"No Email")
    user_feed = EmailHandler(feed=feed,name=name,email=email)
    return JsonResponse(user_feed.status_email(), safe=False)
# Create your views here.
