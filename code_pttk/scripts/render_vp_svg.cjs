// Render the project-native SVG assets with the workspace's bundled sharp.
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const moduleRoot = process.env.CODEX_NODE_MODULES || path.join(os.homedir(), '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules');
const sharp = require(require.resolve('sharp', { paths: [moduleRoot] }));
const dir = path.resolve(__dirname, '../diagrams/vp_fix1');
(async () => {
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.svg'));
  for (const file of files) {
    await sharp(path.join(dir, file), { density: 192 }).png().toFile(path.join(dir, file.replace(/\.svg$/, '.png')));
  }
  console.log(`Rendered ${files.length} SVG diagrams and panels.`);
})().catch(e => { console.error(e.message); process.exit(1); });
