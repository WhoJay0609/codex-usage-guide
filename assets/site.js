(function () {
  var path = window.location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll("[data-nav]").forEach(function (link) {
    if (link.getAttribute("href") === path) {
      link.setAttribute("aria-current", "page");
    }
  });

  if (!window.gsap || !window.ScrollTrigger) return;
  gsap.registerPlugin(ScrollTrigger);

  document.querySelectorAll(".scrub-text").forEach(function (element) {
    var words = element.textContent.trim().split(/\s+/);
    element.innerHTML = words.map(function (word) {
      return '<span class="reveal-word">' + word + '</span>';
    }).join(" ");
    gsap.to(element.querySelectorAll(".reveal-word"), {
      opacity: 1,
      stagger: 0.035,
      ease: "none",
      scrollTrigger: {
        trigger: element,
        start: "top 78%",
        end: "bottom 42%",
        scrub: true
      }
    });
  });

  gsap.utils.toArray(".card, .source-card, .content-block").forEach(function (element) {
    gsap.fromTo(element, { opacity: 0, y: 24, scale: 0.99 }, {
      opacity: 1,
      y: 0,
      scale: 1,
      duration: 0.65,
      ease: "power2.out",
      scrollTrigger: {
        trigger: element,
        start: "top 90%"
      }
    });
  });
})();
