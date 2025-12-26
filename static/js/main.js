// وظيفة التوليد
async function generate() {
    const mode = document.getElementById('network-tab').classList.contains('active') ? 'network' : 'other';
    const data = {
        mode: mode,
        name: document.getElementById('net_name')?.value,
        length: document.getElementById('net_length')?.value,
        chars: document.getElementById('custom_chars')?.value,
    };

    const response = await fetch('/api/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });

    const result = await response.json();
    alert("تم التوليد بنجاح! العدد: " + result.count);
}