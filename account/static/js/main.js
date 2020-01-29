var model;
var view;
var controller;
var stanby;
var overlay;
var sttManager;
var ttsManager;
var apiGateway;

/**
 * 설계요소와는 별개로 DOM의 준비와 동시에 JS Class를 로드하는 부분.
 * 실제 스크립트의 엔트리포인트 역할을 한다.
 * objectLinker는 <A>.objectLinker(<B>)형태로 A->B 연결을 의미한다.
 * 생성시에 DOME에 접근하는 클래스나 loading 시간차로 인한 오류를 막기 위해서 별도로 관리한다.
 */

$(document).ready(function() {
  model = new Model();
  view = new View();
  controller = new Controller();
  stanby = new StandbyView();
  overlay = new OverlayView();
  sttManager = new STTManger();
  ttsManager = new TTSModel();
  apiGateway = new APIGateway("localhost");

  model.objectLinker(view, controller);
  controller.objectLinker(model, sttManager, ttsManager, apiGateway);
  view.objectLinker(controller, [stanby, overlay]);
  apiGateway.objectLinker(model);
  sttManager.objectLinker(model);
  ttsManager.objectLinker(controller);

  stanby.objectLinker(view);
  overlay.objectLinker(view);

  controller.ReadFirstTimeOnLoad();
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
