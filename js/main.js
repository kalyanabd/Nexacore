var DREAMIT = {};
(function($) {

	"use strict";

	//Loading Preloader
	function handlePreloader() {
		if($('.preloader').length){
			$('.preloader').delay(200).fadeOut(500);
		}
	}

	// Mobile Menu js
    $('.mobile-menu nav').meanmenu({
        meanScreenWidth: "991",
        meanMenuContainer: ".mobile-menu",
        meanMenuOpen: "<span></span> <span></span> <span></span>",
        onePage: false,
    });
  

    //Header Search js
    if($('.search-box-outer').length) {
        $('.search-box-outer').on('click', function() {
            $('body').addClass('search-active');
        });
        $('.close-search').on('click', function() {
            $('body').removeClass('search-active');
        });
    }

	// sticky
	var wind = $(window);
	var sticky = $('#sticky-header');
	wind.on('scroll', function () {
		var scroll = wind.scrollTop();
		if (scroll < 100) {
			sticky.removeClass('sticky');
		} else {
			sticky.addClass('sticky');
		}
	});

    // counterUp
    $('.counter').counterUp({
        delay: 10,
        time: 1000
    });

	// Data background image
    $("[data-background]").each(function() {
        $(this).css("background-image", "url(" + $(this).attr("data-background") + ")");
    });

	// =======< accordion js >========
    $(".accordion > li:eq(0) a").addClass("active").next().slideDown();
    $('.accordion a').on('click', function (j) {
        var dropDown = $(this).closest("li").find("p");

        $(this).closest(".accordion").find("p").not(dropDown).slideUp();

        if ($(this).hasClass("active")) {
            $(this).removeClass("active");
        } else {
            $(this).closest(".accordion").find("a.active").removeClass("active");
            $(this).addClass("active");
        }

        dropDown.stop(false, true).slideToggle();

        j.preventDefault();
    });


    // process home four tab
    document.addEventListener("DOMContentLoaded", function() {
        var tabBtns = document.querySelectorAll(".tab-btn");
        var tabContents = document.querySelectorAll(".tab-content");

        // Default active state
        if (tabBtns.length > 0 && !document.querySelector(".tab-btn.active")) {
            tabBtns[0].classList.add("active");
        }
        if (tabContents.length > 0 && !document.querySelector(".tab-content.active")) {
            tabContents[0].classList.add("active");
        }

        // Tab click event
        tabBtns.forEach(function(btn) {
            btn.addEventListener("click", function() {
                tabBtns.forEach(function(b) { b.classList.remove("active"); });
                tabContents.forEach(function(c) { c.classList.remove("active"); });

                btn.classList.add("active");

                var target = document.getElementById(btn.dataset.tab);
                if (target) {
                    target.classList.add("active");
                }
            });
        });
    });


	//Progress Bar
	if ($('.progress-line').length) {
		$('.progress-line').appear(function () {
			var el = $(this);
			var percent = el.data('width');
			$(el).css('width', percent + '%');
		}, { accY: 0 });
	}


	// Scroll to a Specific Div
	if($('.scroll-to-target').length){
		$(".scroll-to-target").on('click', function() {
			var target = $(this).attr('data-target');
		   // animate
		   $('html, body').animate({
			   scrollTop: $(target).offset().top
			 }, 0);

		});
	}

	// Elements Animation
	if($('.wow').length){
		var wow = new WOW(
		  {
			boxClass:     'wow',
			animateClass: 'animated',
			offset:       0,
			mobile:       false,
			live:         true
		  }
		);
		wow.init();
	}

	// count Bar
	if ($(".count-bar").length) {
		$(".count-bar").appear(
			function () {
					var el = $(this);
					var percent = el.data("percent");
					$(el).css("width", percent).addClass("counted");
				}, {
					accY: -50
			}
		);
	}


/* ==============================
   loading
   ============================== */

	$(window).on('load', function() {
		handlePreloader();
	});

	//===== Nice select js
    if ($('select').length){
        $('select').niceSelect();
    }

    //======< Custom Tab >======
    $('.tab ul.tabs').addClass('active').find('> li:eq(0)').addClass('current');

    $(".tab ul.tabs li a").on("click", function (g) {
        var tab = $(this).closest('.tab'),
            index = $(this).closest('li').index();
    
        tab.find('ul.tabs > li').removeClass('current');
        $(this).closest('li').addClass('current');
    
        tab.find('.tab_content').find('div.tabs_item').not('div.tabs_item:eq(' + index + ')').slideUp();
        tab.find('.tab_content').find('div.tabs_item:eq(' + index + ')').slideDown();
    
        g.preventDefault();
    });

	//Text Count
	if($('.count-box').length){
		$('.count-box').appear(function(){
			var $t = $(this),
				n = $t.find(".count-text").attr("data-stop"),
				r = parseInt($t.find(".count-text").attr("data-speed"), 10);

			if (!$t.hasClass("counted")) {
				$t.addClass("counted");
				$({
					countNum: $t.find(".count-text").text()
				}).animate({
					countNum: n
				}, {
					duration: r,
					easing: "linear",
					step: function() {
						$t.find(".count-text").text(Math.floor(this.countNum));
					},
					complete: function() {
						$t.find(".count-text").text(this.countNum);
					}
				});
			}

		},{accY: 0});
	}

	/* Popup Video */
	if ($('.popup-video').length) {
		$('.popup-video').magnificPopup({
			type: 'iframe',
			mainClass: 'mfp-fade',
			removalDelay: 160,
			preloader: false,
			fixedContentPos: true
		});
	}


	/* Image Reveal Animation */
	if ($('.reveal').length) {
        gsap.registerPlugin(ScrollTrigger);
        var revealContainers = document.querySelectorAll(".reveal");
        revealContainers.forEach(function(container) {
            var image = container.querySelector("img");
            var tl = gsap.timeline({
                scrollTrigger: {
                    trigger: container,
                    toggleActions: "play none none none"
                }
            });
            tl.set(container, {
                autoAlpha: 1
            });
            tl.from(container, 1, {
                xPercent: -100,
                ease: Power2.out
            });
            tl.from(image, 1, {
                xPercent: 100,
                scale: 1,
                delay: -1,
                ease: Power2.out
            });
        });
    }

	/* Text Effect Animation */
	if ($('.text-anime-3').length) {		
		var animatedTextElements = document.querySelectorAll('.text-anime-3');
		
		animatedTextElements.forEach(function(element) {
			//Reset if needed
			if (element.animation) {
				element.animation.progress(1).kill();
				element.split.revert();
			}

			element.split = new SplitText(element, {
				type: "lines,words,chars",
				linesClass: "split-line",
			});
			gsap.set(element, { perspective: 400 });

			gsap.set(element.split.chars, {
				opacity: 0,
				x: "50",
			});

			element.animation = gsap.to(element.split.chars, {
				scrollTrigger: { trigger: element, start: "top 90%" },
				x: "0",
				y: "0",
				rotateX: "0",
				opacity: 1,
				duration: 1,
				ease: Back.easeOut,
				stagger: 0.02,
			});
		});		
	}

	// Title Animation
    var splitTitleLines = gsap.utils.toArray(".title-anim");

    splitTitleLines.forEach(function(splitTextLine) {
      var tl = gsap.timeline({
        scrollTrigger: {
          trigger: splitTextLine,
          start: 'top 90%',
          end: 'bottom 60%',
          scrub: false,
          markers: false,
          toggleActions: 'play none none none'
        }
      });
      var itemSplitted = new SplitText(splitTextLine, { type: "words, lines" });
      gsap.set(splitTextLine, { perspective: 400 });
      itemSplitted.split({ type: "lines" });
      tl.from(itemSplitted.lines, { duration: 1, delay: 0.3, opacity: 0, rotationX: -80, force3D: true, transformOrigin: "top center -50", stagger: 0.1 });
    });

	// Scroll down area start here ***
	$("#scrollDown").on("click", function () {
		setTimeout(function () {
			$("html, body").animate({ scrollTop: "+=1000px" }, "slow");
		}, 1000);
	});
	// Scroll down area end here ***

    // Home one band-active js
    var bandSlider = new Swiper(".band-active", {
        speed: 1500,
        slidesPerView: 4,
        spaceBetween: 30,
        loop: true,
        autoplay: true,
        breakpoints: {
            1920: { slidesPerView: 6 },
            1400: { slidesPerView: 5 },
            1200: { slidesPerView: 4 },
            992:  { slidesPerView: 3 },
            768:  { slidesPerView: 3 },
            576:  { slidesPerView: 2 },
            0:    { slidesPerView: 1 },
        },
        navigation: {
            nextEl: ".slider-next",
            prevEl: ".slider-prev",
        },
    });

    // Home one testimonial-active js
    var testiSlider = new Swiper(".testimonial-active", {
        speed: 1500,
        slidesPerView: 3,
        spaceBetween: 30,
        loop: true,
        centeredSlides: true,
        breakpoints: {
            1920: { slidesPerView: 3 },
            1400: { slidesPerView: 3 },
            1200: { slidesPerView: 3 },
            992:  { slidesPerView: 2 },
            768:  { slidesPerView: 2 },
            576:  { slidesPerView: 1 },
            0:    { slidesPerView: 1 },
        },
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
            dynamicBullets: true
        },
        keyboard: {
            enabled: true,
            onlyInViewport: true,
        }
    });

    // Home two testi-active js
    var testiSlider2 = new Swiper(".testi-active", {
        speed: 1500,
        slidesPerView: 2,
        spaceBetween: 30,
        loop: true,
        autoplay: true,
        breakpoints: {
            1920: { slidesPerView: 2 },
            1400: { slidesPerView: 2 },
            1200: { slidesPerView: 2 },
            992:  { slidesPerView: 2 },
            768:  { slidesPerView: 2 },
            576:  { slidesPerView: 1 },
            0:    { slidesPerView: 1 },
        },
        navigation: {
            nextEl: ".slider-next",
            prevEl: ".slider-prev",
        },
        keyboard: {
            enabled: true,
            onlyInViewport: true,
        }
    });


    // Home four testi active2 js
    document.addEventListener("DOMContentLoaded", function () {
        var testiSlider3 = new Swiper(".testi-active2", {
            speed: 1000,
            slidesPerView: 1,
            loop: true,
            autoplay: false,
            spaceBetween: 20,
            breakpoints: {
                1920: { slidesPerView: 1 },
                1400: { slidesPerView: 1 },
                1200: { slidesPerView: 1 },
                992:  { slidesPerView: 2 },
                768:  { slidesPerView: 2 },
                576:  { slidesPerView: 1 },
                0:    { slidesPerView: 1 },
            },
        });

        // Select all avatar divs
        var avatars = document.querySelectorAll(".testi-avatars-img > div");

        function setActiveAvatar(index) {
            avatars.forEach(function(a) { a.classList.remove("active"); });
            if (avatars[index]) {
                avatars[index].classList.add("active");
            }
        }

        avatars.forEach(function(avatar, index) {
            avatar.addEventListener("click", function() {
                testiSlider3.slideToLoop(index);
                setActiveAvatar(index);
            });
        });

        testiSlider3.on("slideChange", function() {
            setActiveAvatar(testiSlider3.realIndex);
        });

        // Default active
        setActiveAvatar(0);
    });


    // Gsap animation split chars
    gsap.registerPlugin(ScrollTrigger, SplitText, TweenMax);

    var splitChars = document.querySelectorAll(".split_chars");

    splitChars.forEach(function(item) {
        var isScrollAble = true,
            tweenOptions = {
                duration: 0.3,
                delay: 0.3,
                autoAlpha: 0,
                stagger: 0.1,
                ease: "power2.out",
            },
            scrollTrigger = {
                trigger: item,
                start: "top 90%",
                markers: false,
            };

        if (item.hasAttribute("data-duration")) {
            tweenOptions.duration = item.getAttribute("data-duration");
        }

        if (item.hasAttribute("data-delay")) {
            tweenOptions.delay = item.getAttribute("data-delay");
        }

        if (item.hasAttribute("data-ease")) {
            tweenOptions.ease = item.getAttribute("data-ease");
        }

        if (item.hasAttribute("data-stagger")) {
            tweenOptions.stagger = item.getAttribute("data-stagger");
        }

        if (item.hasAttribute("data-translateX")) {
            tweenOptions.x = item.getAttribute("data-translateX");
        }

        if (item.hasAttribute("data-translateY")) {
            tweenOptions.y = item.getAttribute("data-translateY");
        }

        // FIX: was checking data-translateX twice (duplicate condition bug)
        if (!item.hasAttribute("data-translateX") && !item.hasAttribute("data-translateY")) {
            tweenOptions.x = 0;
        }

        if (item.hasAttribute("data-scroll-trigger")) {
            isScrollAble = item.getAttribute("data-scroll-trigger");
        }

        if (item.hasAttribute("data-trigger-start")) {
            scrollTrigger.start = item.getAttribute("data-trigger-start");
        }

        if (isScrollAble) {
            tweenOptions.scrollTrigger = scrollTrigger;
        }

        var splittedText = new SplitText(item, {
            type: "chars, words",
        });

        gsap.from(splittedText.chars, tweenOptions);
    });

    // Character Come Animation
    var char_come = document.querySelectorAll(".animation__char_come");

    char_come.forEach(function(el) {
        var split_char = new SplitText(el, { type: "chars, words" });
        gsap.from(split_char.chars, { duration: 1, x: 70, autoAlpha: 0, stagger: 0.05 });
    });

    // Character Come Long Animation
    var char_come_long = document.querySelectorAll(".animation__char_come_long");

    char_come_long.forEach(function(el) {
        var split_char = new SplitText(el, { type: "chars, words" });
        gsap.from(split_char.chars, { duration: 1, x: 70, autoAlpha: 0, stagger: 0.15 });
    });

    // Split text animation
    gsap.registerPlugin(ScrollTrigger);
    document.querySelectorAll(".split-text").forEach(function(element) {
        var text = element.textContent;
        element.innerHTML = "";
        
        text.split("").forEach(function(char) {
            var span = document.createElement("span");
            span.classList.add("char");
            span.textContent = (char === " ") ? "\u00A0" : char;
            element.appendChild(span);
        });

        gsap.to(element.querySelectorAll(".char"), {
            opacity: 1,
            y: 0,
            rotation: 0,
            duration: 0.5,
            stagger: 0.05,
            ease: "back.out(1.7)",
            scrollTrigger: {
                trigger: element,
                start: "top 80%",
                toggleActions: "play none none reverse",
                markers: false
            }
        });
    });
    
    // fade in
    gsap.registerPlugin(ScrollTrigger);

    if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
        var itemsToReveal = gsap.utils.toArray(".fade-in");
        itemsToReveal.forEach(function(item) {
            gsap.set(item, {
                autoAlpha: 0,
                y: 50
            });
            ScrollTrigger.create({
                trigger: item,
                start: "top bottom-=100px",
                once: true,
                onEnter: function() {
                    gsap.to(item, {
                        autoAlpha: 1,
                        y: 0
                    });
                }
            });
        });
    }

    // service sticky scroll
	gsap.registerPlugin(ScrollTrigger);

	var width = window.innerWidth;
	var boxes = gsap.utils.toArray(".single-service-box");
	var container = document.getElementById("scroll-container");
	var stickyBox = document.getElementById("sticky-box");

	// Sticky right box
	if (width >= 1200) {
		ScrollTrigger.create({
            trigger: stickyBox,
            start: "top 9%",
            endTrigger: container,
            end: (width >= 1700)
                ? "bottom 103.2%"
                : (width >= 1400)
                ? "bottom 180%"
                : "bottom 160%",
            pin: true,
            pinSpacing: false,
            scrub: true,
		});
	}

	// Activate content boxes
	boxes.forEach(function(box, i) {
		ScrollTrigger.create({
            trigger: box,
            start: "top 50%",
            end: "bottom 50%",
            onEnter: function() {
                for (var j = 0; j <= i; j++) {
                    boxes[j].classList.add("before-opacity-0");
                }
            },
            onLeaveBack: function() {
                for (var j = i; j < boxes.length; j++) {
                    boxes[j].classList.remove("before-opacity-0");
                }
            }
		});
	});
    
    // type animation text
    var typingText = "AUTOMATION";
    var typingEl = document.querySelector(".typing");
    if (typingEl) {
        function typingEffect() {
            typingEl.textContent = "";
            var i = 0;
            function typeChar() {
                typingEl.textContent = typingText.substring(0, i + 1);
                i++;
                if (i < typingText.length) {
                    setTimeout(typeChar, 200);
                } else {
                    setTimeout(typingEffect, 1000);
                }
            }
            typeChar();
        }
        typingEffect();
    }


    // particles js all
    document.addEventListener("DOMContentLoaded", function () {
        var particleDivs = [
            'js-particles', 
            'js-particles-testimonial', 
            'js-particles-footer'
        ];

        particleDivs.forEach(function(id) {
            var el = document.getElementById(id);
            if (el) {
                particlesJS(id, {
                    'particles': {
                        'number': { 'value': 38 },
                        'color': { 'value': ['#37B884', '#EB7043', '#6766FF'] },
                        'shape': { 'type': 'circle' },
                        'opacity': {
                            'value': 1,
                            'random': false,
                            'anim': { 'enable': false }
                        },
                        'size': {
                            'value': 3,
                            'random': true,
                            'anim': { 'enable': false }
                        },
                        'line_linked': { 'enable': false },
                        'move': {
                            'enable': true,
                            'speed': 2,
                            'direction': 'none',
                            'random': true,
                            'straight': false,
                            'out_mode': 'out'
                        }
                    },
                    'interactivity': {
                        'detect_on': 'canvas',
                        'events': {
                            'onhover': { 'enable': false },
                            'onclick': { 'enable': false },
                            'resize': true
                        }
                    },
                    'retina_detect': true
                });
            }
        });
    });

})(window.jQuery);