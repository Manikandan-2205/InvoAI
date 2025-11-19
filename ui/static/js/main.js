 $(document).ready(function () {
        const $sidebar = $('#sidebar');
        const $toggleBtn = $('#toggleSidebar');
        const $mobileOverlay = $('#mobileOverlay');
        const $menuItems = $('.has-submenu, .account-menu');
        const $userInfoToggle = $('#userInfoToggle');
        const $userMenu = $('#userMenu');

        // Load saved state from localStorage
        const savedSidebarState = localStorage.getItem('sidebarCollapsed');
        const savedMenuStates = JSON.parse(localStorage.getItem('menuStates') || '{}');

        // Apply saved sidebar state
        if (savedSidebarState === 'true') {
          $sidebar.addClass('collapsed');
        }

        // Apply saved menu states
        $.each(savedMenuStates, function (menuId, isActive) {
          if (isActive) {
            $('#' + menuId).addClass('active');
          }
        });

        // Set active menu based on current page
        function setActiveMenu() {
          const currentPath = window.location.pathname;
          const $menuLinks = $('.menu-link');

          $menuLinks.each(function () {
            const $link = $(this);
            $link.removeClass('active');
            if ($link.attr('href') === currentPath) {
              $link.addClass('active');

              // Also activate parent menus
              let $parentMenu = $link.closest('.has-submenu, .account-menu');
              while ($parentMenu.length) {
                $parentMenu.addClass('active');
                $parentMenu = $parentMenu.parent().closest('.has-submenu, .account-menu');
              }
            }
          });
        }

        setActiveMenu();

        // Toggle sidebar
        $toggleBtn.on('click', function () {
          $sidebar.toggleClass('collapsed');

          // Save state to localStorage
          localStorage.setItem('sidebarCollapsed', $sidebar.hasClass('collapsed'));

          // Close all submenus when collapsing sidebar
          if ($sidebar.hasClass('collapsed')) {
            $menuItems.removeClass('active');

            const menuStates = {};
            $menuItems.each(function () {
              menuStates[this.id] = false;
            });
            localStorage.setItem('menuStates', JSON.stringify(menuStates));
          }

          // Close user menu when collapsing sidebar
          $userMenu.removeClass('show');
        });

        // Handle submenu toggle
        $menuItems.each(function () {
          const $item = $(this);
          const $link = $item.find('.menu-link').first();

          $link.on('click', function (e) {
            if (!$sidebar.hasClass('collapsed')) {
              e.preventDefault();

              const isActive = $item.hasClass('active');
              $item.toggleClass('active');

              // Close other open submenus at the same level
              if (!isActive) {
                $menuItems.not($item).removeClass('active');
              }

              // Save menu states to localStorage
              const menuStates = {};
              $menuItems.each(function () {
                menuStates[this.id] = $(this).hasClass('active');
              });
              localStorage.setItem('menuStates', JSON.stringify(menuStates));
            }
          });
        });

        // Handle user menu toggle
        $userInfoToggle.on('click', function () {
          $userMenu.toggleClass('show');
        });

        // Close dropdowns when clicking outside
        $(document).on('click', function (e) {
          if (!$userInfoToggle.is(e.target) && $userInfoToggle.has(e.target).length === 0 &&
            !$userMenu.is(e.target) && $userMenu.has(e.target).length === 0) {
            $userMenu.removeClass('show');
          }

          // Close submenus when clicking outside (for mobile)
          if (!$sidebar.is(e.target) && $sidebar.has(e.target).length === 0 && $(window).width() <= 768) {
            $menuItems.removeClass('active');
          }
        });

        // Handle mobile overlay
        $mobileOverlay.on('click', function () {
          $sidebar.removeClass('mobile-open');
          $mobileOverlay.removeClass('active');
          $userMenu.removeClass('show');
        });

        // Responsive behavior
        function handleResize() {
          if ($(window).width() <= 768) {
            $sidebar.addClass('collapsed');
          }
        }

        $(window).on('resize', handleResize);
        handleResize(); // Initial check
      });