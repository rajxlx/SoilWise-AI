"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { api, Analysis } from "../../lib/api";
export default function Dashboard(){
 const [items,setItems]=useState<Analysis[]>([]); const [error,setError]=useState(""); const [loading,setLoading]=useState(true);
 useEffect(()=>{if(!localStorage.getItem("soilwise_token")){location.href="/login";return;} api<Analysis[]>("/analyses").then(setItems).catch(e=>setError(e.message)).finally(()=>setLoading(false));},[]);
 return <main className="mx-auto max-w-5xl px-5 py-8"><header className="flex flex-wrap items-center justify-between gap-4"><div><Link href="/" className="font-bold text-leaf">🌱 SoilWise</Link><h1 className="mt-3 text-3xl font-bold">Your soil dashboard</h1><p className="text-gray-600">Track field health and recent assessments.</p></div><div className="flex gap-2"><Link href="/new-analysis" className="rounded-xl bg-leaf px-5 py-3 font-semibold text-white">+ New analysis</Link><button onClick={()=>{localStorage.removeItem("soilwise_token");location.href="/";}} className="rounded-xl border px-4">Sign out</button></div></header>
 {error&&<p className="mt-6 rounded-xl bg-red-50 p-4 text-red-700">{error}</p>}
 <section className="mt-8 rounded-2xl bg-white p-5 shadow-sm"><h2 className="font-bold">Recent analyses</h2>{loading?<p className="py-8 text-gray-500">Loading…</p>:items.length===0?<p className="py-8 text-gray-500">No soil records yet. Create your first analysis to get started.</p>:<div className="mt-4 divide-y">{items.map(a=><Link key={a.id} href={`/analysis/${a.id}`} className="flex items-center justify-between gap-4 py-4 hover:bg-gray-50"><div><b>{a.field_name}</b><p className="text-sm text-gray-500">{new Date(a.created_at).toLocaleDateString()} · {a.diagnosis.status}</p></div><span className="rounded-full bg-green-50 px-4 py-2 font-bold text-leaf">{a.health_score}/100</span></Link>)}</div>}</section>
 </main>
}
