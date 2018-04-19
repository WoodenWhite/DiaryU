from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    return render(request, 'matching/index.html')
    # return HttpResponse("Test")


def emotion(request):
    userid = request.POST['userid']
    content = request.POST['diary']
    return HttpResponse(userid + ":" + content)
