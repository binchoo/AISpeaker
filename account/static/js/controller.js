<<<<<<< HEAD
/**
 * Model과 다른 기능요소를 연결하는 부분.
 * 가장 많은 모듈과 연결되어 있다.
 * DOM이벤트가 정의되어 있는 클래스로 실제로 이벤트의 시작지점이 된다.
 * 내부에 상태를 가지고 있지 않아서 순수함수의 특성을 가진다.
 */
class Controller {
  constructor() {}
  objectLinker(model, stt, tts, gateway) {
    this.model = model;
    this.sttManager = stt;
    this.ttsManager = tts;
    this.apiGateway = gateway;
  }

  StandbyView_StartRecognition() {
    let isPressed = model.getModelData("standby-view", 0).show;
    model.changeViewModel([
      { view: "standby-view", argc: 0, argv: !isPressed }
    ]);
    if (!isPressed) sttManager.startListen();
    else sttManager.stopListen();
  }
  StandbyView_PlayAndPhuse() {
    let isPause = model.getModelData("standby-view", 1).show;
    model.changeViewModel([{ view: "standby-view", argc: 1, argv: !isPause }]);
    if (!isPause) ttsManager.pauseTTS();
    else ttsManager.startTTS(model.getPreviousMessage());
  }

  StandbyView_ResetSpeach() {
    model.changeViewModel([
      { view: "standby-view", argc: 0, argv: false },
      { view: "standby-view", argc: 2, argv: true }
    ]);
    sttManager.stopListen();
    setTimeout(() => {
      model.changeViewModel([{ view: "standby-view", argc: 0, argv: true }]);
      sttManager.startListen();
    }, 500);
  }
  StandbyView_ShowOverlay() {
    model.changeViewModel([
      { view: "standby-view", argc: 3 },
      { view: "overlay-view", argc: 3, argv: true }
    ]);
    model.changeThisView("overlay-view");
  }

  OverlayView_StartRecognition() {
    let isPressed = model.getModelData("overlay-view", 0).show;
    model.changeViewModel([
      { view: "overlay-view", argc: 0, argv: !isPressed }
    ]);
    if (!isPressed) sttManager.startListen();
    else sttManager.stopListen();
  }
  OverlayView_PlayAndPhuse() {
    let isPause = model.getModelData("overlay-view", 1).show;
    model.changeViewModel([{ view: "overlay-view", argc: 1, argv: !isPause }]);
    if (!isPause) ttsManager.pauseReading();
    else ttsManager.startReading();
  }
  OverlayView_ResetSpeach() {
    model.changeViewModel([
      { view: "overlay-view", argc: 0, argv: false },
      { view: "overlay-view", argc: 2, argv: true }
    ]);
    sttManager.stopListen();
    setTimeout(() => {
      model.changeViewModel([{ view: "overlay-view", argc: 0, argv: true }]);
      sttManager.startListen();
    }, 500);
  }
  OverlayView_CloseOverlay(event) {
    if (event.target.id === "overlay-view") {
      model.changeViewModel([{ view: "overlay-view", argc: 3, argv: false }]);
      model.changeThisView("standby-view");
    }
  }

  sendQuestion(question) {
    this.apiGateway.sendQuestion(question);
  }

  sendAdditionalQuestion(question, contents) {
    this.apiGateway.sendAdditionalQuestion(question, contents);
  }
  getMoreData() {
    this.apiGateway.sendIteratorRequest();
  }

  startRecognition() {
    this.sttManager.startListen();
  }

  speachEnd() {
    this.StandbyView_PlayAndPhuse();
  }

  JustTogglePlayAndPhuse() {
    let isPause = model.getModelData("standby-view", 1);
    model.changeViewModel([{ view: "standby-view", argc: 1, argv: !isPause }]);
  }

  ReadFirstTimeOnLoad() {
    this.ttsManager.pauseTTS();
    this.StandbyView_PlayAndPhuse();
  }
  appendIFrame(text) {
    $("#msgbox")[0].contentWindow.appendBibleText(text);
  }
}
=======
class Controller {
  constructor() {}
  objectLinker(model, stt, tts, gateway) {
    this.model = model;
    this.sttManager = stt;
    this.ttsManager = tts;
    this.apiGateway = gateway;
  }

  StandbyView_StartRecognition() {
    let isPressed = model.getModelData("standby-view", 0).show;
    model.changeViewModel([
      { view: "standby-view", argc: 0, argv: !isPressed }
    ]);
    if (!isPressed) sttManager.startListen();
    else sttManager.stopListen();
  }
  StandbyView_PlayAndPhuse() {
    let isPause = model.getModelData("standby-view", 1).show;
    model.changeViewModel([{ view: "standby-view", argc: 1, argv: !isPause }]);
    if (!isPause) ttsManager.pauseTTS();
    else ttsManager.startTTS(model.getPreviousMessage());
  }

  StandbyView_ResetSpeach() {
    model.changeViewModel([
      { view: "standby-view", argc: 0, argv: false },
      { view: "standby-view", argc: 2, argv: true }
    ]);
    sttManager.stopListen();
    setTimeout(() => {
      model.changeViewModel([{ view: "standby-view", argc: 0, argv: true }]);
      sttManager.startListen();
    }, 500);
  }
  StandbyView_ShowOverlay() {
    model.changeViewModel([
      { view: "standby-view", argc: 3 },
      { view: "overlay-view", argc: 3, argv: true }
    ]);
    model.changeThisView("overlay-view");
  }

  OverlayView_StartRecognition() {
    let isPressed = model.getModelData("overlay-view", 0).show;
    model.changeViewModel([
      { view: "overlay-view", argc: 0, argv: !isPressed }
    ]);
    if (!isPressed) sttManager.startListen();
    else sttManager.stopListen();
  }
  OverlayView_PlayAndPhuse() {
    let isPause = model.getModelData("overlay-view", 1).show;
    model.changeViewModel([{ view: "overlay-view", argc: 1, argv: !isPause }]);
    if (!isPause) ttsManager.pauseReading();
    else ttsManager.startReading();
  }
  OverlayView_ResetSpeach() {
    model.changeViewModel([
      { view: "overlay-view", argc: 0, argv: false },
      { view: "overlay-view", argc: 2, argv: true }
    ]);
    sttManager.stopListen();
    setTimeout(() => {
      model.changeViewModel([{ view: "overlay-view", argc: 0, argv: true }]);
      sttManager.startListen();
    }, 500);
  }
  OverlayView_CloseOverlay(event) {
    if (event.target.id === "overlay-view") {
      model.changeViewModel([{ view: "overlay-view", argc: 3, argv: false }]);
      model.changeThisView("standby-view");
    }
  }

  sendQuestion(question) {
    this.apiGateway.sendQuestion(question);
  }

  sendAdditionalQuestion(question, contents) {
    this.apiGateway.sendAdditionalQuestion(question, contents);
  }
  getMoreData() {
    this.apiGateway.sendIteratorRequest();
  }

  startRecognition() {
    this.sttManager.startListen();
  }

  speachEnd() {
    this.StandbyView_PlayAndPhuse();
  }

  JustTogglePlayAndPhuse() {
    let isPause = model.getModelData("standby-view", 1);
    model.changeViewModel([{ view: "standby-view", argc: 1, argv: !isPause }]);
  }

  ReadFirstTimeOnLoad() {
    this.ttsManager.pauseTTS();
    this.StandbyView_PlayAndPhuse();
  }
  appendIFrame(text) {
    $("#msgbox")[0].contentWindow.appendBibleText(text);
  }
}
>>>>>>> a89ae6cc4c453ec866e4c9b426dd967826cce4cc
