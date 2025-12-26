let deferredPrompt;
window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    console.log("التطبيق جاهز للتثبيت!");
});

// يمكن استدعاء deferredPrompt.prompt() عند ضغط زر معين لتثبيت التطبيق