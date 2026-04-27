/* eslint-disable no-restricted-globals */
if (typeof window === "undefined") {
  self.addEventListener("install", () => self.skipWaiting());

  self.addEventListener("activate", (event) => {
    event.waitUntil(self.clients.claim());
  });

  self.addEventListener("fetch", (event) => {
    const request = event.request;

    if (request.cache === "only-if-cached" && request.mode !== "same-origin") {
      return;
    }

    event.respondWith(
      fetch(request)
        .then((response) => {
          if (response.status === 0) {
            return response;
          }

          const headers = new Headers(response.headers);
          headers.set("Cross-Origin-Embedder-Policy", "require-corp");
          headers.set("Cross-Origin-Opener-Policy", "same-origin");

          return new Response(response.body, {
            status: response.status,
            statusText: response.statusText,
            headers,
          });
        })
        .catch((error) => {
          console.error("coi-serviceworker fetch failed:", error);
          throw error;
        })
    );
  });
} else {
  (function () {
    if (!window.isSecureContext) return;
    if (!("serviceWorker" in navigator)) return;

    if (window.crossOriginIsolated) return;

    const RELOAD_GUARD_KEY = "pp-coi-sw-reloaded";

    function reloadOnceForCOI() {
      try {
        if (sessionStorage.getItem(RELOAD_GUARD_KEY) === "1") return;
        sessionStorage.setItem(RELOAD_GUARD_KEY, "1");
      } catch (_) {
        // If sessionStorage is unavailable, still avoid hard failure.
      }
      window.location.reload();
    }

    if (navigator.serviceWorker.controller) {
      // Service worker is already controlling this page; no need to force reload.
      return;
    }

    navigator.serviceWorker
      .register(window.document.currentScript.src, { scope: "./" })
      .then((registration) => {
        // If a controller appears, this indicates SW takeover and a single reload
        // can apply COOP/COEP headers to the controlled document.
        navigator.serviceWorker.addEventListener(
          "controllerchange",
          () => {
            if (!window.crossOriginIsolated) reloadOnceForCOI();
          },
          { once: true }
        );

        // If the active worker is already present but this page is not yet
        // controlled, do a guarded reload once to attach controller on next load.
        if (registration.active && !navigator.serviceWorker.controller && !window.crossOriginIsolated) {
          reloadOnceForCOI();
        }
      })
      .catch((error) => {
        console.error("coi-serviceworker registration failed:", error);
      });
  })();
}
