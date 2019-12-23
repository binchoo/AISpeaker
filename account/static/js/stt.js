var SpeechRecognition = SpeechRecognition || webkitSpeechRecognition
    //var SpeechGrammarList = SpeechGrammarList || webkitSpeechGrammarList
    //var SpeechRecognitionEvent = SpeechRecognitionEvent || webkitSpeechRecognitionEvent

    var diagnosticPara = document.querySelector('.output'); //결과물html로
    

    recognition = new SpeechRecognition();
    recognition.lang = 'ko-KR';
    recognition.interimResults = false;
    //recognition.continuous = false;
    recognition.maxAlternatives = 1;

    diagnosticPara.textContent = '...음성입력전';

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