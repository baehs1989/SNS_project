$(function() {
  $('button.navbar-toggle').click(function() {
    var value = $('body').css('padding-top');
    if (value === '45px') {
      $('body').css('padding-top', '+=185');
    } else {
      $('body').css('padding-top', '45px');
    }
  });
});
