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
