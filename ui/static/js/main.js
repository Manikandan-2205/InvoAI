$(document).ready(function() {
            // Load sidebar state from localStorage
            const isSidebarCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
            const openMenus = JSON.parse(localStorage.getItem('openMenus') || '[]');
            
            // Apply saved state
            if (isSidebarCollapsed) {
                $('#sidebar').addClass('collapsed');
                $('#toggleSidebar i').removeClass('fa-chevron-left').addClass('fa-chevron-right');
            }
            
            // Apply open menus
            openMenus.forEach(menuId => {
                $(`#${menuId}`).addClass('open');
                $(`#${menuId} .submenu`).addClass('open');
            });
            
            // Toggle sidebar
            $('#toggleSidebar').on('click', function() {
                $('#sidebar').toggleClass('collapsed');
                const isCollapsed = $('#sidebar').hasClass('collapsed');
                
                // Update toggle button icon
                if (isCollapsed) {
                    $(this).find('i').removeClass('fa-chevron-left').addClass('fa-chevron-right');
                } else {
                    $(this).find('i').removeClass('fa-chevron-right').addClass('fa-chevron-left');
                }
                
                // Save state to localStorage
                localStorage.setItem('sidebarCollapsed', isCollapsed);
            });
            
            // Toggle submenus
            $('.has-submenu > .menu-link').on('click', function(e) {
                e.preventDefault();
                
                const parent = $(this).parent('.has-submenu');
                const submenu = parent.find('.submenu');
                
                // Close other submenus if sidebar is collapsed
                if ($('#sidebar').hasClass('collapsed')) {
                    $('.has-submenu').not(parent).removeClass('open');
                    $('.submenu').not(submenu).removeClass('open');
                }
                
                // Toggle current submenu
                parent.toggleClass('open');
                submenu.toggleClass('open');
                
                // Save open menus to localStorage
                const openMenus = [];
                $('.has-submenu.open').each(function() {
                    openMenus.push($(this).attr('id'));
                });
                localStorage.setItem('openMenus', JSON.stringify(openMenus));
            });
            
            // Mobile menu handling
            if ($(window).width() <= 768) {
                $('#sidebar').addClass('collapsed');
                
                $('.has-submenu > .menu-link').on('click', function() {
                    if ($('#sidebar').hasClass('collapsed')) {
                        $('#mobileOverlay').addClass('active');
                        $('#sidebar').removeClass('collapsed');
                    }
                });
                
                $('#mobileOverlay').on('click', function() {
                    $(this).removeClass('active');
                    $('#sidebar').addClass('collapsed');
                });
            }
            
            // Update on window resize
            $(window).on('resize', function() {
                if ($(window).width() > 768) {
                    $('#mobileOverlay').removeClass('active');
                } else {
                    if (!$('#sidebar').hasClass('collapsed')) {
                        $('#mobileOverlay').addClass('active');
                    }
                }
            });
            
            // Set active menu item
            $('.menu-link').on('click', function() {
                $('.menu-link').removeClass('active');
                $(this).addClass('active');
            });
        });