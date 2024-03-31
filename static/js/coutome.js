// home-product-slider js


$('.product-list-slider').slick({

  autoplay: true,
  autoplaySpeed: 1000,
  slidesToShow: 4,
  prevArrow: false,
  nextArrow: false,
  pauseOnHover: true,
  responsive: [
    {
      breakpoint: 1440,
      settings: {
        arrows: false,
        autoplay: true,
        autoplaySpeed: 1000,
        prevArrow: false,
        centerMode: false,
        nextArrow: false,
        slidesToShow: 3
      }
    },
    {
      breakpoint: 1024,
      settings: {
        arrows: false,
        autoplay: true,
        autoplaySpeed: 1000,
        prevArrow: false,
        centerMode: false,
        nextArrow: false,
        slidesToShow: 2
      }
    },
    {
      breakpoint: 768,
      settings: {
        arrows: false,
        autoplay: true,
        autoplaySpeed: 1000,
        prevArrow: false,
        centerMode: false,
        nextArrow: false,
        slidesToShow: 1
      }
    },
    {
      breakpoint: 480,
      settings: {
        arrows: false,
        autoplay: true,
        autoplaySpeed: 1000,
        centerMode: false,
        prevArrow: false,
        nextArrow: false,
        slidesToShow: 1
      }
    }
  ]
});

// ////

// product-page sub-prjct-js

$(document).ready(function () {
  // Display the first image by default
  displayLargeImage($(".thumbnail:first").attr("src"));

  // Click event for thumbnail images
  $(".thumbnail").click(function () {
    var imageSrc = $(this).attr("src");
    displayLargeImage(imageSrc);
  });

  // Click event to toggle large image container
  $("#toggle-button").click(function () {
    $("#large-image-container").toggle();
  });
});

function displayLargeImage(imageSrc) {
  // Get the large image container and the large image element
  var largeImageContainer = $("#large-image-container");
  var largeImage = $("#large-image");

  // Set the source of the large image
  largeImage.attr("src", imageSrc);

  // Display the large image container
  largeImageContainer.show();
}

