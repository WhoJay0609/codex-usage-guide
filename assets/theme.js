(function () {
  var key = "codex-guide-theme";
  var allowed = new Set(["light", "dark"]);

  function read() {
    try {
      var value = window.localStorage.getItem(key);
      return allowed.has(value) ? value : "light";
    } catch (_) {
      return "light";
    }
  }

  function apply(value) {
    var theme = allowed.has(value) ? value : "light";
    document.documentElement.setAttribute("data-theme", theme);
    return theme;
  }

  function set(value) {
    var theme = apply(value);
    try {
      window.localStorage.setItem(key, theme);
      return true;
    } catch (_) {
      return false;
    }
  }

  var initial = read();
  apply(initial);
  window.GUIDE_THEME = { read: read, apply: apply, set: set, current: initial };
})();
