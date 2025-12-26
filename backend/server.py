from flask import Flask, request, jsonify, render_template
import os
# تأكد من أن الاستدعاء صحيح حسب بنية مجلداتك
try:
    from .generator import PasswordGenerator
    from .automation import AutomationHandler
except ImportError:
    from generator import PasswordGenerator
    from automation import AutomationHandler

app = Flask(__name__, 
            template_folder='../templates', 
            static_folder='../static')

# إنشاء كائنات من الكلاسات
gen = PasswordGenerator()
auto = AutomationHandler()

# --- مسارات الصفحات (HTML Routes) ---

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/settings')
def settings_page():
    return render_template('settings.html')

@app.route('/terminal')
def terminal_page():
    return render_template('terminal.html')

# --- مسارات البرمجة (API Routes) ---

@app.route('/api/generate', methods=['POST'])
def handle_generation():
    data = request.json
    mode = data.get('mode') 
    name = data.get('name', '')
    length = int(data.get('length', 8))
    chars = data.get('chars', '')
    add_dot = data.get('add_dot', True)

    if mode == 'network':
        results = gen.generate_network_list(name, length)
    else:
        results = gen.generate_custom_list(chars, length, add_dot)
    
    # حفظ النتائج في ملف
    with open("last_generated.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(results))
        
    return jsonify({"status": "Generated", "count": len(results)})

@app.route('/api/start', methods=['POST'])
def handle_start():
    data = request.json
    if not os.path.exists("last_generated.txt"):
        return jsonify({"status": "error", "message": "Generate passwords first!"})
        
    with open("last_generated.txt", "r", encoding="utf-8") as f:
        passwords = f.read().splitlines()
    
    # جلب الإعدادات من الطلب
    initial_delay = int(data.get('initial_delay', 5))
    speed_mode = data.get('speed_mode', '1_per_sec')
    
    auto.start_process(passwords, initial_delay, speed_mode)
    return jsonify({"status": "Started"})

@app.route('/api/stop', methods=['POST'])
def handle_stop():
    auto.stop()
    return jsonify({"status": "Stopped"})

if __name__ == '__main__':
    app.run(debug=True)