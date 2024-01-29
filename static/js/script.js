/* jshint esversion: 8, jquery: true, scripturl: true */

  // jQuery for MaterializeCSS initialization
  $(document).ready(function () {
    $(".sidenav").sidenav({edge: "right"});
    $('input#title, textarea#content').characterCounter();
    $('.modal').modal();
  });

  // delete post functionality
    document.addEventListener('DOMContentLoaded', function() {
      var myButton = document.getElementById('modal-delete');
      
      if (myButton) {
          myButton.addEventListener('click', function() {
              // get post object id assigned to the variable
              var objectId = this.getAttribute('post-id');
              // assign new link to the Delete post anchor
              document.getElementById('delete-post').href = "/delete_post/"+objectId;
          });
      }
  });