$("input[name='username'], input[name='password'], input[name='password2']").focus(function() {
  $(this).prevAll("label").eq(0).animate({
    top: "8px"
  }, 500);
})
$("input[name='username'], input[name='password'], input[name='password2']").focusout(function() {
  if($(this).val() === '') {
    $(this).prevAll("label").eq(0).animate({
      top: "40px"
    }, 500);
  }
})