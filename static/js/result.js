var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition
//var SpeechGrammarList = SpeechGrammarList || webkitSpeechGrammarList
//var SpeechRecognitionEvent = SpeechRecognitionEvent || webkitSpeechRecognitionEvent

var diagnosticPara = document.querySelector('.output'); //결과물html로
diagnosticPara.textContent = '다시 질문하려면 아이콘을 클릭하세요';


recognition = new SpeechRecognition();
recognition.lang = 'ko-KR';
recognition.interimResults = false;
//recognition.continuous = false;
recognition.maxAlternatives = 1;

document.getElementsByClassName("speak-icon")[0].onclick = function() {
recognition.start();
$(".speak-icon").attr("src", "/static/img/audio_color.png");
console.log('Ready to receive a question.');
}

recognition.onresult = function(event) {
var speechResult = event.results[0][0].transcript.toLowerCase();
console.log('transcript', speechResult);
diagnosticPara.textContent = 'Speech received: ' + speechResult + '.';
console.log('end');
$(".speak-icon").attr("src", "/static/img/audio_black.png");
input_Text(speechResult)
document.getElementById('frm').submit()
}

recognition.onspeechend = function() {
recognition.stop();
console.log('rec stop');
}

function input_Text(t){
document.getElementById("q").value = t;
}

var qtype = $(".qtype").text();
$(".response").css({
  "background-image": `url(/static/img/${qtype}.jpg)`,
  "background-size": "cover",
  "background-repeat": "no-repeat",
  "background-position": "center"
})

function send_qa_to_controller(action,question, question_type){
//form 에 q와 a를 담아 controller에 전송

var form = document.createElement("form");
form.setAttribute("charset", "UTF-8");
form.setAttribute("method", "Post"); // Get 또는 Post 입력
form.setAttribute('action', action);

var hiddenField = document.createElement("input");
hiddenField.setAttribute("type", "text");
hiddenField.setAttribute("name", "question");
hiddenField.setAttribute("value", question);
form.appendChild(hiddenField);

hiddenField = document.createElement("input");
hiddenField.setAttribute("type", "text");
hiddenField.setAttribute("name", "question_type");
hiddenField.setAttribute("value", question_type);
form.appendChild(hiddenField);

document.body.appendChild(form);
form.submit();

}