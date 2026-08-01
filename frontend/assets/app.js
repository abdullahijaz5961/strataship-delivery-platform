const API = window.API_BASE || 'http://localhost:8000/api';
const summaryMap = {"stat-0": "services", "stat-1": "deployment_frequency", "stat-2": "verifying", "stat-3": "production_healthy"};
const suffix = {};
const columns = ["Service", "Version", "Environment", "Status"];
const fallbackRows = [["gateway", "v2.8.1", "Production", "Healthy"], ["identity", "v1.14.0", "Production", "Healthy"], ["workflow-api", "v3.2.4", "Staging", "Verifying"]];
function escapeHtml(value){return String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function renderRows(rows){document.getElementById('data-rows').innerHTML=rows.slice(0,6).map(row=>`<div class="data-row">${row.map((v,i)=>`<span class="${i===0?'primary-cell':''}">${escapeHtml(v)}</span>`).join('')}</div>`).join('');}
async function load(){try{const [summaryResponse,listResponse]=await Promise.all([fetch(`${API}/summary`),fetch(`${API}/releases`)]);if(!summaryResponse.ok||!listResponse.ok)throw new Error('API unavailable');const summary=await summaryResponse.json();for(const [id,key] of Object.entries(summaryMap)){if(summary[key]!==undefined)document.getElementById(id).textContent=`${summary[key]}${suffix[id]||''}`;}const list=await listResponse.json();const normalized=list.map(r=>{return [r.service, `v${r.version}`, r.environment, r.status]});renderRows(normalized);document.getElementById('api-status').textContent='Live API connected · data refreshed successfully.';}catch(error){renderRows(fallbackRows);}}
load();
