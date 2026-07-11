(function () {
  document.documentElement.classList.add("js");
  var themeSelect = document.querySelector(".theme-select");
  var themeStatus = document.querySelector(".theme-status");
  var mermaidSources = new WeakMap();

  function resolvedTheme() {
    var override = document.documentElement.getAttribute("data-theme");
    if (override === "light" || override === "dark") return override;
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  function mermaidOptions() {
    var dark = resolvedTheme() === "dark";
    return {
      startOnLoad: false,
      securityLevel: "strict",
      theme: "base",
      themeVariables: dark ? {
        fontFamily: 'ui-sans-serif, system-ui, "Noto Sans CJK SC", sans-serif',
        primaryColor: "#24272c", primaryTextColor: "#f5f1e8",
        primaryBorderColor: "#ff9a75", lineColor: "#8fb0ff",
        secondaryColor: "#1c1f23", tertiaryColor: "#24272c"
      } : {
        fontFamily: 'ui-sans-serif, system-ui, "Noto Sans CJK SC", sans-serif',
        primaryColor: "#fffaf0", primaryTextColor: "#11110f",
        primaryBorderColor: "#c44924", lineColor: "#2458d8",
        secondaryColor: "#f7f3ea", tertiaryColor: "#fffaf0"
      }
    };
  }

  function showMermaidFailure(element, source) {
    element.removeAttribute("data-processed");
    element.setAttribute("data-mermaid-failed", "true");
    element.textContent = source;
    var status = element.parentElement && element.parentElement.querySelector(".diagram-status");
    if (!status && element.parentElement) {
      status = document.createElement("p");
      status.className = "diagram-status";
      status.setAttribute("role", "status");
      element.parentElement.insertBefore(status, element);
    }
    if (status) status.textContent = "图表脚本不可用；以下保留可复制的文字源。";
  }

  function renderMermaid() {
    var nodes = Array.from(document.querySelectorAll(".mermaid"));
    if (!nodes.length) return Promise.resolve();
    nodes.forEach(function (element) {
      if (!mermaidSources.has(element)) mermaidSources.set(element, element.textContent.trim());
      element.removeAttribute("data-mermaid-failed");
      element.removeAttribute("data-processed");
      element.textContent = mermaidSources.get(element);
      var status = element.parentElement && element.parentElement.querySelector(".diagram-status");
      if (status) status.remove();
    });
    if (!window.mermaid || typeof window.mermaid.run !== "function") {
      nodes.forEach(function (element) { showMermaidFailure(element, mermaidSources.get(element)); });
      return Promise.resolve();
    }
    window.mermaid.initialize(mermaidOptions());
    return Promise.resolve(window.mermaid.run({ nodes: nodes })).catch(function () {
      nodes.forEach(function (element) { showMermaidFailure(element, mermaidSources.get(element)); });
    });
  }

  if (themeSelect && window.GUIDE_THEME) {
    themeSelect.value = window.GUIDE_THEME.read();
    themeSelect.addEventListener("change", function () {
      var saved = window.GUIDE_THEME.set(themeSelect.value);
      if (themeStatus) themeStatus.textContent = saved ? "主题偏好已保存。" : "主题已应用，但未保存。";
      renderMermaid();
    });
    if (window.matchMedia) {
      var systemTheme = window.matchMedia("(prefers-color-scheme: dark)");
      systemTheme.addEventListener("change", function () {
        if (themeSelect.value === "system") renderMermaid();
      });
    }
  }
  var path = window.location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll("[data-nav]").forEach(function (link) {
    if (link.getAttribute("href") === path) {
      link.setAttribute("aria-current", "page");
    }
  });

  var searchTrigger = document.querySelector(".search-trigger");
  var searchDialog = document.querySelector("#site-search-dialog");
  var searchClose = document.querySelector(".search-close");
  var searchInput = document.querySelector("#site-search-input");
  var searchStatus = document.querySelector("#site-search-status");
  var searchResults = document.querySelector("#site-search-results");
  var activeSearchIndex = -1;
  var renderedSearchOptions = [];

  function normalizeSearchText(value) {
    var text = String(value || "");
    if (text.normalize) text = text.normalize("NFKC");
    return text.toLocaleLowerCase().replace(/[\s\p{P}\p{S}]+/gu, " ").trim();
  }

  function allowedSearchRecords() {
    var data = window.GUIDE_SITE_DATA;
    var index = window.GUIDE_SEARCH_INDEX;
    if (!data || !Array.isArray(data.pages) || !data.fragments ||
        !index || index.schema_version !== 1 || !Array.isArray(index.records)) {
      return null;
    }
    var pageFragments = new Map();
    data.pages.forEach(function (page) {
      if (!page || typeof page.path !== "string" || !Array.isArray(data.fragments[page.path])) return;
      pageFragments.set(page.path, new Set(data.fragments[page.path]));
    });
    return index.records.filter(function (record) {
      if (!record || typeof record.page !== "string" || typeof record.fragment !== "string" ||
          typeof record.title !== "string" || typeof record.section !== "string" ||
          typeof record.text !== "string" || !Array.isArray(record.prompts)) return false;
      var fragments = pageFragments.get(record.page);
      return Boolean(fragments && (!record.fragment || fragments.has(record.fragment)));
    });
  }

  var searchRecords = allowedSearchRecords();

  function setActiveSearchOption(index) {
    if (!searchInput) return;
    if (!renderedSearchOptions.length) {
      activeSearchIndex = -1;
      searchInput.removeAttribute("aria-activedescendant");
      return;
    }
    activeSearchIndex = (index + renderedSearchOptions.length) % renderedSearchOptions.length;
    renderedSearchOptions.forEach(function (option, optionIndex) {
      option.setAttribute("aria-selected", String(optionIndex === activeSearchIndex));
    });
    var active = renderedSearchOptions[activeSearchIndex];
    searchInput.setAttribute("aria-activedescendant", active.id);
    active.scrollIntoView({ block: "nearest" });
  }

  function navigateToSearchOption(option) {
    var target = option && option.dataset.searchTarget;
    if (target) window.location.href = target;
  }

  function renderSearchResults() {
    if (!searchInput || !searchStatus || !searchResults) return;
    searchResults.replaceChildren();
    renderedSearchOptions = [];
    setActiveSearchOption(-1);
    if (searchRecords === null) {
      searchStatus.textContent = "搜索索引暂时不可用，站内导航仍可继续使用。";
      return;
    }
    var query = normalizeSearchText(searchInput.value);
    if (!query) {
      searchStatus.textContent = "输入关键词开始搜索。";
      return;
    }
    var matches = searchRecords.map(function (record) {
      var title = normalizeSearchText(record.title);
      var section = normalizeSearchText(record.section);
      var body = normalizeSearchText([record.text].concat(record.prompts).join(" "));
      var score = section === query ? 100 : section.indexOf(query) >= 0 ? 60 :
        title.indexOf(query) >= 0 ? 40 : body.indexOf(query) >= 0 ? 20 : 0;
      return { record: record, score: score };
    }).filter(function (match) {
      return match.score > 0;
    }).sort(function (left, right) {
      return right.score - left.score || left.record.page.localeCompare(right.record.page, "zh-CN") ||
        left.record.fragment.localeCompare(right.record.fragment, "zh-CN");
    }).slice(0, 12);

    if (!matches.length) {
      searchStatus.textContent = "没有找到匹配结果。";
      return;
    }
    searchStatus.textContent = "找到 " + matches.length + " 条结果。";
    matches.forEach(function (match, index) {
      var record = match.record;
      var option = document.createElement("li");
      option.className = "search-option";
      option.id = "search-option-" + index;
      option.setAttribute("role", "option");
      option.setAttribute("aria-selected", "false");
      option.tabIndex = -1;
      option.dataset.searchTarget = record.page + (record.fragment ? "#" + encodeURIComponent(record.fragment) : "");
      var title = document.createElement("strong");
      title.textContent = record.title;
      var section = document.createElement("span");
      section.textContent = record.section || "页面概览";
      var snippet = document.createElement("small");
      snippet.textContent = record.text.slice(0, 120);
      option.append(title, section, snippet);
      option.addEventListener("mousedown", function (event) { event.preventDefault(); });
      option.addEventListener("click", function () { navigateToSearchOption(option); });
      searchResults.appendChild(option);
      renderedSearchOptions.push(option);
    });
  }

  function openSearch() {
    if (!searchDialog || !searchInput) return;
    searchInput.setAttribute("aria-expanded", "true");
    renderSearchResults();
    if (typeof searchDialog.showModal === "function") searchDialog.showModal();
    else searchDialog.setAttribute("open", "");
    searchInput.focus();
  }

  function closeSearch() {
    if (!searchDialog || !searchDialog.hasAttribute("open")) return;
    searchInput.setAttribute("aria-expanded", "false");
    if (typeof searchDialog.close === "function") searchDialog.close();
    else {
      searchDialog.removeAttribute("open");
      if (searchTrigger) searchTrigger.focus();
    }
  }

  if (searchTrigger && searchDialog && searchInput && searchResults && searchStatus) {
    searchTrigger.addEventListener("click", openSearch);
    searchClose.addEventListener("click", closeSearch);
    searchDialog.addEventListener("cancel", function (event) {
      event.preventDefault();
      closeSearch();
    });
    searchDialog.addEventListener("close", function () {
      searchInput.setAttribute("aria-expanded", "false");
      searchTrigger.focus();
    });
    searchDialog.addEventListener("click", function (event) {
      if (event.target === searchDialog) closeSearch();
    });
    searchInput.addEventListener("input", renderSearchResults);
    searchInput.addEventListener("keydown", function (event) {
      if (event.key === "ArrowDown") {
        event.preventDefault();
        setActiveSearchOption(activeSearchIndex + 1);
      } else if (event.key === "ArrowUp") {
        event.preventDefault();
        setActiveSearchOption(activeSearchIndex - 1);
      } else if (event.key === "Enter" && renderedSearchOptions.length) {
        event.preventDefault();
        navigateToSearchOption(renderedSearchOptions[activeSearchIndex < 0 ? 0 : activeSearchIndex]);
      }
    });
  }

  document.querySelectorAll("main pre > code").forEach(function (code) {
    var pre = code.parentElement;
    if (!pre || pre.closest(".copy-block")) return;
    var sourceText = code.textContent;
    var wrapper = document.createElement("div");
    wrapper.className = "copy-block";
    pre.parentNode.insertBefore(wrapper, pre);
    var tools = document.createElement("div");
    tools.className = "copy-tools";
    var button = document.createElement("button");
    button.className = "copy-button";
    button.type = "button";
    button.textContent = "复制";
    var status = document.createElement("span");
    status.className = "copy-status";
    status.setAttribute("aria-live", "polite");
    tools.append(button, status);
    wrapper.append(tools, pre);
    button.addEventListener("click", function () {
      status.textContent = "";
      button.disabled = true;
      var write = navigator.clipboard && typeof navigator.clipboard.writeText === "function"
        ? navigator.clipboard.writeText(sourceText)
        : Promise.reject(new Error("Clipboard unavailable"));
      Promise.resolve(write).then(function () {
        status.textContent = "已复制";
      }).catch(function () {
        status.textContent = "复制失败，请手动选择文本。";
      }).finally(function () {
        button.disabled = false;
      });
    });
  });

  var menuButton = document.querySelector(".menu-toggle");
  var globalNav = document.querySelector(".global-nav");
  function closeMenu() {
    document.body.classList.remove("nav-open");
    if (menuButton) menuButton.setAttribute("aria-expanded", "false");
  }
  if (menuButton && globalNav) {
    menuButton.addEventListener("click", function () {
      var open = document.body.classList.toggle("nav-open");
      menuButton.setAttribute("aria-expanded", String(open));
      if (open) {
        var firstLink = globalNav.querySelector("a");
        if (firstLink) firstLink.focus();
      }
    });
    globalNav.addEventListener("click", function (event) {
      if (event.target.closest("a")) closeMenu();
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && document.body.classList.contains("nav-open")) {
        closeMenu();
        menuButton.focus();
      }
    });
  }

  var tocLinks = Array.from(document.querySelectorAll(".page-toc a[href^='#']"));
  if ("IntersectionObserver" in window && tocLinks.length) {
    var tocById = new Map(tocLinks.map(function (link) {
      return [decodeURIComponent(link.hash.slice(1)), link];
    }));
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        tocLinks.forEach(function (link) { link.removeAttribute("aria-current"); });
        var link = tocById.get(entry.target.id);
        if (link) link.setAttribute("aria-current", "location");
      });
    }, { rootMargin: "-18% 0px -70%" });
    tocById.forEach(function (_, id) {
      var target = document.getElementById(id);
      if (target) observer.observe(target);
    });
  }

  renderMermaid();
})();
