"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
export function AuthForm({ mode }: { mode: "login" | "register" }) {
  const [error,setError]=useState(""); const [busy,setBusy]=useState(false); const router=useRouter();
  async function submit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault(); setError(""); setBusy(true);
    const data = new FormData(e.currentTarget);
    try {
      if(mode==="register") {
        const r=await fetch(`${API}/auth/register`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({email:data.get("email"),password:data.get("password"),full_name:data.get("full_name"),preferred_language:data.get("language")})});
        if(!r.ok) throw new Error((await r.json()).detail || "Registration failed");
      }
      const body=new URLSearchParams({username:String(data.get("email")),password:String(data.get("password"))});
      const response=await fetch(`${API}/auth/login`,{method:"POST",headers:{"Content-Type":"application/x-www-form-urlencoded"},body});
      if(!response.ok) throw new Error((await response.json()).detail || "Login failed");
      const result=await response.json(); localStorage.setItem("soilwise_token",result.access_token); router.push("/dashboard");
    } catch(err) { setError(err instanceof Error?err.message:"Something went wrong"); } finally {setBusy(false);}
  }
  return <form onSubmit={submit} className="space-y-4">
    {mode==="register" && <label className="block text-sm font-medium">Full name<input name="full_name" required className="mt-1 w-full rounded-xl border p-3"/></label>}
    <label className="block text-sm font-medium">Email<input name="email" type="email" required className="mt-1 w-full rounded-xl border p-3"/></label>
    <label className="block text-sm font-medium">Password<input name="password" type="password" minLength={8} required className="mt-1 w-full rounded-xl border p-3"/></label>
    {mode==="register" && <label className="block text-sm font-medium">Language<select name="language" className="mt-1 w-full rounded-xl border p-3"><option value="en">English</option><option value="hi">हिन्दी</option><option value="kn">ಕನ್ನಡ</option></select></label>}
    {error && <p role="alert" className="text-sm text-red-700">{error}</p>}
    <button disabled={busy} className="w-full rounded-xl bg-leaf p-3 font-semibold text-white disabled:opacity-60">{busy?"Please wait…":mode==="login"?"Sign in":"Create account"}</button>
  </form>;
}
