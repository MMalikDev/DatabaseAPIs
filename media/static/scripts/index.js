function handleHeaderHeight() {
  const header = document.querySelector(".page-header");
  const content = document.querySelector("#content");

  function setHeaderHeight() {
    const headerHeight = header.offsetHeight;
    content.style.setProperty("--header-height", `${headerHeight}px`);
  }

  if (!header) return;
  setHeaderHeight();
  window.addEventListener("resize", setHeaderHeight);
}

function handleThemeSwitch() {
  const themeSwitcher = document.querySelector("[data-theme-picker]");
  const theme = document.documentElement;

  function setDarkTheme() {
    theme.setAttribute("data-theme", "dark");
  }

  function setLightTheme() {
    theme.setAttribute("data-theme", "light");
  }

  function switchTheme() {
    theme.getAttribute("data-theme") === "dark"
      ? setLightTheme()
      : setDarkTheme();
  }

  if (!themeSwitcher) return;
  themeSwitcher.addEventListener("click", switchTheme);
}

function handleNavMenu() {
  const navigation = document.querySelector("#primary-navigation");
  const menuToggle = document.querySelector("#menu-toggle");
  const footer = document.querySelector("footer");
  const main = document.querySelector("main");
  const mediaQuery = window.matchMedia("(min-width: 600px)");
  const once = { once: true };

  function closeNavigation() {
    navigation.setAttribute("data-state", "closed");
    menuToggle.setAttribute("aria-expanded", "false");
    main.removeEventListener("click", closingNavigation);
    footer.removeEventListener("click", closingNavigation);
  }

  function closingNavigation() {
    navigation.setAttribute("data-state", "closing");
    navigation.addEventListener("animationend", closeNavigation, once);
  }

  function openNavigation() {
    navigation.setAttribute("data-state", "opened");
    menuToggle.setAttribute("aria-expanded", "true");
    main.addEventListener("click", closingNavigation, once);
    footer.addEventListener("click", closingNavigation, once);
  }

  function toggleNavigation() {
    const state = navigation.getAttribute("data-state");
    state === "closed" ? openNavigation() : closingNavigation();
  }

  function handleNavChange(e) {
    if (e.matches) closeNavigation();
  }

  if (!navigation) return;
  mediaQuery.addEventListener("change", handleNavChange);
  menuToggle.addEventListener("click", toggleNavigation);
}

function setCopyright() {
  const currentYear = document.querySelector("#currentYear");

  if (!currentYear) return;
  currentYear.innerHTML = new Date().getFullYear();
}

function setTheme() {
  const theme = document.documentElement;
  const noPreference = !("theme" in localStorage);
  const preferenceLight = localStorage.theme === "light";
  const themeDark = theme.getAttribute("data-theme") === "dark";
  const defaultDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

  const setDarkMode =
    !preferenceLight || (noPreference && defaultDark) || themeDark;

  setDarkMode
    ? theme.setAttribute("data-theme", "dark")
    : theme.setAttribute("data-theme", "light");
}

function debug() {
  const root = document.querySelector(":root");
  root.style.setProperty("--outline-color", "green");
}

handleHeaderHeight();
handleThemeSwitch();
handleNavMenu();
setCopyright();
setTheme();

// debug();
