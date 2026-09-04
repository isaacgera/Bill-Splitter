var CACHE_NAME = 'splitzy-v1.3.5';
var ASSETS = [
    './',
    './index.html',
    './manifest.json',
    './icons/icon.svg',
    './icons/icon-maskable.svg',
    './icons/icon-192.png',
    './icons/icon-512.png',
    './icons/icon-maskable-192.png',
    './icons/icon-maskable-512.png',
    './sample-data.json',
    './Splitzy-UserGuide.html'
];

// Install - cache core assets
self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME).then(function(cache) {
            return cache.addAll(ASSETS);
        })
    );
    self.skipWaiting();
});

// Activate - clean old caches
self.addEventListener('activate', function(event) {
    event.waitUntil(
        caches.keys().then(function(keys) {
            return Promise.all(
                keys.filter(function(key) { return key !== CACHE_NAME; })
                    .map(function(key) { return caches.delete(key); })
            );
        })
    );
    self.clients.claim();
});

// Fetch - cache first, network fallback
self.addEventListener('fetch', function(event) {
    event.respondWith(
        caches.match(event.request).then(function(cached) {
            if (cached) return cached;
            return fetch(event.request).then(function(response) {
                if (response.status === 200 && event.request.method === 'GET') {
                    var clone = response.clone();
                    caches.open(CACHE_NAME).then(function(cache) {
                        cache.put(event.request, clone);
                    });
                }
                return response;
            }).catch(function() {
                if (event.request.mode === 'navigate') {
                    return caches.match('./index.html');
                }
            });
        })
    );
});
