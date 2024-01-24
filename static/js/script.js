// document.addEventListener('DOMContentLoaded', function() {
//     var elems = document.querySelectorAll('.sidenav');
//     var instances = M.Sidenav.init(elems, {edge: "right"});
//     // get the input and textarea elements by their IDs
//     var titleText = document.getElementById('title');
//     var contentText = document.getElementById('content');
//     // Apply character counter functionality
//     addCharacterCounter(titleText);
//     addCharacterCounter(contentText);

//   });



  $(document).ready(function () {
    $(".sidenav").sidenav({edge: "right"});
    $('input#title, textarea#content').characterCounter();
    $('.modal').modal();
  });
    
