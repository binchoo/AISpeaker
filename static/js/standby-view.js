class StandbyView {
  constructor() {
    this.speakerCircle = $(
      "#standby-view > #speaker-section > .speaker-circle"
    );
    this.coreVoice = $("#standby-core-voice");
    this.voiceImage = $("#standby-core-img");
    this.mailbox = $("#result-mailbox");
    this.haloEffect = $(
      "#standby-view > #speaker-section > .speaker-circle > .effect-halo"
    );
    this.playAndPause = $(
      "#standby-view > #speaker-section > .speaker-circle >  .icon-section > .control-icon"
    ).first();
    this.reset = $(
      "#standby-view > #speaker-section > .speaker-circle > .icon-section > .control-icon"
    ).next();

    this.siri = $("#siri-wave");
    $("#siri-wave > canvas").css({ width: "100%" });
  }
  objectLinker(view) {
    this.view = view;
    this.controller = view.controller;
    this.addEventHandler();
  }
  addEventHandler() {
    this.coreVoice.click(this.controller.StandbyView_StartRecognition);
    this.mailbox.click(this.controller.StandbyView_ShowOverlay);
    this.playAndPause.click(this.controller.StandbyView_PlayAndPhuse);
    this.reset.click(this.controller.StandbyView_ResetSpeach);
  }
  update(data) {
    for (const key in data) {
      if (data.hasOwnProperty(key)) {
        const element = data[key];
        if (element.modified) {
          this.domUpdater(element.name, element.arg);
          element.modified = false;
        }
      }
    }
  }

  domUpdater(name, arg) {
    switch (name) {
      case "voice-core":
        this.startRecognition(arg);
        break;
      case "play-and-pause":
        this.switchPlayAndPause(arg);
        break;
      case "reset":
        this.pressResetButton();
        break;
      case "open-mailbox":
        this.pressMailbox(arg);
        break;
      default:
    }
  }

  startRecognition(arg) {
    if (arg.show) {
      this.haloEffect
        .addClass("effect-halo-runnig")
        .removeClass("effect-halo-blink");
      this.voiceImage.addClass("fade-out").removeClass("fade-in");
      this.speakerCircle.addClass("on");
      this.siri.css({ display: "block" });
      siriWave.start();
      siriWave.setSpeed(0.1);
    } else {
      this.haloEffect
        .addClass("effect-halo-blink")
        .removeClass("effect-halo-runnig");
      this.voiceImage.addClass("fade-in").removeClass("fade-out");
      this.speakerCircle.removeClass("on");
      this.siri.css({ display: "none" });
      siriWave.stop();
    }
  }

  switchPlayAndPause(arg) {
    if (arg.show) {
      this.playAndPause
        .removeClass("pause")
        .addClass("play")
        .addClass("press-button");
      setTimeout(() => {
        this.playAndPause.removeClass("press-button");
      }, 210);
    } else {
      this.playAndPause
        .removeClass("play")
        .addClass("pause")
        .addClass("press-button");
      setTimeout(() => {
        this.playAndPause.removeClass("press-button");
      }, 210);
    }
  }

  pressResetButton() {
    this.reset.addClass("press-button rotate-button");
    setTimeout(() => {
      this.reset.removeClass("press-button rotate-button");
    }, 210);
  }

  pressMailbox(arg) {
    this.mailbox.addClass("press-button");
    this.mailbox.children("p").text(arg.data);
    setTimeout(() => {
      this.mailbox.removeClass("press-button");
    }, 210);
  }
}
