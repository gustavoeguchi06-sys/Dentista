(function () {
  const toggle = document.querySelector('.menu-toggle');
  const sidebar = document.querySelector('.sidebar');
  const backdrop = document.querySelector('.sidebar-backdrop');
  const menuLinks = document.querySelectorAll('.menu a');

  if (!toggle || !sidebar) return;

  const closeSidebar = () => {
    sidebar.classList.remove('open');
    document.body.classList.remove('sidebar-open');
  };

  const openSidebar = () => {
    sidebar.classList.add('open');
    document.body.classList.add('sidebar-open');
  };

  toggle.addEventListener('click', function (event) {
    event.stopPropagation();
    if (sidebar.classList.contains('open')) {
      closeSidebar();
    } else {
      openSidebar();
    }
  });

  if (backdrop) {
    backdrop.addEventListener('click', closeSidebar);
  }

  menuLinks.forEach((link) => {
    link.addEventListener('click', () => {
      if (window.innerWidth <= 900) {
        closeSidebar();
      }
    });
  });

  const path = window.location.pathname.replace(/\/+$/, '');
  menuLinks.forEach((link) => {
    try {
      const href = new URL(link.href).pathname.replace(/\/+$/, '');
      if (href === path) {
        link.classList.add('active');
      }
    } catch (error) {
      // ignore invalid URLs
    }
  });

  document.addEventListener('click', (event) => {
    if (window.innerWidth <= 900 && sidebar.classList.contains('open')) {
      const clickInside = sidebar.contains(event.target) || toggle.contains(event.target);
      if (!clickInside) {
        closeSidebar();
      }
    }
  });
})();
