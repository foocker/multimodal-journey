/** Render each Markdown article to an independent offline HTML with embedded math/fonts/images. */
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
import MarkdownIt from 'markdown-it';
import texmath from 'markdown-it-texmath';
import katex from 'katex';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const require = createRequire(import.meta.url);
const args = process.argv.slice(2);
if (args.length && (args[0] !== '--out' || args.length !== 2)) throw new Error('Usage: node scripts/build_articles.mjs [--out output-directory]');
const out = path.resolve(root, args[1] || '.cache/reading');
if (out === root) throw new Error('Output must be a separate directory');
const catalog = JSON.parse(await fs.readFile(path.join(root, 'articles.json'), 'utf8'));
const articleOutputs = new Map(catalog.articles.map(a => [path.resolve(root, a.path), `${a.id.toLowerCase()}.html`]));
const katexRoot = path.dirname(require.resolve('katex/package.json'));
const licenses = await Promise.all([
  fs.readFile(path.join(katexRoot, 'LICENSE'), 'utf8'),
  fs.readFile(path.join(path.dirname(require.resolve('markdown-it/package.json')), 'LICENSE'), 'utf8'),
  fs.readFile(path.join(path.dirname(require.resolve('markdown-it-texmath/package.json')), 'license.txt'), 'utf8')
]);
const licenseComment = '<!-- Rendering dependency licenses (KaTeX / markdown-it / markdown-it-texmath):\n' + licenses.join('\n\n').replaceAll('--','- -') + '\n-->';
let mathCss = await fs.readFile(path.join(katexRoot, 'dist/katex.min.css'), 'utf8');
// Embed one modern font format per face; the result needs no CDN or sibling files.
const fontRules = [...mathCss.matchAll(/src:([^;}]+)/g)];
for (const match of fontRules) {
  const font = match[1].match(/url\(([^)]+\.woff2)\)\s*format\([^)]+\)/);
  if (!font) continue;
  const bytes = await fs.readFile(path.join(katexRoot, 'dist', font[1]));
  mathCss = mathCss.replace(match[0], `src:url(data:font/woff2;base64,${bytes.toString('base64')}) format("woff2")`);
}
if (/url\((?!data:)/.test(mathCss)) throw new Error('Unembedded KaTeX font URL remains');
const css = `
:root{color-scheme:light;font-family:"Microsoft YaHei","Noto Sans CJK SC",sans-serif;color:#232b32;background:#faf9f5}
*{box-sizing:border-box}body{margin:0}main{max-width:870px;padding:70px 42px 96px;margin:auto;background:white;min-height:100vh}
article{font-size:17px;line-height:1.95;overflow-wrap:break-word}h1{font-size:32px;line-height:1.45;letter-spacing:-.5px;margin:0 0 32px;font-weight:700}
h2{font-size:23px;line-height:1.5;margin:46px 0 16px}h3{font-size:19px;margin:30px 0 12px}p{margin:0 0 20px}strong{font-weight:650}
img{display:block;max-width:100%;height:auto;margin:28px auto 14px}p:has(>img){padding:8px;border:1px solid #ececec;background:#fff;border-radius:4px}
a{color:#285d87;text-decoration:none}a:hover{text-decoration:underline}pre{overflow:auto;padding:18px 20px;background:#f4f6f8;border:1px solid #e6ebef;border-radius:5px;font-size:13px;line-height:1.7}
code{font-family:Consolas,"Cascadia Code",monospace;font-size:.86em;background:#f2f4f6;padding:2px 4px;border-radius:3px}pre code{background:none;padding:0}
table{width:100%;border-collapse:collapse;font-size:14px;line-height:1.7;margin:24px 0;display:block;overflow:auto}th,td{padding:10px 12px;border:1px solid #dfe5e9;text-align:left;vertical-align:top}th{background:#f3f6f8;white-space:nowrap}
blockquote{border-left:3px solid #9cb3c5;margin:20px 0;padding:6px 18px;color:#526474}.sources{border-top:1px solid #e3e7e9;margin-top:48px;padding-top:20px;font-size:12px;color:#6a7882;line-height:1.8}.sources ul{padding-left:20px}
.katex{font-size:1.08em}.katex-display{overflow-x:auto;overflow-y:hidden;padding:10px 3px;margin:25px 0}eqn{display:block}eq{white-space:normal}
.contents{list-style:none;padding:0}.contents li{padding:16px 0;border-bottom:1px solid #e8ecef}.contents small{display:inline-block;width:48px;color:#748591}
@media(max-width:650px){main{padding:34px 20px 64px}article{font-size:16px}h1{font-size:27px}h2{font-size:21px}table{font-size:13px}}
@media print{body{background:white}main{max-width:none;padding:0}h2,h3{break-after:avoid}img,pre,.katex-display{break-inside:avoid}article{font-size:11pt}h1{font-size:23pt}}
`;
const escape = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const html = (title, body) => `<!doctype html>${licenseComment}<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escape(title)}</title><style>${mathCss}\n${css}</style></head><body><main>${body}</main></body></html>`;
await fs.mkdir(out, { recursive: true });
const manifest = [];
for (const entry of catalog.articles) {
  const source = path.join(root, entry.path);
  let content = await fs.readFile(source, 'utf8');
  const front = content.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n/);
  if (!front) throw new Error(`Missing source metadata: ${entry.path}`);
  const sources = JSON.parse(front[1].match(/^source_ids: (\[.*\])$/m)?.[1] || '[]');
  content = content.slice(front[0].length);
  if (/\\\[|\\\]|\\\(|\\\)/.test(content)) throw new Error(`Use dollar math delimiters: ${entry.path}`);
  const title = content.match(/^# (.+)$/m)?.[1];
  if (!title || sources.length === 0) throw new Error(`Missing title/source_ids: ${entry.path}`);
  const md = new MarkdownIt({ html: false, linkify: false, typographer: false }).use(texmath, {
    engine: katex, delimiters: 'dollars', katexOptions: {throwOnError: true, strict: 'error', trust: false, output: 'htmlAndMathml'}
  });
  const tokens = md.parse(content, {});
  let imageCount = 0;
  for (const token of tokens) for (const child of token.children || []) {
    if (child.type === 'link_open') {
      const href = child.attrGet('href');
      if (href && !/^[a-z]+:/i.test(href) && !href.startsWith('#')) {
        const target = path.resolve(path.dirname(source), href.split('#')[0]);
        if (!target.startsWith(root + path.sep)) throw new Error(`Link escapes repository: ${href}`);
        if (articleOutputs.has(target)) {
          child.attrSet('href', articleOutputs.get(target));
        } else if (['.py', '.json'].includes(path.extname(target))) {
          const bytes = await fs.readFile(target);
          child.attrSet('href', `data:text/plain;charset=utf-8;base64,${bytes.toString('base64')}`);
          child.attrSet('download', path.basename(target));
        }
      }
    }
    if (child.type !== 'image') continue;
    const src = child.attrGet('src');
    if (/^[a-z]+:/i.test(src)) throw new Error(`Use a local image for offline articles: ${src}`);
    const target = path.resolve(path.dirname(source), src);
    if (!target.startsWith(root + path.sep)) throw new Error(`Image escapes repository: ${src}`);
    const bytes = await fs.readFile(target);
    const mime = {'.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.svg':'image/svg+xml'}[path.extname(target)];
    if (!mime) throw new Error(`Unsupported illustration: ${src}`);
    child.attrSet('src', `data:${mime};base64,${bytes.toString('base64')}`);
    child.attrSet('loading', 'eager');
    imageCount++;
  }
  const body = md.renderer.render(tokens, md.options, {});
  if (/katex-error|texmath-error/.test(body)) throw new Error(`Math failed to render: ${entry.path}`);
  const renderedMath = (body.match(/class="katex"/g) || []).length;
  const metadata = `<footer class="sources"><div>source_ids</div><ul>${sources.map(s=>`<li>${escape(s)}</li>`).join('')}</ul></footer>`;
  const filename = `${entry.id.toLowerCase()}.html`;
  await fs.writeFile(path.join(out, filename), html(title, `<article>${body}</article>${metadata}`));
  manifest.push({...entry, title, filename, math_count:renderedMath, image_count:imageCount});
}
const index = `<h1>${escape(catalog.title)}</h1><ul class="contents">${manifest.map(a=>`<li><small>${a.id}</small><a href="${a.filename}">${escape(a.title)}</a></li>`).join('')}</ul>`;
await fs.writeFile(path.join(out, 'index.html'), html(catalog.title, index));
await fs.writeFile(path.join(out, 'build-report.json'), JSON.stringify({articles:manifest, total_math:manifest.reduce((s,a)=>s+a.math_count,0), total_image_uses:manifest.reduce((s,a)=>s+a.image_count,0)},null,2)+'\n');
console.log(`Rendered ${manifest.length} independent offline articles to ${path.relative(root,out)}; ${manifest.reduce((s,a)=>s+a.math_count,0)} formulas, ${manifest.reduce((s,a)=>s+a.image_count,0)} illustrations.`);
