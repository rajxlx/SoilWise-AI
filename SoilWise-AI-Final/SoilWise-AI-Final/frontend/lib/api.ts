const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
export function token() { if (typeof window === "undefined") return ""; return localStorage.getItem("soilwise_token") || ""; }
export async function api<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers);
  const t = token(); if (t) headers.set("Authorization", `Bearer ${t}`);
  if (!(init.body instanceof FormData) && init.body) headers.set("Content-Type", "application/json");
  const response = await fetch(`${API}${path}`, { ...init, headers, cache: "no-store" });
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    const detail = body.detail;
    const message = typeof detail === "string" ? detail : Array.isArray(detail)
      ? detail.map((item: { msg?: string }) => item.msg || "Invalid input").join("; ")
      : `Request failed (${response.status})`;
    throw new Error(message);
  }
  return response.json();
}
export type Analysis = {
  id: string; field_name: string; nitrogen: number; phosphorus: number; potassium: number;
  ph: number; organic_matter: number; moisture: number; health_score: number;
  diagnosis: { status: string; issues: { nutrient: string; message: string; level: string }[]; method: string };
  recommendations: { title: string; detail: string }[]; created_at: string;
};
