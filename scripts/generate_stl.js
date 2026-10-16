// Generate the printable v6 meshes from the authoritative OpenSCAD solid.
// No longer serializes decorative WebGL preview meshes into a false "STL".
const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const root = path.resolve(__dirname, '..');
const source = path.join(root, 'hardware', 'the_scribble_v6_fit.scad');
const options = process.argv.slice(2);
function value(flag) {
  const idx = options.indexOf(flag);
  if (idx < 0) return null;
  if (idx + 1 >= options.length) throw Error('Missing value for ' + flag);
  return options[idx + 1];
}
const part = value('--part') || 'print_layout';
const allowed = new Set(['rear', 'bezel', 'side_caps', 'print_layout']);
if (!allowed.has(part)) throw Error('Unsupported part: ' + part);
const target = path.resolve(value('--output') || path.join(root, 'output', 'the_scribble_v6_' + part + '.stl'));
const windowsOpenSCAD = path.join(process.env.ProgramFiles || 'C:\\Program Files', 'OpenSCAD', 'openscad.exe');
const tool = process.env.OPENSCAD_BIN || (process.platform === 'win32' && fs.existsSync(windowsOpenSCAD) ? windowsOpenSCAD : 'openscad');
fs.mkdirSync(path.dirname(target), { recursive: true });
const run = spawnSync(tool, ['-o', target, '-D', 'part="' + part + '"', source], { encoding: 'utf8' });
if (run.error) {
  throw Error('Cannot start OpenSCAD (' + tool + '): ' + run.error.message + '. Install OpenSCAD or set OPENSCAD_BIN.');
}
if (run.status !== 0 || !fs.existsSync(target) || fs.statSync(target).size === 0) {
  throw Error('OpenSCAD did not create a usable v6 ' + part + ' STL:\\n' + (run.stderr || 'No output'));
}
console.log('Generated v6 ' + part + ': ' + target + ' (' + fs.statSync(target).size + ' bytes)');
