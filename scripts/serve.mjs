import http from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { resolve, extname, sep } from 'node:path';

const root = resolve('dist');
const port = Number(process.env.PORT || 4173);
const types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.json': 'application/json', '.svg': 'image/svg+xml', '.md': 'text/plain; charset=utf-8', '.tsv': 'text/tab-separated-values; charset=utf-8' };
http.createServer(async (req, res) => {
  try {
    let path = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
    // Also exercise GitHub's project-site prefix during local verification.
    path = path.replace(/^\/test-fantasy-world(?=\/|$)/, '') || '/';
    const file = resolve(root, '.' + path, path.endsWith('/') ? 'index.html' : '');
    if (!file.startsWith(root + sep) || !(await stat(file)).isFile()) throw new Error('Not found');
    res.writeHead(200, { 'Content-Type': types[extname(file)] || 'application/octet-stream' });
    res.end(await readFile(file));
  } catch {
    res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(await readFile(resolve(root, '404.html')));
  }
}).listen(port, '0.0.0.0', () => console.log(`World guide: http://localhost:${port}/test-fantasy-world/`));
