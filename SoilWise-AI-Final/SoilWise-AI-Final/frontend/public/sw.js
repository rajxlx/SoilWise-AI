const CACHE = "soilwise-shell-v2";
const SHELL = ["/", "/manifest.json", "/icon.svg"];

self.addEventListener("install", event => {
  event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(SHELL)));
  self.skipWaiting();
});

self.addEventListener("activate", event => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter(key => key.startsWith("soilwise-shell-") && key !== CACHE).map(key => caches.delete(key)));
    await self.clients.claim();
  })());
});

self.addEventListener("fetch", event => {
  const request = event.request;
  const url = new URL(request.url);
  if (request.method !== "GET" || url.origin !== self.location.origin) return;
  // Never cache navigations, authenticated pages, API calls, or user-specific responses.
  if (request.mode === "navigate" || url.pathname.startsWith("/api/")) return;
  const isImmutableAsset = url.pathname.startsWith("/_next/static/") ||
    url.pathname === "/manifest.json" || url.pathname === "/icon.svg";
  if (!isImmutableAsset) return;
  event.respondWith((async () => {
    const cache = await caches.open(CACHE);
    const cached = await cache.match(request);
    if (cached) return cached;
    const response = await fetch(request);
    if (response.ok) await cache.put(request, response.clone());
    return response;
  })());
});
