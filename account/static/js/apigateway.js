/**
 * 서버와의 통신을 담당하는 부분.
 * 서버에 대한 정의와 서버 API가 정의되어있다.
 */
class APIGateway {
  constructor(serverName) {
    switch (serverName) {
      case "bquad":
        this.serverUrl = "https://bquadai.asdv.cf/";
        break;
      case "localhost":
        this.serverUrl = "127.0.0.1:8000";
        break;
      default:
        this.serverUrl = undefined;
    }
  }
  objectLinker(model) {
    this.model = model;

    let csrftoken = this.getCookie("csrftoken");
    $.ajaxSetup({
      beforeSend: (xhr, settings) => {
        if (!this.csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    });
  }

  sendQuestion(question) {
    if (this.serverUrl === undefined) {
      this.model.getServerError(500);
    } else {
      $.ajax({
        type: "POST",
        url: "speaker/result",
        dataType: "json",
        data: {
          question: question
        },
        success: res => {
          this.receive(res);
        },
        error: res => {
          if (res.status === 200) this.receive(res);
        }
      });
    }
  }

  sendIteratorRequest() {
    if (this.serverUrl === undefined) {
      this.model.getServerError(500);
    } else {
      $.ajax({
        type: "POST",
        url: "bible/more",
        dataType: "json",
        data: {
          data: 3
        },
        success: res => {
          this.model.appandModelData(res.contents);
        },
        error: res => {
          console.log(res);
        }
      });
    }
  }

  sendInvertQC() {
    if (this.serverUrl === undefined) {
      this.model.getServerError(500);
    } else {
      $.ajax({
        type: "POST",
        url: "speaker/qc_inverter",
        dataType: "json",
        data: {},
        success: res => {
          console.log(res.responseText);
        },
        error: res => {
          console.log(res.responseText);
        }
      });
    }
  }

  sendAdditionalQuestion(question, contents) {
    if (this.serverUrl === undefined) {
      this.model.getServerError(500);
    } else {
      $.ajax({
        type: "POST",
        url: "bible/qa",
        dataType: "json",
        data: {
          question: question,
          contents: contents
        },
        success: res => {
          this.receive(res);
        },
        error: res => {
          if (res.status === 200) this.receive(res);
        }
      });
    }
  }

  receive(res) {
    this.model.receiveResult(res.responseText);
  }

  getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie != "") {
      let cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        let cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  }
}
