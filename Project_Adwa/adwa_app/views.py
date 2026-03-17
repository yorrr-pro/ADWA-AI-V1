from django.shortcuts import render
from django.http import JsonResponse
from .logic import My_AI
from .feedback import EmailHandler

def answer(request):
    question = request.GET.get('question')
    if not question:
        return JsonResponse({"error": "No question provided"}, status=400)

    try:
        ai = My_AI(question)
        response, source = ai.answer()
        return JsonResponse(
            {"answer": response, "source": source},
            json_dumps_params={"ensure_ascii": False},
            safe=False
        )
    except Exception as e:
        print(f"AI response error: {e}")  # This will show in Render logs
        return JsonResponse(
            {"error": "Server error while generating AI response. Check logs."},
            status=500
        )

def feedback(request):
    feed = request.GET.get('feed')
    name = request.GET.get('name')
    email = request.GET.get('email', "No Email")
    try:
        user_feed = EmailHandler(feed=feed, name=name, email=email)
        return JsonResponse(user_feed.status_email(), safe=False)
    except Exception as e:
        print(f"Feedback error: {e}")
        return JsonResponse(
            {"error": "Server error while sending feedback. Check logs."},
            status=500
        )