class Model {
  constructor() {
    this.viewModel = {
      "standby-view": {
        modified: false,
        data: [
          {
            name: "voice-core",
            modified: false,
            arg: { show: false }
          },
          {
            name: "play-and-pause",
            modified: false,
            arg: { show: true }
          },
          {
            name: "reset",
            modified: false,
            arg: { show: false }
          },
          {
            name: "open-mailbox",
            modified: false,
            arg: { show: true, update: false, data: "질문을 말씀해주세요" }
          }
        ]
      },
      "overlay-view": {
        modified: false,
        data: [
          {
            name: "voice-core",
            modified: false,
            arg: { show: false }
          },
          {
            name: "play-and-pause",
            modified: false,
            arg: { show: true }
          },
          {
            name: "reset",
            modified: false,
            arg: { show: false }
          },
          {
            name: "overlay",
            modified: false,
            arg: {
              show: false,
              update: false,
              data: "질문을 말씀해주세요"
            }
          }
        ]
      }
    };

    this.thisView = "standby-view";
    this.question = "";
    this.answer = "";
    this.message =
      "AI 스피커 아이쿠 입니다!\n머핀을 누르고 말씀해주세요\n주식, 날씨, 뉴스, 성경에 대해 질문하시면 됩니다!";
  }

  objectLinker(view, controller) {
    this.view = view;
    this.controller = controller;
  }

  changeViewModel(chages) {
    for (const key in chages) {
      if (chages.hasOwnProperty(key)) {
        const element = chages[key];
        this.viewModel[element.view].modified = true;
        this.viewModel[element.view].data[element.argc].modified = true;
        if (element.argv !== undefined) {
          this.viewModel[element.view].data[element.argc].arg = {
            show: element.argv
          };
        }
      }
    }
    this.updateView();
  }

  getModelData(view, argc) {
    return this.viewModel[view].data[argc].arg;
  }

  getPreviousMessage() {
    return this.message;
  }

  updateView() {
    this.view.update(this.viewModel);
  }

  changeThisView(view) {
    this.thisView = view;
  }

  getServerError() {}

  getText(text) {
    if (this.thisView == "standby-view") {
      this.question = text;
      this.controller.sendQuestion(text);
      console.log("get text from stt : " + text);
    } else {
      this.question = text;
      this.controller.sendAdditionalQuestion(this.answer, text);
      console.log("get text from stt + Q : " + text);
    }
  }

  updateSpeechAnimation() {
    let temp = this.viewModel[this.thisView];
    temp.modified = true;
    temp = temp.data[0];
    temp.modified = true;
    temp.arg.show = false;
    this.updateView();
  }
  receiveResult(result) {
    this.answer = result;
    let overlay = this.viewModel["overlay-view"];
    overlay.modified = true;
    overlay = overlay.data[3];
    overlay.modified = true;
    overlay.arg = { show: true, update: true, data: result };

    let mailbox = this.viewModel["standby-view"];
    mailbox.modified = true;
    mailbox = mailbox.data[3];
    mailbox.modified = true;
    mailbox.arg = { show: true, update: true, data: this.question };

    console.log("receive data form server : " + result);

    this.thisView = "overlay-view";
    this.updateView();
  }
}
