/**
 * وظيفة بدء التخمين من الصفحة الرئيسية
 */
function startGuessing() {
    // الانتقال لصفحة التيرمينال حيث يبدأ العداد
    window.location.href = '/terminal';
}

/**
 * منطق صفحة التيرمينال (العداد التنازلي والتشغيل)
 */
if (window.location.pathname === '/terminal') {
    // 1. جلب وقت التجهيز من الإعدادات أو استخدام 5 ثوانٍ كافتراضي
    let delaySetting = parseInt(localStorage.getItem('initial_delay')) || 5;
    let timeLeft = delaySetting;
    
    const overlay = document.getElementById('countdown-overlay');
    const counterDisplay = document.getElementById('counter-number'); // تأكد أن ID مطابق لـ terminal.html

    // 2. تحديث الرقم في الواجهة قبل البدء
    if (counterDisplay) counterDisplay.innerText = timeLeft;

    // 3. بدء العداد التنازلي
    const timer = setInterval(() => {
        timeLeft--;
        if (counterDisplay) counterDisplay.innerText = timeLeft;

        if (timeLeft <= 0) {
            clearInterval(timer);
            // إخفاء طبقة العداد
            if (overlay) overlay.classList.add('hidden');
            // تشغيل الأتمتة الحقيقية في الباك آند
            triggerStart();
        }
    }, 1000);
}

/**
 * وظيفة إرسال أمر البدء للسيرفر (الباك آند)
 */
async function triggerStart() {
    // جلب السرعة المختارة من الإعدادات
    const speed = localStorage.getItem('speed_mode') || '1_per_sec';

    // إظهار رسالة في لوج التيرمينال (إذا كانت الدالة addLog موجودة)
    if (typeof addLog === "function") {
        addLog("تم انتهاء الوقت.. بدء الكتابة الآن!", "sys");
    }

    try {
        // إرسال الإعدادات للباك آند ليبدأ PyAutoGUI بالعمل
        await fetch('/api/start', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                initial_delay: 0, // نرسل 0 لأننا انتظرنا بالفعل في الفرونت آند
                speed_mode: speed 
            })
        });
    } catch (error) {
        console.error("خطأ في تشغيل الأتمتة:", error);
        if (typeof addLog === "function") addLog("فشل الاتصال بالسيرفر!", "error");
    }
}

/**
 * وظيفة إيقاف العملية فوراً
 */
async function stopProcess() {
    try {
        await fetch('/api/stop', { method: 'POST' });
        alert("🚨 تم إرسال أمر إيقاف الطوارئ!");
        window.location.href = '/';
    } catch (error) {
        window.location.href = '/';
    }
}