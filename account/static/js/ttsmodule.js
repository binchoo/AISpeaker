/**
 * TTS는 단순하게 텍스트를 입력받으면 음성으로 읽어준다.
 * 해당 모듈은 음성읽기, 읽기정지 등 TTS의 기능을 한 곳으로 모으기 위해 존재한다.
 */
class TTSModel {
  constructor() {}
  objectLinker(controller) {
    this.controller = controller;
    this.synth = window.speechSynthesis;
    this.isCanceled = false;
  }

  startTTS(text) {
    let voices = this.synth.getVoices()[0];
    let utter = new SpeechSynthesisUtterance();
    utter.voice = voices;
    utter.pitch = 0.8;
    utter.rate = 0.8;

    utter.onend = () => {
      if (!this.isCanceled) {
        this.controller.JustTogglePlayAndPhuse();
      }
    };
    this.isCanceled = false;
    utter.text = text;
    this.synth.speak(utter);
  }
  pauseTTS() {
    this.isCanceled = true;
    this.synth.cancel();
  }

  startReading() {
    $("#msgbox")[0].contentWindow.speak();
  }

  pauseReading() {
    $("#msgbox")[0].contentWindow.pause();
  }
}
