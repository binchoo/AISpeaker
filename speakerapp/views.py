from django.shortcuts import render
from . import question_classifier
from Forwarder.Forwarder import Forwarder
from django.http import HttpResponse, JsonResponse

# Create your views here.

qc_type = 'rnn'

#홈화면
def home(request):
    user = request.user
    return render(request, 'index.html',{'user' : user})

# #스피커초기 화면
# def speaker(request):
#     user = request.user
#     return render(request, 'speakerInit.html', {'loginUser' : user})

#리시버
def wait(request):
    return render(request, 'wait_or_error.html')

def qc_invert(request) :
    global qc_type
    if qc_type == 'rnn' :
        qc_type = 'regex'
    else :
        qc_type = 'rnn'
    return HttpResponse("Changed To {} Classifier.\n".format(qc_type))

def result(request):
    try :
        question = request.POST["question"]
    except :
        question = request.GET["question"]
    response = Forwarder(type=qc_type, upgrade=True).forward(question)
    return HttpResponse(response)