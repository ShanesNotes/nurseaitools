const PAGES=__PAGES__;const SITEMAP=__SITEMAP__;
const J=(o,s=200)=>new Response(JSON.stringify(o),{status:s,headers:{'content-type':'application/json'}});
export default{async fetch(req,env){const u=new URL(req.url);if(u.hostname==='www.nurseaitools.com'){u.hostname='nurseaitools.com';return Response.redirect(u.toString(),301)}let p=u.pathname.replace(/\/+$/,'')||'/';
if(req.method==='POST'&&(p==='/api/subscribe'||p==='/api/submit')){let d;try{d=await req.json()}catch{return J({error:'Bad request'},400)}
if(d.hp)return J({message:'Thanks!'});const ua=(req.headers.get('user-agent')||'').slice(0,200),now=new Date().toISOString();
if(p==='/api/subscribe'){const em=String(d.email||'').trim().toLowerCase();if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em)||em.length>200)return J({error:'Please enter a valid email.'},400);
await env.DB.prepare('INSERT OR IGNORE INTO subscribers(email,created_at,user_agent) VALUES(?,?,?)').bind(em,now,ua).run();return J({message:"You're subscribed. Thanks!"})}
const name=String(d.name||'').trim().slice(0,200),url=String(d.url||'').trim().slice(0,500);if(!name||!/^https?:\/\//.test(url))return J({error:'Tool name and a valid URL are required.'},400);
await env.DB.prepare('INSERT INTO submissions(name,url,category,notes,email,created_at,user_agent) VALUES(?,?,?,?,?,?,?)').bind(name,url,String(d.category||'').slice(0,100),String(d.notes||'').slice(0,3000),String(d.email||'').slice(0,200),now,ua).run();
return J({message:'Thanks! Your submission is in the review queue.'})}
if(p==='/sitemap.xml')return new Response(SITEMAP,{headers:{'content-type':'application/xml'}});
if(p==='/robots.txt')return new Response('User-agent: *\nAllow: /\nSitemap: __BASE__/sitemap.xml\n');
const h=PAGES[p];if(h)return new Response(h,{headers:{'content-type':'text/html;charset=utf-8','cache-control':'public,max-age=300'}});
return new Response(PAGES['/'].replace(/<main>[\s\S]*<\/main>/,'<main><h1>Page not found</h1><p><a href="/">Back to the directory</a></p></main>'),{status:404,headers:{'content-type':'text/html;charset=utf-8'}})}};
