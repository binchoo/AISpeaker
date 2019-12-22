class OverlayView {
  constructor() {
    this.overlayView = $("#overlay-view");
    this.speakerCircle = $("#overlay-modal > .speaker-circle");
    this.coreVoice = $(
      "#overlay-modal > .speaker-circle > #overlay-core-voice"
    );
    this.haloEffect = $("#overlay-modal > .speaker-circle > .effect-halo");

    this.playAndPause = $(
      "#overlay-modal > .speaker-circle > .icon-section > .control-icon"
    ).first();
    this.reset = $(
      "#overlay-modal > .speaker-circle > .icon-section > .control-icon"
    ).next();

    this.showOverlayView = false;
  }

  objectLinker(view) {
    this.view = view;
    this.controller = view.controller;
    this.addEventHandler();
  }
  addEventHandler() {
    this.coreVoice.click(this.controller.OverlayView_StartRecognition);
    this.reset.click(this.controller.OverlayView_ResetSpeach);
    this.playAndPause.click(this.controller.OverlayView_PlayAndPhuse);
    this.overlayView.click(this.controller.OverlayView_CloseOverlay);
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
      case "overlay":
        this.toggleOverlay(arg);
        break;
      default:
    }
  }

  startRecognition(arg) {
    if (arg.show) {
      console.log("Speaker On");
      this.haloEffect
        .addClass("effect-halo-runnig")
        .removeClass("effect-halo-blink");
      this.speakerCircle.addClass("on");
    } else {
      console.log("Speaker Off");
      this.haloEffect
        .addClass("effect-halo-blink")
        .removeClass("effect-halo-runnig");
      this.speakerCircle.removeClass("on");
    }
  }
  switchPlayAndPause(arg) {
    if (arg.show) {
      this.playAndPause
        .attr("src", "../img/round_play_circle_outline_white_48dp.png")
        .addClass("press-button");
      setTimeout(() => {
        this.playAndPause.removeClass("press-button");
      }, 210);
    } else {
      this.playAndPause
        .attr("src", "../img/round_pause_circle_outline_white_48dp.png")
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

  toggleOverlay(arg) {
    if (arg.show) {
      console.log("show overlay");
      this.showOverlayView = true;
      this.overlayView.addClass("slide-up").removeClass("slide-down");
      this.overlayView.css({ opacity: "1", "pointer-events": "auto" });
    } else {
      console.log("hide overlay");
      this.showOverlayView = false;
      this.overlayView.addClass("slide-down").removeClass("slide-up");
      this.overlayView.css({ opacity: "0", "pointer-events": "none" });
    }

    if (arg.update) {
      console.log("update");
      console.log(arg.data);
      arg.update = false;
    } else {
      console.log("no updaye");
    }
  }
}
