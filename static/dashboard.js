"use strict";
const $=id=>document.getElementById(id);
const esc=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const list=data=>data.results||data;
const notice=message=>{$('notice').textContent=message;};
async function api(url, options={}, retry=true){
  const headers={Authorization:'Bearer '+localStorage.getItem('access_token'),...options.headers};
  if(options.body && !(options.body instanceof FormData)){headers['Content-Type']='application/json';options.body=typeof options.body==='string'?options.body:JSON.stringify(options.body);}
  let response=await fetch(url,{...options,headers});
  if(response.status===401 && retry){const refresh=localStorage.getItem('refresh_token');if(refresh){const r=await fetch('/api/auth/token/refresh/',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({refresh})});if(r.ok){const data=await r.json();localStorage.setItem('access_token',data.access);return api(url,options,false);}}location.href='/login/';throw new Error('Please sign in again.');}
  if(response.status===204)return null;
  const data=await response.json();if(!response.ok)throw new Error(Object.entries(data).map(([k,v])=>k+': '+(typeof v==='object'?JSON.stringify(v):v)).join(' '));return data;
}
async function run(task){try{notice('');await task();}catch(error){notice(error.message);}}
function card(title,subtitle,body='',actions=''){return `<article class="card"><h3>${esc(title)}</h3><p class="muted">${esc(subtitle)}</p>${body}<div class="actions">${actions}</div></article>`;}
function empty(target,text){$(target).innerHTML=`<p class="muted">${esc(text)}</p>`;}
let jobs=[],nextPage=null,currentApplication=null,currentRole=null;
async function candidate(){
 const [apps,saved]=await Promise.all([api('/api/applications/my/'),api('/api/jobs/saved/')]);
 $('applications').innerHTML=list(apps).map(a=>card(a.job_title,a.company_name,`<span class="badge">${esc(a.status)}</span><p class="muted">Applied ${new Date(a.applied_at).toLocaleDateString()}</p>`,`<button class="secondary" data-conversation="${a.id}">Messages & interviews</button><a href="/jobs/${a.job}/">View job</a>${['HIRED','REJECTED','WITHDRAWN'].includes(a.status)?'':`<button class="secondary" data-withdraw="${a.id}">Withdraw</button>`}`)).join('');if(!list(apps).length)empty('applications','No applications yet. Find an opportunity below.');
 $('saved').innerHTML=list(saved).map(s=>card(s.job_title,s.company_name,'',`<a href="/jobs/${s.job}/">View job</a><button class="secondary" data-unsave="${s.id}">Remove</button>`)).join('');if(!list(saved).length)empty('saved','Save a job to come back to it later.');
}
async function discover(url='/api/jobs/'){
 const data=await api(url);nextPage=data.next;
 $('discover').innerHTML=list(data).map(j=>card(j.title,j.company_name+' · '+(j.location||j.work_mode),`<span class="badge">${esc(j.job_type.replaceAll('_',' '))}</span>`,`<a href="/jobs/${j.id}/">View & apply →</a><button class="secondary" data-save="${j.id}">Save</button><button class="secondary" data-match="${j.id}">Skill match</button>`)).join('');if(!list(data).length)empty('discover','No matching jobs found. Try another search.');$('moreJobs').classList.toggle('hidden',!nextPage);
}
async function recruiter(){
 const [companies,jobData,appData]=await Promise.all([api('/api/recruiter/companies/'),api('/api/recruiter/jobs/'),api('/api/applications/recruiter/')]);
 $('companySelect').innerHTML=list(companies).map(c=>`<option value="${c.id}">${esc(c.name)}</option>`).join('')||'<option value="">Add a company first</option>';
 jobs=list(jobData);$('recruiterJobs').innerHTML=jobs.map(j=>card(j.title,j.company_name,`<span class="badge">${esc(j.status)}</span><p>${j.applications_count} applications · ${j.views_count} views</p>`,`<button data-edit="${j.id}">Edit</button><button class="secondary" data-close="${j.id}">Close job</button>${j.status==='PUBLISHED'?`<a href="/jobs/${j.id}/">View</a>`:''}`)).join('');if(!jobs.length)empty('recruiterJobs','Your published jobs will appear in the public job search.');
 $('applicants').innerHTML=list(appData).map(a=>card(a.job_title,a.candidate_name+' · '+a.candidate_email,`<span class="badge">${esc(a.status)}</span><p>${esc(a.cover_letter||'No cover letter provided.')}</p>`,`<button class="secondary" data-conversation="${a.id}">Messages & interviews</button>${a.resume?`<button class="secondary" data-resume="${a.resume}">Download resume</button>`:''}${a.status==='WITHDRAWN'?'':`<select aria-label="Application status" id="status-${a.id}">${['REVIEWING','SHORTLISTED','REJECTED','HIRED'].map(s=>`<option ${a.status===s?'selected':''}>${s}</option>`).join('')}</select><button data-status="${a.id}">Update status</button>`}`)).join('');if(!list(appData).length)empty('applicants','Applicants will appear here when candidates apply.');
}
$('logout').onclick=()=>{localStorage.removeItem('access_token');localStorage.removeItem('refresh_token');location.href='/login/';};
$('searchForm').onsubmit=e=>{e.preventDefault();run(()=>discover('/api/jobs/?'+new URLSearchParams(new FormData(e.target))));};
$('moreJobs').onclick=()=>run(()=>discover(nextPage));
$('companyForm').onsubmit=e=>{e.preventDefault();run(async()=>{await api('/api/recruiter/companies/',{method:'POST',body:Object.fromEntries(new FormData(e.target))});e.target.reset();await recruiter();notice('Company added. You can now post a job.');});};
$('jobForm').onsubmit=e=>{e.preventDefault();run(async()=>{const data=Object.fromEntries(new FormData(e.target)),id=data.id;delete data.id;['salary_min','salary_max','application_deadline'].forEach(k=>{if(!data[k])data[k]=null;});await api('/api/recruiter/jobs/'+(id?id+'/':''),{method:id?'PATCH':'POST',body:data});e.target.reset();$('jobForm').elements.id.value='';$('jobFormTitle').textContent='Post a job';await recruiter();notice('Job saved.');});};
$('resetJob').onclick=()=>{$('jobForm').reset();$('jobForm').elements.id.value='';$('jobFormTitle').textContent='Post a job';};
document.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;run(async()=>{
 if(b.dataset.conversation){currentApplication=b.dataset.conversation;await conversation();}
 if(b.dataset.cancelInterview){await api('/api/interviews/'+b.dataset.cancelInterview+'/',{method:'PATCH',body:{status:'CANCELLED'}});await conversation();}
 if(b.dataset.save){await api('/api/jobs/save/',{method:'POST',body:{job:Number(b.dataset.save)}});await candidate();notice('Job saved.');}
 if(b.dataset.unsave){await api('/api/jobs/saved/'+b.dataset.unsave+'/',{method:'DELETE'});await candidate();}
 if(b.dataset.withdraw && confirm('Withdraw this application?')){await api('/api/applications/'+b.dataset.withdraw+'/withdraw/',{method:'PATCH',body:{}});await candidate();}
 if(b.dataset.match){const m=await api('/api/ai-matching/generate/',{method:'POST',body:{job:Number(b.dataset.match)}});notice('Skill match: '+m.match_score+'% — '+m.recommendation+' Missing: '+(m.missing_skills.join(', ')||'none'));}
 if(b.dataset.edit){const job=jobs.find(j=>j.id===Number(b.dataset.edit));Object.entries(job).forEach(([k,v])=>{if($('jobForm').elements[k])$('jobForm').elements[k].value=v??'';});$('jobFormTitle').textContent='Edit job';$('jobForm').scrollIntoView({behavior:'smooth'});}
 if(b.dataset.close){await api('/api/recruiter/jobs/'+b.dataset.close+'/',{method:'PATCH',body:{status:'CLOSED'}});await recruiter();}
 if(b.dataset.status){await api('/api/applications/'+b.dataset.status+'/status/',{method:'PATCH',body:{status:$('status-'+b.dataset.status).value}});await recruiter();notice('Application status updated.');}
 if(b.dataset.resume){const r=await fetch('/api/resumes/'+b.dataset.resume+'/download/',{headers:{Authorization:'Bearer '+localStorage.getItem('access_token')}});if(!r.ok)throw new Error('Could not download resume. Please sign in again.');const url=URL.createObjectURL(await r.blob()),a=document.createElement('a');a.href=url;a.download='resume.pdf';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
 });});
run(async()=>{if(!localStorage.getItem('access_token')){location.href='/login/';return;}const me=await api('/api/auth/me/');currentRole=me.role;await activity();$('greeting').textContent='Welcome back, '+me.username+'.';if(me.role==='RECRUITER'){$('recruiter').classList.remove('hidden');$('profileLink').classList.add('hidden');await recruiter();}else if(me.role==='CANDIDATE'){$('candidate').classList.remove('hidden');await Promise.all([candidate(),discover()]);}else{notice('Use the Django admin at /admin/ to manage this portal.');}});

async function activity(){
 const [stats,events]=await Promise.all([api('/api/analytics/'),api('/api/notifications/')]);
 $('stats').innerHTML=Object.entries(stats).filter(([k,v])=>typeof v==='number').map(([k,v])=>`<div class="panel"><strong>${v}</strong> ${esc(k.replaceAll('_',' '))}</div>`).join('');
 $('activity').innerHTML=events.map(a=>`<p><span class="muted">${esc(new Date(a.at).toLocaleString())}</span> · ${esc(a.text)}</p>`).join('')||'<p class="muted">No activity yet.</p>';
}
async function conversation(){
 const [messages,interviews]=await Promise.all([api('/api/applications/'+currentApplication+'/messages/'),api('/api/applications/'+currentApplication+'/interviews/')]);
 $('conversation').classList.remove('hidden');
 $('messages').innerHTML=list(messages).map(m=>`<div class="card"><strong>${esc(m.sender_name)}</strong><span class="muted"> · ${esc(new Date(m.created_at).toLocaleString())}</span><p>${esc(m.body)}</p></div>`).join('')||'<p class="muted">No messages yet.</p>';
 $('interviewList').innerHTML=list(interviews).map(i=>`<div class="card"><span class="badge">${esc(i.status)}</span><p>${esc(new Date(i.scheduled_at).toLocaleString())} · ${i.duration_minutes} minutes</p><p>${esc(i.location)} ${esc(i.meeting_url)}</p><p>${esc(i.notes)}</p>${currentRole==='RECRUITER'&&i.status==='SCHEDULED'?`<button class="secondary" data-cancel-interview="${i.id}">Cancel interview</button>`:''}</div>`).join('')||'<p class="muted">No interviews scheduled.</p>';
 $('interviewForm').classList.toggle('hidden',currentRole!=='RECRUITER');$('conversation').scrollIntoView({behavior:'smooth'});
}
$('closeConversation').onclick=()=>$('conversation').classList.add('hidden');
$('refreshActivity').onclick=()=>run(activity);
$('messageForm').onsubmit=e=>{e.preventDefault();run(async()=>{await api('/api/applications/'+currentApplication+'/messages/',{method:'POST',body:Object.fromEntries(new FormData(e.target))});e.target.reset();await conversation();});};
$('interviewForm').onsubmit=e=>{e.preventDefault();run(async()=>{const data=Object.fromEntries(new FormData(e.target));data.scheduled_at=new Date(data.scheduled_at).toISOString();await api('/api/applications/'+currentApplication+'/interviews/',{method:'POST',body:data});e.target.reset();await conversation();notice('Interview scheduled. It is visible to the candidate in their dashboard.');});};
