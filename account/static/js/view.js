/**
 * View는 하위에 다수의 view를 다시 가지는 일종의 root view이다.
 * Model이 View로 update를 요청하면 View는 ViewModel을 받아서 자신의 자식 view중 변경이 발생한 view로 데이터를 전달한다.
 * 변경사항이 없은 자식 view는 이때 무시한다.
 * View의 역할은 다수의 자식 view들을 통합하여 관리하는 것이다.
 * 현재는 stanby-view와 overlay-view라는 2개의 view를 가지고 있다.
 */
class View {
  constructor() {
    this.view = {};
  }

  objectLinker(controller, views) {
    this.controller = controller;
    this.view["standby-view"] = views[0];
    this.view["overlay-view"] = views[1];
  }

  update(viewModel) {
    if (viewModel === undefined) return;

    if (viewModel["standby-view"].modified) {
      this.view["standby-view"].update(viewModel["standby-view"].data);
    }
    if (viewModel["overlay-view"].modified) {
      this.view["overlay-view"].update(viewModel["overlay-view"].data);
    }
  }
}
