(function() {
    // Load the script
    var script = document.createElement("SCRIPT");
    script.src = 'https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js';
    script.type = 'text/javascript';
    script.onload = function() {
        var $ = window.jQuery;
        setInterval(function(){

         $(".field-teacher").hide()
         $(".field-image_path").hide()

         }, 50);

    };
    document.getElementsByTagName("head")[0].appendChild(script);
})();


function getAttendance(){

$.get( "/get/attendance/", function( data ) {
  $("#id_teacher").val(data["teacher_name"])
  $("#id_image_path").val(data["image_path"])
  $('#submit_btn').click()
  alert("Attendance Marked Successfully")

});

}