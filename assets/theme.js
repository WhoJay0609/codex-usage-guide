(function () {
  var key = "codex-guide-theme";
  var allowed = new Set(["system", "light", "dark"]);

  function read() {
    try {
      var value = window.localStorage.getItem(key);
      return allowed.has(value) ? value : "system";
    } catch (_) {
      return "system";
    }
  }

  function apply(value) {
    var theme = allowed.has(value) ? value : "system";
    if (theme === "system") document.documentElement.removeAttribute("data-theme");
    else document.documentElement.setAttribute("data-theme", theme);
    return theme;
  }

  function set(value) {
    var theme = apply(value);
    try {
      if (theme === "system") window.localStorage.removeItem(key);
      else window.localStorage.setItem(key, theme);
      return true;
    } catch (_) {
      return false;
    }
  }

  var initial = read();
  apply(initial);
  window.GUIDE_THEME = { read: read, apply: apply, set: set, current: initial };
})();
