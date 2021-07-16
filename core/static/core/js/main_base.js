const handleScrollTop = () => {
  $(window).scroll(function () {
    if ($(this).scrollTop() >= 50) {
      $('#return-to-top').fadeIn(200);
    } else {
      $('#return-to-top').fadeOut(200);
    }
  });
  $('#return-to-top').click(function () {
    $('body,html').animate(
      {
        scrollTop: 0,
      },
      500
    );
  });
}

const lightboxInit = () => {
  $(document).on('click', '[data-toggle="lightbox"]', function (event) {
    event.preventDefault();
    $(this).ekkoLightbox();
  });
}

handleScrollTop();
lightboxInit();