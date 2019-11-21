from django.shortcuts import render
from . import question_classifier
from Controller.Controller import Controller
from django.http import HttpResponse
# Create your views here.


#홈화면
def home(request):
    user = request.user
    return render(request, 'home.html',{'user' : user})

#스피커초기 화면
def speaker(request):
    user = request.user
    return render(request, 'speakerInit.html', {'loginUser' : user})

#리시버
def wait(request):
    return render(request, 'wait_or_error.html')

#iframe 컨트롤러 - 리시버url
def controller(request):
    question = request.POST["question"]
    c = Controller()
    response = c.propagete(question)
    return HttpResponse(response)
    # try :
    #     question_type = request.POST["question_type"]
    #     question = request.POST["question"]
    #     print("result->컨트롤러")
    #     return render(request, 'controller.html',{'question': question, 'question_type' : question_type})
    # except KeyError:
    #     question_type = "wait"
    #     question = "wait"
    #     print("result->컨트롤러 예외발생")
    #     return render(request, 'controller.html',{'question': question, 'question_type' : question_type})

##    if (question_type=="weather"):
##        return render(request, 'weather.html')
##    elif (question_type=="news"):
##        return render(request, 'news.html')
##   elif (question_type=="stockinfo") or (question_type=="stocktrade"):
##        return render(request, 'stock.html',{'question': question, 'question_type' : question_type})
##    elif (question_type=="bible"):
##        return render(request, 'bible.html')
##   else:
##       return render(request,'wait_or_error.html')

def result(request):
    question = request.POST["question"]
    print(question)
    question_type = question_classifier.getFinalResult(question)
    print(question_type)
    return render(request, 'result.html', {'question': question , 'question_type' : question_type})