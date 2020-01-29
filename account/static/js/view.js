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
