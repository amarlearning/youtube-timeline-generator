$(document).ready(function () {
  $("form").on("submit", function (event) {
    event.preventDefault();
    var videoUrl = $("#video_url").val();
    $("#spinner").css("display", "block");
    $("button[type='submit']").prop("disabled", true);
    $.post("/submit", { video_url: videoUrl }, function (data) {
      $("#spinner").css("display", "none");
      $("button[type='submit']").prop("disabled", false);
      if (data) {
        $("#data").css("padding", "10px");
      }
      $("#data").html(JSON.stringify(data).replace(/^"|"$/g, ""));
    })
      .fail(function () {
        alert("An error occurred. Please try again.");
      })
      .always(function () {
        $("#spinner").css("display", "none");
        $("button[type='submit']").prop("disabled", false);
      });
  });
});
