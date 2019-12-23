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
}
