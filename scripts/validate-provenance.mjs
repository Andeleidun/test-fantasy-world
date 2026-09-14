import { access, readFile } from 'node:fs/promises';

const manifest = JSON.parse(await readFile('content/provenance.json', 'utf8'));
const publicCatalog = JSON.parse(await readFile('content/public/catalog.json', 'utf8'));

const assert = (condition, message) => {
  if (!condition) throw new Error(message);
};

const unique = (items, label) => {
  assert(items.length === new Set(items).size, `Duplicate ${label}`);
};

assert(manifest.schemaVersion === 1, 'Unsupported provenance schema');
assert(manifest.level === 3, 'The project provenance level must be 3');
assert(manifest.status === 'authorial', 'The provenance manifest must remain authorial');

const authorityIds = manifest.authorityDocuments.map(item => item.id);
const registerIds = manifest.registers.map(item => item.id);
const coverageIds = manifest.coverage.map(item => item.id);
unique(authorityIds, 'authority id');
unique(registerIds, 'register id');
unique(coverageIds, 'coverage id');

for (const authority of manifest.authorityDocuments) {
  assert(authority.title && authority.locator, `Incomplete authority ${authority.id}`);
  assert(/^https:\/\/(docs|drive)\.google\.com\//.test(authority.locator), `Non-Drive authority locator: ${authority.id}`);
  assert(!/[?#]/.test(authority.locator), `Authority locator must be canonical: ${authority.id}`);
}

for (const register of manifest.registers) {
  if (register.authorityRef) assert(authorityIds.includes(register.authorityRef), `Unknown register authority: ${register.authorityRef}`);
  for (const locator of [register.locator, ...(register.additionalLocators || [])].filter(Boolean)) await access(locator);
}

const relationshipTypes = new Set(manifest.relationshipTypes);
const sourceGroupIds = manifest.otherworldSourceGroups.map(item => item.id);
unique(sourceGroupIds, 'Otherworld source group');
assert(sourceGroupIds.join(',') === 'OW-A,OW-B,OW-C,OW-D,OW-E,OW-F,OW-G,OW-H,OW-I,OW-J,OW-K,OW-L,OW-M,OW-N,OW-O', 'Otherworld groups OW-A through OW-O must be indexed in order');
for (const group of manifest.otherworldSourceGroups) {
  assert(['materially-used', 'candidate'].includes(group.status), `Invalid source status: ${group.id}`);
  assert(group.relationship.length > 0, `Missing relationship: ${group.id}`);
  for (const relationship of group.relationship) assert(relationshipTypes.has(relationship), `Unknown relationship ${relationship} in ${group.id}`);
  if (group.status === 'candidate') assert(group.relationship.every(item => item === 'candidate'), `Candidate ${group.id} cannot be recorded as adopted`);
}

const published = new Set(publicCatalog.map(page => page.file));
const mapped = new Set();
for (const domain of manifest.coverage) {
  assert(domain.status === 'complete', `Incomplete Level 3 domain: ${domain.id}`);
  assert(domain.boundary, `Missing evidence boundary: ${domain.id}`);
  for (const ref of domain.authorityRefs) assert(authorityIds.includes(ref), `Unknown authority ${ref} in ${domain.id}`);
  for (const ref of domain.registerRefs) assert(registerIds.includes(ref), `Unknown register ${ref} in ${domain.id}`);
  for (const path of domain.repositoryRefs) await access(path);
  for (const file of domain.publicFiles) {
    assert(published.has(file), `Unknown public file ${file} in ${domain.id}`);
    mapped.add(file);
  }
}

const missing = [...published].filter(file => !mapped.has(file));
assert(missing.length === 0, `Public files without Level 3 coverage: ${missing.join(', ')}`);
console.log(`Validated Level 3 provenance: ${manifest.coverage.length} domains, ${manifest.authorityDocuments.length} authorities, ${manifest.otherworldSourceGroups.length} Otherworld source groups and ${mapped.size} public files.`);
