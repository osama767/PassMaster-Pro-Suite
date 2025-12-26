const CACHE_NAME = 'passmaster-cache-v1';
const assets = ['/', '/static/css/main.css', '/static/js/main.js'];

self.addEventListener('install', event => {
    event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(assets)));
});

self.addEventListener('fetch', event => {
    event.respondWith(caches.match(event.request).then(response => response || fetch(event.request)));
});