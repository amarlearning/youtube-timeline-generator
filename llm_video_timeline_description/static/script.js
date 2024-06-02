$(document).ready(function () {
  $("form").on("submit", function (event) {
    event.preventDefault();
    var videoUrl = $("#video_url").val();

    showLoadingSpinner();

    $.post("/submit", { video_url: videoUrl }, function (data) {
      hideLoadingSpinner();
      if (data) {
        $("#response").css("display", "block");
        $("#summary-content").html(data.summary.replace(/\n/g, "<br>"));
        $("#timeline-content").html(data.timeline.replace(/\n/g, "<br>"));
      }
    })
      .fail(function () {
        alert("An error occurred. Please try again.");
      })
      .always(function () {
        hideLoadingSpinner();
      });
  });
});

function showLoadingSpinner() {
  $("#spinner").css("display", "block");
  $("button[type='submit']").prop("disabled", true);
}

function hideLoadingSpinner() {
  $("#spinner").css("display", "none");
  $("button[type='submit']").prop("disabled", false);
}

$(".copy-icon").on("click", function () {
  var copyTarget = $(this).data("copy-target");
  var textToCopy = $(copyTarget).html();

  navigator.clipboard
    .writeText(textToCopy)
    .then(function () {
      $("#copy-toast").toast("show");
    })
    .catch(function () {
      console.log("Failed to copy text");
    });
});
