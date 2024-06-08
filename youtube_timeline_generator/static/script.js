$(document).ready(function () {
  $("form").on("submit", function (event) {
    event.preventDefault();
    var videoUrl = $("#video_url").val();

    showLoadingSpinner();

    $.post("/submit", { video_url: videoUrl }, function (data) {
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
  $(".custom-badge-button").html(
    '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>'
  );
  $(".custom-badge-button").prop("disabled", true);
  $("input").prop("disabled", true);
}

function hideLoadingSpinner() {
  $(".custom-badge-button").html("Submit");
  $(".custom-badge-button").prop("disabled", false);
  $("input").prop("disabled", false);
}

$(".copy-icon").on("click", function () {
  var copyTarget = $(this).data("copy-target");
  var textToCopy = $(copyTarget).html();

  var textToCopy = textToCopy.replace(/<br>/g, "");

  navigator.clipboard
    .writeText(textToCopy)
    .then(function () {
      $("#copy-toast").toast("show");
    })
    .catch(function () {
      console.log("Failed to copy text");
    });
});
