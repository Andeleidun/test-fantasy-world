// Apply a saved preference before the stylesheet paints. Without one, CSS follows the system.
(() => {
  try {
    const theme = localStorage.getItem('world-guide-theme');
    if (theme === 'light' || theme === 'dark') document.documentElement.dataset.theme = theme;
  } catch { /* Reading still works when browser storage is unavailable. */ }
})();
