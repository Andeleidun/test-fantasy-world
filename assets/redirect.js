// Static compatibility pages also expose every destination as an ordinary link.
const data = document.getElementById('redirect-destinations');
if (data) {
  const routes = JSON.parse(data.textContent);
  let fragment = location.hash.slice(1);
  try { fragment = decodeURIComponent(fragment); } catch { /* Keep malformed fragments literal. */ }
  const target = routes[fragment] || routes[''];
  if (target) {
    const destination = new URL(target, location.href);
    destination.search = location.search;
    location.replace(destination.href);
  }
}
