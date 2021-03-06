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
            arg: {
              show: true,
              update: false,
              data: "주식, 날씨, 뉴스, 성경에 대해 물어보세요!"
            }
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
            arg: { show: false }
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
              data: ""
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

  changeViewModel(changes) {
    for (const key in changes) {
      if (changes.hasOwnProperty(key)) {
        const element = changes[key];
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
    this.modifiedBubbling();
    this.view.update(this.viewModel);
  }

  modifiedBubbling() {
    for (const target in this.viewModel) {
      if (this.viewModel.hasOwnProperty(target)) {
        const view = this.viewModel[target];
        for (const key in view.data) {
          if (view.hasOwnProperty(key)) {
            const element = view[key];
            view.modified = view.modified || element.modified;
          }
        }
      }
    }
  }

  changeThisView(view) {
    this.thisView = view;
  }

  appandModelData(text) {
    let data = this.viewModel["overlay-view"].data[3].arg.data;
    let index = data.indexOf('</p><div onclick="next()" />') - 1;
    data = data.substring(0, index) + " " + text + data.substring(index);
    this.viewModel["overlay-view"].data[3].arg.data = data;
    this.answer = data;
    this.appendData(text);
    // this.viewModel["overlay-view"].data[3].modified = true;
    // this.viewModel["overlay-view"].data[3].arg.update = true;
    // this.updateView();
  }
  appendData(text) {
    this.controller.appendIFrame(text);
  }

  getServerError() {}

  getText(text) {
    if (this.thisView == "standby-view") {
      this.question = text;
      this.controller.sendQuestion(text);
    } else {
      this.question = text; //질문
      let contesnts = this.dataCleansing(
        this.answer,
        '<div id="dic_area">',
        "</div>"
      );
      this.controller.sendAdditionalQuestion(text, contesnts);
    }
  }

  dataCleansing(htmlText, openTag, closeTag) {
    let start = htmlText.indexOf(openTag, 0) + openTag.length;
    let end = htmlText.indexOf(closeTag, start);
    return htmlText.substring(start, end);
  }

  updateSpeechAnimation() {
    if (this.getModelData("standby-view", 0).show) {
      let temp = this.viewModel["standby-view"].data[0];
      temp.modified = true;
      temp.data[0].arg.show = false;
    }
    if (this.getModelData("overlay-view", 0).show) {
      let temp = this.viewModel["overlay-view"].data[0];
      temp.modified = true;
      temp.arg.show = false;
    }
    this.updateView();
  }
  receiveResult(result) {
    this.answer = result;
    let overlay = this.viewModel["overlay-view"].data[3];
    overlay.modified = true;
    overlay.arg = { show: true, update: true, data: result };

    let mailbox = this.viewModel["standby-view"].data[3];
    mailbox.modified = true;
    mailbox.arg = { show: true, update: true, data: this.question };

    this.thisView = "overlay-view";
    this.updateView();
  }
}
