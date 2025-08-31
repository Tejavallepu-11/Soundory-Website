const CACHE_NAME = "soundory-cache-v1";
const OFFLINE_URL = "/offline/";

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll([OFFLINE_URL]);
    })
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(
          keys.map((k) => (k !== CACHE_NAME ? caches.delete(k) : null))
        )
      )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  if (event.request.mode === "navigate") {
    // For page navigation
    event.respondWith(
      fetch(event.request).catch(() =>
        caches.open(CACHE_NAME).then((cache) => cache.match(OFFLINE_URL))
      )
    );
  } else if (event.request.url.includes("/static/")) {
    // Cache-first for static files
    event.respondWith(
      caches.match(event.request).then((res) => {
        return (
          res ||
          fetch(event.request).then((response) => {
            return caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, response.clone());
              return response;
            });
          })
        );
      })
    );
  }
});
