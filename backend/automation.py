import pyautogui
import time
import threading
import keyboard

class AutomationHandler:
    def __init__(self):
        self.is_running = False
        self.thread = None
        # إلغاء أي تأخير بين ضغطات المفاتيح في pyautogui
        pyautogui.PAUSE = 0

    def start_process(self, password_list, initial_delay, speed_mode):
        self.is_running = True
        self.thread = threading.Thread(target=self._run_loop, args=(password_list, initial_delay, speed_mode))
        self.thread.start()

    def _get_delay(self, mode):
        """تحويل خيارات السرعة إلى ثواني (حسب طلبك بدقة)"""
        speeds = {
            "1_per_min": 60,
            "1_per_30s": 30,
            "1_per_10s": 10,
            "1_per_sec": 1,
            "10_per_sec": 0.1,
            "100_per_sec": 0.01,
            "1000_per_sec": 0.0001  # سرعة جنونية
        }
        return speeds.get(mode, 1)

    def _run_loop(self, passwords, delay, speed_mode):
        # وقت الانتظار اللي بيحدده المستخدم من الإعدادات
        time.sleep(delay)
        
        wait_time = self._get_delay(speed_mode)

        for pwd in passwords:
            # التحقق من زر ESC أو الضغط على إيقاف من الموقع
            if not self.is_running or keyboard.is_pressed('esc'):
                break
            
            # --- السرعة الذكية ---
            if wait_time < 0.01:
                # للسرعات العالية جداً نستخدم مكتبة keyboard لأنها أسرع من pyautogui
                keyboard.write(pwd)
                keyboard.press('enter')
            else:
                # للسرعات العادية نستخدم pyautogui
                pyautogui.write(pwd)
                pyautogui.press('enter')
            
            # الانتظار حسب السرعة المطلوبة
            if wait_time > 0:
                time.sleep(wait_time)
        
        self.is_running = False

    def stop(self):
        self.is_running = False