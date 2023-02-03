var CACHE_NAME = 'pwa-cache-v1';
var urlsToCache = [
	'/',
	'/sw.js',
	'/app.js',
	'/manifest.json',
	'/offline',
	'/static/pwa/images/dino.gif',

	'/static/global/css/bootstrap.min.css',
	'/static/global/css/custom-bootstrap.css',
	'/static/global/css/style.css',

	'/static/global/img/brand.png',
	'/static/global/img/cwebbr-nicbr-cgibr.png',
	'/static/global/img/if-sudeste-barbacena.png',

	'/static/global/js/bootstrap.bundle.min.js',
	'/static/global/js/jquery-3.6.1.min.js',
	'/static/global/js/jquery.mask.min.js',
	'/static/global/js/script.js',
];
const self = this;

// Install SW
self.addEventListener('install', (event) =>{
	event.waitUntil(
		caches.open(CACHE_NAME)
		.then((cache) => {
			console.log('Cache Opend.');
			return cache.addAll(urlsToCache);
		})
	)
});

// Listen For requests
self.addEventListener('fetch', (event) =>{
	event.respondWith(
    caches.match(event.request)
		.then(() => {
      return fetch(event.request)
			.catch(async () => {
        const cache = await caches.open(CACHE_NAME);
        const cached = await cache.match(event.request);
        return cached || cache.match('/offline')
      })
		})
	)
});

// Activate
self.addEventListener('activate', (event) =>{
	const cacheWhitelist = [];
	cacheWhitelist.push(CACHE_NAME);
	event.waitUntil(
		caches.keys().then((cacheNames) => Promise.all(
			cacheNames.map((cacheName) => {
				if (!cacheWhitelist.includes(cacheName)) {
					return caches.delete(cacheName);
					}
				})
			))
		)
});