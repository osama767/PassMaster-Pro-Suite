import itertools

class PasswordGenerator:
    def __init__(self):
        self.generated_list = []

    def generate_network_list(self, net_name, total_length):
        """توليد الكلمات بناءً على القواعد الـ 6 المطلوبة للشبكة"""
        self.generated_list = []
        
        # الحالات الثلاث لاسم الشبكة: osama, Osama, OSAMA
        variations = [
            net_name.lower(),      
            net_name.capitalize(), 
            net_name.upper()       
        ]

        for base in variations:
            # القاعدة 1: اسم الشبكة + أرقام عشوائية + نقطة ( . )
            # الطول المتبقي = الطول الكلي - طول الاسم - 1 (مكان النقطة)
            digits_len_with_dot = int(total_length) - len(base) - 1
            if digits_len_with_dot >= 0:
                combos = [''.join(p) for p in itertools.product('0123456789', repeat=digits_len_with_dot)]
                for d in combos:
                    self.generated_list.append(f"{base}{d}.")

            # القاعدة 2: اسم الشبكة + أرقام عشوائية (بدون نقطة)
            # الطول المتبقي = الطول الكلي - طول الاسم
            digits_len_no_dot = int(total_length) - len(base)
            if digits_len_no_dot >= 0:
                combos = [''.join(p) for p in itertools.product('0123456789', repeat=digits_len_no_dot)]
                for d in combos:
                    self.generated_list.append(f"{base}{d}")
            
        return self.generated_list

    def generate_custom_list(self, user_input, total_length, add_dot=True):
        """توليد الكلمات لتبويب 'شيء آخر' بناءً على مدخلات المستخدم حصراً"""
        self.generated_list = []
        
        # تحويل الطول لرقم صحيح
        total_length = int(total_length)
        
        # إذا كانت المدخلات فارغة، نرجع قائمة فارغة لتجنب الأخطاء
        if not user_input:
            return []

        # توليد التباديل والتوافيق (Combinations with replacement)
        # هذا السطر يولد كل الاحتمالات الممكنة من الحروف والارقام المدخلة فقط
        combos = [''.join(p) for p in itertools.product(user_input, repeat=total_length)]
        
        for c in combos:
            # إضافة الكلمة كما هي (بدون نقطة)
            self.generated_list.append(c)
            
            # إضافة الكلمة مع نقطة في النهاية إذا كان الخيار مفعلاً
            # "مرة بنقطة ومرة بلا نقطة بس كلن يكونو موجودين"
            if add_dot:
                self.generated_list.append(f"{c}.")
                
        return self.generated_list