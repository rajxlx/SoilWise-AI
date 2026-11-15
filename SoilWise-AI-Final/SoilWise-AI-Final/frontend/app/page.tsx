import Link from "next/link";
export default function Home() {
  return <main className="min-h-screen">
    <header className="mx-auto flex max-w-6xl items-center justify-between px-6 py-6"><b className="text-2xl text-leaf">🌱 SoilWise</b><Link className="rounded-xl bg-leaf px-5 py-3 font-semibold text-white" href="/login">Sign in</Link></header>
    <section className="mx-auto grid max-w-6xl gap-10 px-6 py-16 md:grid-cols-2 md:items-center">
      <div><p className="mb-3 font-bold uppercase tracking-widest text-leaf">Smarter soil decisions</p><h1 className="text-5xl font-bold leading-tight">Know your soil. Grow with confidence.</h1><p className="mt-6 text-lg text-gray-600">Record soil test values, understand nutrient alerts and explore practical crop guidance — designed for a farmer's phone.</p><div className="mt-8 flex gap-3"><Link href="/register" className="rounded-xl bg-leaf px-6 py-3 font-semibold text-white">Get started</Link><Link href="/login" className="rounded-xl border border-gray-300 px-6 py-3 font-semibold">Sign in</Link></div></div>
      <div className="rounded-3xl bg-[#e5efdf] p-8 shadow-sm"><div className="rounded-2xl bg-white p-6"><p className="text-sm text-gray-500">Example soil report</p><div className="mt-2 text-5xl font-bold text-leaf">82<span className="text-xl">/100</span></div><p className="mt-1 font-semibold">Good starting point</p><div className="mt-6 grid grid-cols-3 gap-3">{[["N","Good"],["P","Check"],["K","Good"]].map(x=><div key={x[0]} className="rounded-xl bg-gray-50 p-3"><b>{x[0]}</b><p className="text-sm text-gray-500">{x[1]}</p></div>)}</div><p className="mt-5 text-xs text-gray-500">Illustrative preview — actual assessment uses submitted values.</p></div></div>
    </section>
  </main>;
}
