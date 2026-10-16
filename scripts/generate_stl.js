const fs = require('fs');
const path = require('path');

const html = fs.readFileSync(path.join(__dirname, '../hardware/case_model_viewer.html'), 'utf8');
const lines = html.split('\n');

// Extract geometry generator (MeshBuilder + buildAllPartMeshes)
const geomCode = lines.slice(215, 710).join('\n');

// Extract exportPrintableSTL
const exportStart = lines.findIndex(l => l.includes('function exportPrintableSTL'));
const exportEnd = lines.findIndex(l => l.includes('function exportParametricSCAD'));
const exportCode = lines.slice(exportStart, exportEnd).join('\n');

const fullRunner = `
${geomCode}
const rawParts = buildAllPartMeshes();
${exportCode}
const stl = exportPrintableSTL();
fs.writeFileSync(path.join(__dirname, '../hardware/the_scribble_v5_step.stl'), stl, 'utf8');
console.log('Successfully generated hardware/the_scribble_v5_step.stl, size:', stl.length, 'bytes');
`;

const fn = new Function('fs', 'path', '__dirname', fullRunner);
fn(fs, path, __dirname);
