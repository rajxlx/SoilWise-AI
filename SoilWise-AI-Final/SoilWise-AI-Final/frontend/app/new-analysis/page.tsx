"use client";
import { useState } from "react"; import Link from "next/link"; import { useRouter } from "next/navigation"; import { api, Analysis } from "../../lib/api";
export default function NewAnalysis(){
 const [error,setError]=useState(""); const [busy,setBusy]=useState(false); const router=useRouter();
 async function submit(e:React.FormEvent<HTMLFormElement>){e.preventDefault();setBusy(true);setError("");const form=new FormData(e.currentTarget);try{const result=await api<Analysis>("/analyses",{method:"POST",body:form});router.push(`/analysis/${result.id}`);}catch(err){setError(err instanceof Error?err.message:"Unable to analyze");}finally{setBusy(false);}}
 return <main className="mx-auto max-w-2xl px-5 py-8"><Link href="/dashboard" className="text-leaf">← Dashboard</Link><h1 className="mt-5 text-3xl font-bold">New soil analysis</h1><p className="mt-2 text-gray-600">Enter your laboratory readings. N, P and K are assumed to be mg/kg; organic matter and moisture are percentages.</p><form onSubmit={submit} className="mt-8 space-y-5 rounded-2xl bg-white p-6 shadow-sm">
 <label className="block text-sm font-medium">Field name<input name="field_name" placeholder="e.g. North field" className="mt-1 w-full rounded-xl border p-3"/></label>
 <div className="grid gap-4 sm:grid-cols-2">{[["nitrogen","Nitrogen (N, mg/kg)"],["phosphorus","Phosphorus (P, mg/kg)"],["potassium","Potassium (K, mg/kg)"],["ph","Soil pH"],["organic_matter","Organic matter (%)"],["moisture","Moisture (%)"]].map(([name,label])=><label key={name} className="block text-sm font-medium">{label}<input name={name} type="number" step="any" required min="0" max={name==="ph"?"14":name==="organic_matter"||name==="moisture"?"100":"10000"} className="mt-1 w-full rounded-xl border p-3"/></label>)}</div>
 <label className="block text-sm font-medium">Soil photo (optional)<input name="image" type="file" accept="image/jpeg,image/png,image/webp" capture="environment" className="mt-2 block w-full text-sm"/></label>
 {error&&<p role="alert" className="text-red-700">{error}</p>}<button disabled={busy} className="w-full rounded-xl bg-leaf p-3 font-semibold text-white">{busy?"Analyzing…":"Generate soil report"}</button>
 <p className="text-xs text-gray-500">The score and thresholds are illustrative screening logic, not a laboratory diagnosis. Thresholds require calibration to regional laboratory methods and crop requirements.</p>
 </form></main>
}
