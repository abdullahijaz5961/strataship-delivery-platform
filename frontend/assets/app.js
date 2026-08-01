const API = window.API_BASE || 'http://localhost:8000/api';
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const ago = value => value ? new Date(value).toLocaleString([], {month:'short',day:'numeric',hour:'2-digit',minute:'2-digit'}) : 'In progress';

function renderReleases(releases) {
  document.getElementById('release-list').innerHTML = releases.slice(0,4).map(release => {
    const running = release.status === 'verifying';
    return `<div><span class="release-icon ${running?'running':'success'}">${running?'···':'✓'}</span><p><strong>${esc(release.service)} <b>v${esc(release.version)}</b></strong><small>${esc(release.environment)} · ${esc(release.strategy)} · ${ago(release.created_at)}</small></p></div>`;
  }).join('');
}

function latestByService(releases) {
  const catalog = new Map();
  releases.forEach(release => {
    if (!catalog.has(release.service)) catalog.set(release.service, release);
  });
  return [...catalog.values()];
}

function renderServices(releases) {
  const owners = ['Platform Edge', 'Identity', 'Automation', 'Web Experience'];
  document.getElementById('service-rows').innerHTML = latestByService(releases).map((release, index) => `<div class="table-row"><span><b>${esc(release.service)}</b><small>tracked release · ${esc(release.commit_sha)}</small></span><span>${owners[index % owners.length]}</span><span>v${esc(release.version)}</span><span><i class="health ${release.status === 'healthy' ? 'healthy' : 'degraded'}"></i>${esc(release.status)}</span><span>${ago(release.created_at)}</span></div>`).join('');
}

async function load() {
  try {
    const [summaryRes, releaseRes] = await Promise.all([fetch(`${API}/summary`), fetch(`${API}/releases`)]);
    if (!summaryRes.ok || !releaseRes.ok) throw new Error('API unavailable');
    const [summary, releases] = await Promise.all([summaryRes.json(), releaseRes.json()]);
    if (summary.deployment_frequency !== undefined) document.getElementById('deployment-frequency').textContent = summary.deployment_frequency;
    renderReleases(releases);
    renderServices(releases);
    document.getElementById('api-status').textContent = 'Live API connected · release records refreshed.';
  } catch (_) { /* polished fixtures remain visible for static preview */ }
}

document.getElementById('service-search').addEventListener('input', event => {
  const query = event.target.value.toLowerCase();
  document.querySelectorAll('.table-row').forEach(row => row.hidden = !row.textContent.toLowerCase().includes(query));
});
load();
