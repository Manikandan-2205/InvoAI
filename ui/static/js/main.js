$(document).ready(function () {
  const $sidebar = $("#sidebar");
  const $toggleBtn = $("#toggleSidebar");
  const $mobileOverlay = $("#mobileOverlay");
  const $menuItems = $(".has-submenu, .account-menu");
  const $userInfoToggle = $("#userInfoToggle");
  const $userMenu = $("#userMenu");


  const savedSidebarState = localStorage.getItem("sidebarCollapsed");
  const savedMenuStates = JSON.parse(
    localStorage.getItem("menuStates") || "{}"
  );


  if (savedSidebarState === "true") {
    $sidebar.addClass("collapsed");
  }


  $.each(savedMenuStates, function (menuId, isActive) {
    if (isActive) {
      $("#" + menuId).addClass("active");
    }
  });


  function setActiveMenu() {
    const currentPath = window.location.pathname;
    const $menuLinks = $(".menu-link");

    $menuLinks.each(function () {
      const $link = $(this);
      $link.removeClass("active");
      if ($link.attr("href") === currentPath) {
        $link.addClass("active");


        let $parentMenu = $link.closest(".has-submenu, .account-menu");
        while ($parentMenu.length) {
          $parentMenu.addClass("active");
          $parentMenu = $parentMenu
            .parent()
            .closest(".has-submenu, .account-menu");
        }
      }
    });
  }

  setActiveMenu();


  $toggleBtn.on("click", function () {
    $sidebar.toggleClass("collapsed");


    localStorage.setItem("sidebarCollapsed", $sidebar.hasClass("collapsed"));


    if ($sidebar.hasClass("collapsed")) {
      $menuItems.removeClass("active");

      const menuStates = {};
      $menuItems.each(function () {
        menuStates[this.id] = false;
      });
      localStorage.setItem("menuStates", JSON.stringify(menuStates));
    }


    $userMenu.removeClass("show");
  });


  $menuItems.each(function () {
    const $item = $(this);
    const $link = $item.find(".menu-link").first();

    $link.on("click", function (e) {
      if (!$sidebar.hasClass("collapsed")) {
        e.preventDefault();

        const isActive = $item.hasClass("active");
        $item.toggleClass("active");


        if (!isActive) {
          $menuItems.not($item).removeClass("active");
        }


        const menuStates = {};
        $menuItems.each(function () {
          menuStates[this.id] = $(this).hasClass("active");
        });
        localStorage.setItem("menuStates", JSON.stringify(menuStates));
      }
    });
  });


  $userInfoToggle.on("click", function () {
    $userMenu.toggleClass("show");
  });


  $(document).on("click", function (e) {
    if (
      !$userInfoToggle.is(e.target) &&
      $userInfoToggle.has(e.target).length === 0 &&
      !$userMenu.is(e.target) &&
      $userMenu.has(e.target).length === 0
    ) {
      $userMenu.removeClass("show");
    }


    if (
      !$sidebar.is(e.target) &&
      $sidebar.has(e.target).length === 0 &&
      $(window).width() <= 768
    ) {
      $menuItems.removeClass("active");
    }
  });


  $mobileOverlay.on("click", function () {
    $sidebar.removeClass("mobile-open");
    $mobileOverlay.removeClass("active");
    $userMenu.removeClass("show");
  });


  function handleResize() {
    if ($(window).width() <= 768) {
      $sidebar.addClass("collapsed");
    }
  }

  $(window).on("resize", handleResize);
  handleResize();
});


$(document).ready(function () {

  $(".select2").each(function () {
    const $this = $(this);
    const placeholderText =
      $this.attr("data-placeholder") || "Select an option";
    $this.select2({
      placeholder: placeholderText,
      allowClear: true,
    });
  });
});
