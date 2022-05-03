
			
// Dropdown Menu Fade    
jQuery(document).ready(function(){
    $(".dropdown").hover(
        function() { $('.dropdown-menu', this).stop().fadeIn("fast");
        },
        function() { $('.dropdown-menu', this).stop().fadeOut("fast");
    });
});

// Dropdown Menu Fade end   

  // for counter 
//-- Plugin implementation
(function($) {
  $.fn.countTo = function(options) {
    return this.each(function() {
      //-- Arrange
      var FRAME_RATE = 60; // Predefine default frame rate to be 60fps
      var $el = $(this);
      var countFrom = parseInt($el.attr('data-count-from'));
      var countTo = parseInt($el.attr('data-count-to'));
      var countSpeed = $el.attr('data-count-speed'); // Number increment per second

      //-- Action
      var rafId;
      var increment;
      var currentCount = countFrom;
      var countAction = function() {              // Self looping local function via requestAnimationFrame
        if(currentCount < countTo) {              // Perform number incremeant
          $el.text(Math.floor(currentCount));     // Update HTML display
          increment = countSpeed / FRAME_RATE;    // Calculate increment step
          currentCount += increment;              // Increment counter
          rafId = requestAnimationFrame(countAction);
        } else {                                  // Terminate animation once it reaches the target count number
          $el.text(countTo);                      // Set to the final value before everything stops
          //cancelAnimationFrame(rafId);
        }
      };
      rafId = requestAnimationFrame(countAction); // Initiates the looping function
    });
  };
}(jQuery));

//-- Executing
$('.number-counter').countTo();	


// Back to top 
 
$('#top-scrolltop').on('click',function(){
 $('html, body').animate({scrollTop:0},500);
});

$(function ($) {
    "use strict";

	$(".back-to-top").addClass("hidden-top");
		$(window).scroll(function () {
		if ($(this).scrollTop() === 0) {
			$(".back-to-top").addClass("hidden-top")
		} else {
			$(".back-to-top").removeClass("hidden-top")
		}
	});

	$('.back-to-top').click(function () {
		$('body,html').animate({scrollTop:0}, 1200);
		return false;
	});	
});

// sticky_header 
$(window).scroll(function() {
  if ($(this).scrollTop() > 211){
    $('.navbar-area').addClass("is-sticky");
  } else{
    $('.navbar-area').removeClass("is-sticky");
  }
});

 // search   
$(document).ready(function(){
	$('a[href="#search"]').on('click', function(event) {                    
		$('#search').addClass('open');
		$('#search > form > input[type="search"]').focus();
	});            
	$('#search, #search button.close').on('click keyup', function(event) {
		if (event.target == this || event.target.className == 'close' || event.keyCode == 27) {
			$(this).removeClass('open');
		}
	});            
});


//mobile menu script


function openNav() {
  document.getElementById("mySidenav").style.width = "100%";
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
}