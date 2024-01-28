/* jshint esversion: 8, jquery: true, scripturl: true */

  // jQuery for MaterializeCSS initialization
  $(document).ready(function () {
    $(".sidenav").sidenav({edge: "right"});
    $('input#title, textarea#content').characterCounter();
    $('.modal').modal();
  });
    

