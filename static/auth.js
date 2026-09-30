(() => {
 const nativeFetch=window.fetch.bind(window);let pending=null;
 window.fetch=async function(input,options={}){
  const url=new URL(typeof input==='string'?input:input.url,location.origin);
  const isAPI=url.origin===location.origin && url.pathname.startsWith('/api/') && !url.pathname.startsWith('/api/auth/');
  if(!isAPI)return nativeFetch(input,options);
  const headers=new Headers(options.headers||{}), token=localStorage.getItem('access_token');
  if(token)headers.set('Authorization','Bearer '+token);
  let response=await nativeFetch(input,{...options,headers});
  if(response.status!==401||!localStorage.getItem('refresh_token'))return response;
  if(!pending)pending=nativeFetch('/api/auth/token/refresh/',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({refresh:localStorage.getItem('refresh_token')})}).then(async r=>{if(!r.ok)return null;const d=await r.json();localStorage.setItem('access_token',d.access);return d.access;}).finally(()=>pending=null);
  const fresh=await pending;if(!fresh)return response;headers.set('Authorization','Bearer '+fresh);return nativeFetch(input,{...options,headers});
 };
})();