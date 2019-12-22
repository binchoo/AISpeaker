var model;
var view;
var controller;
var stanby;
var overlay;
var sttManager;
var ttsManager;
var apiGateway;

$(document).ready(function() {
  model = new Model();
  view = new View();
  controller = new Controller();
  stanby = new StandbyView();
  overlay = new OverlayView();
  sttManager = new STTManger();
  ttsManager = new TTSModel();
  apiGateway = new APIGateway("bquad");

  model.objectLinker(view, controller);
  controller.objectLinker(model, sttManager, ttsManager, apiGateway);
  view.objectLinker(controller, [stanby, overlay]);
  apiGateway.objectLinker(model);
  sttManager.objectLinker(model);
  ttsManager.objectLinker(controller);

  stanby.objectLinker(view);
  overlay.objectLinker(view);

  //controller.ReadFirstTimeOnLoad();
});

const siriWave = new SiriWave({
  container: document.getElementById("siri-wave"),
  width: 800,
  height: 120,
  style: "ios9",
  autostart: true,
  amplitude: 0
});
function randomAmplitude() {
  const value = 2;
  siriWave.setAmplitude(value);
  requestAnimationFrame(randomAmplitude);
}
randomAmplitude();
