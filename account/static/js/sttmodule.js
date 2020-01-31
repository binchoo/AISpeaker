/**
 * 사람의 음성을 Text로 바꾸는 기술은 STT 번들을 사용한다.
 * 현재는 Chrome에서 제공하는 번들을 사용하고 있으나, 이후 추가되는 다른 STT 번들이나 혹은 STT 라이브러리를 추가할 경우
 * 빠른 대응을 위해 Adapter패턴이 적용되어 있다.
 * 음성을 입력받고 그 결과를 Text로 Model에 전달한다.
 * 설계 당시에는 Model로 전달하는 것이 맞다고 생각했으나, 지금은 Controller로 전달하는 것이 적합하다고 생각된다.
 * 이후 수정이 가능하다면 현행 STT->Model에서 STT->Controller->Model로 구조를 바꾸도록 하자.
 */
class STTManger {
  constructor() {
    this.recognitionAdapter = new STTAdapter(this);
  }
  objectLinker(model) {
    this.model = model;

    let rec = this.recognitionAdapter.recognitionOnLoad();
    if (rec === undefined) {
      alert("크롬 브라우저에서만 실행 가능합니다");
    }
  }
  startListen() {
    this.recognitionAdapter.listen();
  }
  stopListen() {
    this.recognitionAdapter.stop();
  }
  getText(result) {
    model.getText(result);
  }
  update() {
    this.model.updateSpeechAnimation();
  }
}

class STTAdapter {
  constructor(manager) {
    this.sttManager = manager;
    if (webkitSpeechRecognition) {
      this.recognition = new ChromeRecognition(this);
      this.browser = "Chrome";
    } else if (SpeechRecognition) {
      this.recognition = new SpeechRecognition(this);
      this.browser = "Other Web Browser";
    } else {
      this.recognition = undefined;
    }
  }
  recognitionOnLoad() {
    if (this.recognition === undefined) {
      return "No Speech Recognition";
    } else {
      return this.browser;
    }
  }
  listen() {
    this.recognition.start();
  }
  stop() {
    this.recognition.stop();
  }
  update() {
    sttManager.update();
  }
  end(result) {
    this.sttManager.getText(result);
  }
}

class ChromeRecognition {
  constructor(adapter) {
    this.adapter = adapter;
    this.recognition = new webkitSpeechRecognition();
    this.recognition.lang = "ko-KR";
    this.recognition.interimResults = false;

    this.isCancel = false;
    this.setEvent();
  }
  setEvent() {
    this.recognition.onresult = event => {
      if (this.isCancel) return;
      let speechResult = event.results[0][0].transcript.toLowerCase();
      this.adapter.end(speechResult);
    };
    this.recognition.onspeechend = () => {
      this.recognition.stop();
    };
    this.recognition.onend = event => {
      console.log(event);
      this.adapter.update();
    };
  }
  start() {
    this.isCancel = false;
    this.recognition.start();
  }
  stop() {
    this.isCancel = true;
    this.recognition.stop();
  }
}

class SpeechRecognition {
  constructor(adapter) {
    this.adapter = adapter;
    this.recognition = new SpeechRecognition();
    this.recognition.lang = "ko-KR";
    this.recognition.interimResults = false;
  }
  setEvent() {
    this.recognition.onresult = event => {
      let speechResult = event.results[0][0].transcript.toLowerCase();
      this.adapter.end(speechResult);
    };
    this.recognition.onspeechend = () => {
      recognition.stop();
    };
    this.recognition.onend = event => {
      this.adapter.update();
    };
  }
  start() {
    this.recognition.start();
  }
  stop() {
    this.recognition.stop();
  }
}
