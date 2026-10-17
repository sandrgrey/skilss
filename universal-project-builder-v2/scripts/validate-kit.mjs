import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { dirname, resolve, relative } from 'node:path';
import { fileURLToPath } from 'node:url';
const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const required = [
  'README.md', 'AGENTS.md', 'CLAUDE.md', 'PROJECT_BRIEF.md',
  '.ai/core/operating.md', '.ai/core/workflow.md', '.ai/core/quality-gates.md',
  '.ai/modules/cinematic-engine.md', '.ai/modules/video-engine.md',
  '.ai/references/motion-core.mjs', '.ai/references/marlin-timeline.json',
  '.claude/skills/cinematic-scene/SKILL.md', '.agents/skills/cinematic-scene/SKILL.md'
];
let failures = 0;
for (const path of required) {
  if (!existsSync(resolve(root, path))) { console.error('MISSING', path); failures++; }
}
const cli = readFileSync(resolve(root, 'CLAUDE.md'), 'utf8');
for (const match of cli.matchAll(/^@([^\s]+)$/gm)) {
  if (!existsSync(resolve(root, match[1]))) { console.error('BROKEN CLAUDE IMPORT', match[1]); failures++; }
}
const readSkills = (dir) => readdirSync(resolve(root, dir), { withFileTypes: true }).filter(x => x.isDirectory()).map(x => x.name);
const claude = readSkills('.claude/skills');
const codex = readSkills('.agents/skills');
for (const name of [...new Set([...claude, ...codex])]) {
  for (const dir of ['.claude/skills', '.agents/skills']) {
    const path = resolve(root, dir, name, 'SKILL.md');
    if (!existsSync(path)) { console.error('MISSING SKILL', relative(root, path)); failures++; continue; }
    const contents = readFileSync(path, 'utf8');
    if (!contents.startsWith('---\nname:') || !contents.includes('\ndescription:')) { console.error('INVALID SKILL HEADER', path); failures++; }
  }
}
try { JSON.parse(readFileSync(resolve(root, '.ai/references/marlin-timeline.json'), 'utf8')); }
catch (e) { console.error('INVALID JSON', e.message); failures++; }
console.log(`Checked ${required.length} required paths, ${claude.length} Claude skills, ${codex.length} Codex skills. Errors: ${failures}`);
process.exitCode = failures ? 1 : 0;
