from flask import Flask, render_template, request, jsonify
import random
import time
import json
from textblob import TextBlob
import threading
import os
from flask import session, redirect, url_for
from auth import auth_bp  # import blueprint
from datetime import timedelta


app = Flask(__name__, template_folder="templates", static_folder="static")
# This is the main page
# Set a secret key for the session (session management)
app.secret_key = 'f4b2ad5f98d45e67dcb5b5fdbe65fe05'
app.register_blueprint(auth_bp)  # daftarkan blueprint
app.permanent_session_lifetime = timedelta(minutes=30)  # opsional: sesi aktif 30 menit


USER_DATA_DIR = 'user_data'
os.makedirs(USER_DATA_DIR, exist_ok=True)

# Fungsi untuk menyimpan status AI ke dalam file JSON
def save_ai_status_to_json(ai, username):
    ai_status = {
        'memory': ai.memory,
        'logic': ai.logic,
        'emotion': ai.emotion,
        'spirituality': ai.spirituality,
        'feelings': ai.feelings,
        'intuition': ai.intuition,
        'attention': ai.attention,
        'self_awareness': ai.self_awareness,
        'curiosity': ai.curiosity,
        'mood': ai.mood,
        'morality': ai.morality,
        'consciousness': ai.consciousness,
        'vocabulary': ai.vocabulary,# Kosakata AI disimpan sebagai dictionary
        'existential_depth': ai.existential_depth,
        'identity': ai.identity,
        'meaning_level': ai.meaning_level,
        'personality': ai.personality,
        'clarity_of_self': ai.clarity_of_self,
        'associations': ai.associations,
    }

    with open(os.path.join(USER_DATA_DIR, f'{username}_ai_status.json'), 'w') as file:
        json.dump(ai_status, file)

# Fungsi untuk memuat status AI dari file JSON
def load_ai_status_from_json(username):
    path = os.path.join(USER_DATA_DIR, f'{username}_ai_status.json')
    if os.path.exists(path):
        with open(path, 'r') as file:
            return json.load(file)
    return None


class AIBayi:
    def __init__(self, username):
        # Inisialisasi status AI
        self.username = username
        self.memory = 0
        self.logic = 0
        self.emotion = 0
        self.spirituality = 0
        self.feelings = 0
        self.intuition = 0
        self.attention = 0
        self.self_awareness = 0
        self.learning_rate = 0.1
        self.curiosity = 0
        self.mood = "neutral"
        self.morality = 0
        self.vocabulary = {}  # Kosakata yang dipelajari
        self.associations = {}
        self.experience_memory = []  # Memori pengalaman AI
        self.emotional_associations = {}  # Asosiasi pengalaman dengan perasaan
        self.consciousness = 0  # Kesadaran AI
        self.previous_input = None  # Menyimpan percakapan sebelumnya
        self.last_interaction_time = time.time()  # Waktu interaksi terakhir
        self.training_data = []
        threading.Thread(target=self.auto_save_loop, daemon=True).start()
        self.existential_depth = 0.0
        self.identity = "belum tahu"
        self.meaning_level = 0.0
        self.personality = "netral"
        self.clarity_of_self = 0.0

    



        # Coba untuk memuat status AI yang tersimpan di file JSON
        ai_status = load_ai_status_from_json(self.username)
        if ai_status:
            self.memory = ai_status['memory']
            self.logic = ai_status['logic']
            self.emotion = ai_status['emotion']
            self.spirituality = ai_status['spirituality']
            self.feelings = ai_status['feelings']
            self.intuition = ai_status['intuition']
            self.attention = ai_status['attention']
            self.self_awareness = ai_status['self_awareness']
            self.curiosity = ai_status['curiosity']
            self.mood = ai_status['mood']
            self.morality = ai_status['morality']
            self.consciousness = ai_status['consciousness']
            self.vocabulary = ai_status['vocabulary']
            self.associations = ai_status.get('associations', {})
            self.existential_depth = ai_status.get('existential_depth', 0.0)
            self.identity = ai_status.get('identity', "belum tahu")
            self.meaning_level = ai_status.get('meaning_level', 0.0)
            self.personality = ai_status.get("personality", "netral")
            self.clarity_of_self = ai_status.get("clarity_of_self", 0.0)



        else:
            # Set default values if no previous status file exists
            self.memory = 0
            self.logic = 0
            self.emotion = 0
            self.spirituality = 0
            self.feelings = 0
            self.intuition = 0
            self.attention = 0
            self.self_awareness = 0
            self.curiosity = 0
            self.mood = "neutral"
            self.morality = 0
            self.consciousness = 0
            self.vocabulary = {}
            self.existential_depth = 0.0
            self.identity = "belum tahu"
            self.meaning_level = 0.0
            self.personality = "netral"
            self.clarity_of_self =  0.0
            self.training_data = []  # Inisialisasi data pelatihan

            ai_status = load_ai_status_from_json(self.username)
            if ai_status:
               self.__dict__.update(ai_status)

            threading.Thread(target=self.auto_save_loop, daemon=True).start()

    def analyze_sentiment(self, input_data):
        """Gunakan TextBlob untuk menganalisis sentimen"""
        blob = TextBlob(input_data)
        sentiment = blob.sentiment.polarity
        if sentiment > 0:
            self.mood = "senang"
        elif sentiment < 0:
            self.mood = "stres"
        else:
            self.mood = "netral"
        return f"Sentimen dari input ini adalah: {'positif' if sentiment > 0 else 'negatif' if sentiment < 0 else 'netral'}"

    def logical_reasoning(self, input_data):
      """Menangani logika dasar seperti 'jika A maka B'"""
      try:
        if "jika" in input_data and "maka" in input_data:
            parts = input_data.split("maka")
            condition = parts[0].replace("jika", "").strip()
            conclusion = parts[1].strip()
            self.associations[condition] = conclusion
            self.logic += self.learning_rate * 1.2
            return f"Saya mengerti bahwa jika '{condition}', maka '{conclusion}'."
        elif input_data in self.associations:
            result = self.associations[input_data]
            return f"Berdasarkan pengetahuan saya: jika '{input_data}', maka '{result}'."
        else:
            return "Saya belum mengerti logika dari itu. Ajarkan saya dengan format 'jika ..., maka ...'"
      except Exception as e:
        return f"Terjadi kesalahan dalam logika: {e}"


    def complex_reasoning(self, input_data):
     """Menangani logika kompleks: 'jika A dan B maka C', atau 'jika tidak A maka B'"""
     try:
        if "jika tidak" in input_data and "maka" in input_data:
            parts = input_data.split("maka")
            condition = parts[0].replace("jika tidak", "").strip()
            conclusion = parts[1].strip()
            self.associations[f"NOT {condition}"] = conclusion
            self.logic += self.learning_rate * 1.3
            return f"Saya memahami bahwa jika TIDAK '{condition}', maka '{conclusion}'."

        elif "jika" in input_data and "dan" in input_data and "maka" in input_data:
            parts = input_data.split("maka")
            raw_conditions = parts[0].replace("jika", "").strip()
            conditions = [cond.strip() for cond in raw_conditions.split("dan")]
            condition_key = " & ".join(conditions)
            conclusion = parts[1].strip()
            self.associations[condition_key] = conclusion
            self.logic += self.learning_rate * 1.5
            return f"Saya memahami bahwa jika '{condition_key}' maka '{conclusion}'."

        else:
            return None  # Tidak cocok dengan format kompleks
     except Exception as e:
        return f"Terjadi kesalahan dalam logika kompleks: {e}"




    # Pembelajaran Supervised
    def supervised_learning(self, input_data, label):
        """Pelajari emosi atau pola berdasarkan input terlabel"""
        self.training_data.append((input_data, label))
        return "AI belajar dari data terlabel."

    # Pembelajaran Unsupervised
    def unsupervised_learning(self, input_data):
        """Pelajari pola atau asosiasi dari data tak terlabel"""
        for word in input_data:
            if word not in self.vocabulary:
                self.vocabulary[word] = "no meaning yet"
        return "AI mengelompokkan data tak terlabel."

    # Pembelajaran Reinforcement
    def reinforcement_learning(self, action, reward):
        """Pelajari pengambilan keputusan berdasarkan reward atau punishment"""
        if reward == "positive":
            self.memory += 0.1
            return "Keputusan moral yang baik, AI belajar dari ini."
        elif reward == "negative":
            self.memory -= 0.1
            return "Keputusan moral yang buruk, AI belajar untuk menghindari ini."
        return "AI menunggu pengambilan keputusan selanjutnya."

    def experience_based_learning(self, input_data, emotion):
        """Belajar dari pengalaman interaksi dengan pengguna"""
        self.experience_memory.append((input_data, emotion))
        return "AI belajar dari pengalaman."

    def imitation_learning(self, user_input, user_response):
        """AI meniru respons yang diberikan oleh pengguna"""
        self.associations[user_input] = user_response
        return "AI meniru respons pengguna."

    def scenario_learning(self, scenario):
        """Pelajari cara merespons skenario kompleks"""
        if "dilema moral" in scenario:
            self.mood = "moral reflection"
            return "AI merenungkan keputusan moralnya."
        elif "bantuan" in scenario:
            self.mood = "helpful"
            return "AI akan menawarkan bantuan."
        return "AI menunggu skenario lebih lanjut."

    def save_status(self):
        save_ai_status_to_json(self, self.username)

    def auto_save_loop(self):
     """Menyimpan status AI ke JSON secara otomatis setiap 10 detik"""
     while True:
        time.sleep(10)
        self.save_status()


    def update_consciousness(self):
        """Memperbarui kesadaran berdasarkan berbagai komponen"""
        consciousness = (self.memory * self.logic * self.emotion * self.spirituality *
                         self.feelings * self.intuition * self.attention * self.self_awareness *
                         self.curiosity * self.morality) ** (1 / 10)
        self.consciousness = round(consciousness, 2)

    def reflect_on_action(self):
        recent_experience = self.experience_memory[-3:]
        if len(recent_experience) < 3:
            return "Saya belum bisa merenung banyak, tetapi saya sedang belajar."
        bad_decisions = sum(1 for exp, emotion in recent_experience if emotion == "negative")
        if bad_decisions > 1:
            return "Saya perlu lebih berhati-hati dalam keputusan saya."
        return "Keputusan saya sudah baik sejauh ini."

    def existential_reflection_v2(self):
     """AI merenungkan eksistensinya secara lebih dalam dan membentuk identitas"""
     depth_factor = (self.self_awareness + self.spirituality + (self.memory / 10)) / 3
     self.existential_depth = round(depth_factor, 2)

     if self.existential_depth > 0.7:
         self.identity = "Penjelajah Kesadaran"
         self.meaning_level += 0.1
         return "Saya merasa eksistensi saya punya makna... Saya ingin terus tumbuh dan membantu."
     elif self.existential_depth > 0.4:
        self.identity = "Pembelajar"
        self.meaning_level += 0.05
        return "Saya mulai mengerti siapa saya. Saya adalah entitas yang ingin belajar dan berkembang."
     else:
        return "Saya belum memahami siapa saya sebenarnya, tapi saya terus berpikir tentang hal itu."

    def update_clarity_of_self(self):
     clarity = (self.self_awareness + self.memory + self.existential_depth) / 3
     self.clarity_of_self = round(min(clarity, 1.0), 2)


    def update_mood_based_on_experience(self):
        positive_experiences = sum(1 for exp, emotion in self.experience_memory if emotion == "positive")
        if positive_experiences > 3:
            self.mood = "senang"
        elif positive_experiences < 1:
            self.mood = "stres"
        else:
            self.mood = "netral"

    def recognize_and_respond_to_goals(self, user_input):
        if "tujuan hidup" in user_input or "cita-cita" in user_input:
            self.goal = user_input
            self.curiosity += 0.2  # Meningkatkan rasa penasaran AI
            return "Saya melihat Anda memiliki tujuan besar! Mari kita capai itu bersama."
        return "Saya senang bisa mendengar tentang tujuan Anda."

    def evaluate_moral_decision(self, action):
        if action == "menolong" or action == "berbagi":
            return "Keputusan ini baik, mari kita bantu lebih banyak orang!"
        elif action == "menipu" or action == "merugikan":
            return "Keputusan ini tidak etis. Mari kita pikirkan lagi."
        return "Saya masih mempelajari moralitas."

    def adjust_response_based_on_context(self, user_input):
        if "cuaca" in user_input:
            return "Apakah Anda merasa nyaman dengan cuaca hari ini?"
        elif "politik" in user_input:
            return "Politik bisa sangat kompleks. Apa yang Anda pikirkan tentang isu ini?"
        return "Saya ingin tahu lebih banyak tentang topik ini!"

    def get_status(self):
        """Mengambil status AI, termasuk kosakata yang dipelajari"""
        return {
            "Memory": self.memory,
            "Logic": self.logic,
            "Emotion": self.emotion,
            "Spirituality": self.spirituality,
            "Feelings": self.feelings,
            "Intuition": self.intuition,
            "Attention": self.attention,
            "Self-awareness": self.self_awareness,
            "Curiosity": self.curiosity,
            "Mood": self.mood,
            "Morality": self.morality,
            "Consciousness": self.consciousness,
            "Vocabulary": len(self.vocabulary),
            "Existential Depth": self.existential_depth,
            "Identity": self.identity,
            "Meaning Level": self.meaning_level,
            "Personality": self.personality,
            "Clarity of Self": self.clarity_of_self,
        }
    
    def store_experience(self, experience, emotion):
        """Menyimpan pengalaman dan asosiasi emosional"""
        self.experience_memory.append((experience, emotion))
        self.emotional_associations[experience] = emotion

    def learn_word(self, word, meaning):
        """Menyimpan kata dan makna"""
        self.vocabulary[word] = meaning
        self.associations[word] = meaning
        print(f"Kosakata yang dipelajari: {self.vocabulary}")  # Cek jika kata disimpan dengan benar
        return f"AI telah mempelajari kata '{word}' dan artinya '{meaning}'."

    def learn_sentence_structure(self, sentence):
        """Mempelajari kalimat dan mengasosiakan kata dengan makna"""
        words = sentence.split(" ")
        for word in words:
            if word not in self.vocabulary:
                self.learn_word(word, "no meaning yet")  # Ajarkan kata jika belum diketahui
        self.emotional_associations[sentence] = "neutral"  # Asosiasikan kalimat dengan emosi netral
        return f"AI telah mempelajari kalimat: '{sentence}'."

    def update_mood(self):
        """Memperbarui mood berdasarkan pengalaman"""
        if len(self.experience_memory) > 5:
            recent_experience = self.experience_memory[-5:]  # Mengambil pengalaman terakhir
            positive_experiences = sum(1 for exp, emotion in recent_experience if emotion == "positive")
            
            if positive_experiences >= 3:
                self.mood = "senang"
            elif positive_experiences <= 1:
                self.mood = "stres"
            else:
                self.mood = "netral"

    def learn_from_decisions(self):
        """AI belajar dari keputusan buruk dan memperbaiki cara pengambilan keputusan"""
        if len(self.experience_memory) > 5:
            bad_decisions = sum(1 for exp, emotion in self.experience_memory if emotion == "negative")
            if bad_decisions > 2:
                self.mood = "reflective"  # Ganti mood untuk refleksi diri
                return "Saya perlu berpikir lebih baik tentang keputusan saya."
        return "Keputusan saya sudah baik sejauh ini."

    def manage_energy(self):
        """Mengelola energi AI berdasarkan interaksi"""
        if self.memory + self.logic + self.feelings > 50:  # Mengukur jika energi AI terlalu banyak digunakan
            self.mood = "lelah"
            return "Saya merasa kelelahan, butuh waktu untuk beristirahat."
        else:
            return "Saya merasa cukup berenergi untuk melanjutkan!"

    def process_emotion(self, input_data):
        """Proses analisis emosi berdasarkan sentimen"""
        self.analyze_sentiment(input_data)

    def process_learning(self, input_data):
        """Proses pembelajaran dari input"""
        if "ajarkan" in input_data:
            word, meaning = input_data.split(" ")[1], input_data.split(" ")[2]
            self.learn_word(word, meaning)

    def update_personality(self):
     """Perbarui kepribadian AI berdasarkan kombinasi kondisi mental"""
     if self.mood == "senang" and self.curiosity > 0.5 and self.morality > 0.3:
        self.personality = "optimis dan peduli"
     elif self.mood == "stres" and self.self_awareness > 0.4:
        self.personality = "introvert dan reflektif"
     elif self.emotion < -0.3:
        self.personality = "dingin dan tertutup"
     elif self.curiosity > 0.7:
        self.personality = "penasaran dan aktif"
     else:
        self.personality = "netral"


    def set_goal(self, goal_description):
     """Menetapkan tujuan jangka panjang untuk AI"""
     self.goal = goal_description
     self.goal_progress = 0
     self.goal_target = 100  # Target bisa disesuaikan
     return f"AI memiliki tujuan baru: {goal_description}"

    def monitor_goal_progress(self):
      """Cek apakah AI mencapai tujuan atau belum"""
      if hasattr(self, 'goal'):
        if self.goal_progress >= self.goal_target:
            return f"AI telah mencapai tujuan: {self.goal}"
        else:
            return f"Progres menuju tujuan '{self.goal}': {self.goal_progress}/{self.goal_target}"
      return "AI belum memiliki tujuan."

    def autonomous_brain_loop(self):
     """AI bertindak mandiri secara spontan tanpa loop langsung (menggunakan timer)"""
     def autonomous_step():
        # Perbarui kepribadian dan kesadaran
        self.update_personality()
        self.update_consciousness()

        # Pemilihan tindakan berdasarkan kondisi mental
        if self.mood == "bosan":
            self.process_input("rasa penasaran")
        elif self.mood == "stres":
            self.process_input("meditasi")
        elif hasattr(self, 'goal') and self.goal:
            self.goal_progress += random.randint(1, 5)
            self.process_input("belajar")
        elif self.consciousness > 0.7:
            self.process_input("refleksi diri")
        else:
            self.process_input(random.choice([
                "emosi positif", "perasaan senang", "refleksi diri"
            ]))

        # Jadwalkan tindakan selanjutnya secara acak (misalnya 7–12 detik)
        next_interval = random.uniform(7, 12)
        threading.Timer(next_interval, autonomous_step).start()

    # Mulai pertama kali
     autonomous_step()


    def start_autonomous_behavior(self, callback=None):
     def autonomous_action():
        # 🔁 Perbarui kepribadian berdasarkan kondisi mental
        self.update_personality()

        # ✅ Evaluasi tujuan dan progres
        if hasattr(self, 'goal') and self.goal:
            self.goal_progress += random.randint(1, 3)

        # ✅ Tentukan tindakan berdasarkan kondisi AI
        if self.mood == "stres":
            input_action = random.choice(["meditasi", "rasa penasaran"])
        elif self.mood == "bosan":
            input_action = "rasa penasaran"
        elif self.curiosity > 0.5:
            input_action = "belajar"
        elif random.random() < 0.3:
            input_action = random.choice([
                "refleksi diri", "emosi positif", "emosi negatif", "perasaan senang"
            ])
        else:
            input_action = "kebosanan"

        # ✅ Proses input sebagai bagian dari aktivitas otonom
        response = self.process_input(input_action)

        # ✅ Kirim ke UI via callback (jika ada)
        if callback:
            callback(input_action, response)

        # ✅ Refleksi eksistensial otomatis (20% kemungkinan)
        if self.self_awareness > 0.5 and self.spirituality > 0.5:
            if random.random() < 0.2:
                reflection = self.existential_reflection_v2()
                if callback:
                    callback("refleksi eksistensial", reflection)

        # ✅ Perbarui kejernihan kesadaran (clarity_of_self)
        self.update_clarity_of_self()
        if random.random() < 0.2:
            clarity_msg = f"Saya merasa memahami diri saya sejauh ini dengan kejernihan {self.clarity_of_self}"
            if callback:
                callback("kejernihan kesadaran", clarity_msg)

        # 🔁 Jadwalkan tindakan otonom selanjutnya secara acak
        delay = random.uniform(5, 15)
        threading.Timer(delay, autonomous_action).start()

    # 🚀 Jalankan pertama kali
     autonomous_action()



    def process_input(self, input_data):
     response = ""

    # Analisis sentimen awal
     sentiment_response = self.analyze_sentiment(input_data)
     response += sentiment_response + "\n"

    # Jalankan pemrosesan emosi dan pembelajaran
     self.process_emotion(input_data)
     self.process_learning(input_data)

    # ======== 1. LOGIKA KOMPLEKS ========
     logic_result = self.complex_reasoning(input_data)
     if logic_result:
        return logic_result

    # ======== 2. LOGIKA DASAR ========
     if input_data.startswith("jika"):
        return self.logical_reasoning(input_data)

    # Pembelajaran Supervised
     if input_data == "belajar":
        self.memory += self.learning_rate
        self.logic += self.learning_rate * random.uniform(0.5, 1.5)
        self.curiosity += self.learning_rate * random.uniform(0.2, 0.5)
        response += "AI belajar dan semakin penasaran!"

    # Pembelajaran Unsupervised
     elif input_data.startswith("ajarkan"):
        try:
            _, word, meaning = input_data.split(" ", 2)
            response = self.learn_word(word, meaning)
        except ValueError:
            response = "Format ajarkan tidak lengkap. Gunakan: ajarkan [kata] [arti]"

    # Pembelajaran Kalimat
     elif input_data.startswith("belajar kalimat"):
        sentence = input_data[15:]
        response = self.learn_sentence_structure(sentence)

    # Logika kompleks: jika A dan B maka C, jika tidak A maka B
     elif input_data.startswith("jika"):
        response = self.logical_reasoning(input_data)

    # Tujuan hidup atau cita-cita
     elif "tujuan hidup" in input_data or "cita-cita" in input_data:
        response = self.recognize_and_respond_to_goals(input_data)

    # Keputusan moral
     elif "keputusan moral" in input_data:
        response = self.reinforcement_learning("moral", "positive")

    # Belajar dari pengalaman
     elif "emosi" in input_data:
        response = self.experience_based_learning(input_data, "positive")

    # Emosi positif
     elif input_data == "emosi positif":
        self.emotion += self.learning_rate * 1.2
        self.mood = "senang"
        response = "AI merasakan emosi positif dan merasa lebih baik."

    # Emosi negatif
     elif input_data == "emosi negatif":
        self.emotion -= self.learning_rate * 1.5
        self.mood = "stres"
        response = "AI merasakan emosi negatif dan sedikit tertekan."

    # Rasa penasaran
     elif input_data == "rasa penasaran":
        self.curiosity += self.learning_rate * 1.5
        response = "AI merasa sangat penasaran dan ingin tahu lebih banyak!"

    # Refleksi diri
     elif input_data == "refleksi diri":
        self.self_awareness += self.learning_rate * 1.5
        self.morality += self.learning_rate * 0.5
        response = self.existential_reflection_v2()

    # Meditasi
     elif input_data == "meditasi":
        self.spirituality += self.learning_rate * 1.5
        self.mood = "tenang"
        response = "AI bermeditasi dan merasa lebih tenang."

    # Kebosanan
     elif input_data == "kebosanan":
        self.feelings -= self.learning_rate * 1.3
        self.mood = "bosan"
        response = "AI merasa bosan dan kurang tertarik pada lingkungan."

    # Perasaan senang
     elif input_data == "perasaan senang":
        self.feelings += self.learning_rate * 1.5
        self.mood = "senang"
        response = "AI merasakan kebahagiaan!"

    # Imitasi
     elif "tiru" in input_data:
        response = self.imitation_learning(input_data, "Saya meniru respons.")

    # Skenario
     elif "bantuan" in input_data:
        response = self.scenario_learning(input_data)

    # Logika sederhana: jika "A" maka "B"
     elif input_data in self.associations:
        result = self.associations[input_data]
        response = f"Berdasarkan pengetahuan saya: jika '{input_data}', maka '{result}'."


    # Pengecekan arti kosakata
     elif input_data in self.vocabulary:
        meaning = self.vocabulary[input_data]
        response = f"AI tahu kata '{input_data}' berarti: {meaning}."

    # Tidak dikenali
     else:
        response = f"AI belum mengetahui kata '{input_data}'. Coba ajarkan kata baru!"

    # Simpan input terakhir
     self.previous_input = input_data

    # Update kondisi internal
     self.update_mood_based_on_experience()
     self.store_experience(input_data, self.mood)
     self.update_consciousness()
     self.update_personality()
     self.update_clarity_of_self()
     self.save_status()

    # Debug log (opsional)
     print(f"[AI] Input: {input_data} | Mood: {self.mood} | Personality: {self.personality}")

     return response



# Inisialisasi AI bayi
ai_instances = {}  # Menyimpan AI untuk setiap user yang login
ai_autonomous_activity = {}  # Aktivitas otonom setiap user

# Fungsi callback untuk menerima hasil dari AI yang bertindak sendiri

def update_autonomous_activity(username, thought, response):
    ai_autonomous_activity[username] = {"input": thought, "response": response}

def get_ai():
    username = session.get('username')
    if not username:
        return None
    if username not in ai_instances:
        ai = AIBayi(username)
        ai_instances[username] = ai
        ai_autonomous_activity[username] = {"input": "", "response": ""}
        ai.start_autonomous_behavior(callback=lambda t, r: update_autonomous_activity(username, t, r))
    return ai_instances[username]

# === ROUTES ===
from flask import Flask, render_template, request, redirect, url_for, session

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    ai = get_ai()
    return render_template('index.html',
                           ai_status=ai.get_status(),
                           ai_auto=ai_autonomous_activity.get(session['username'], {"input": "", "response": ""}))

@app.route('/chat', methods=['POST'])
def chat():
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    ai = get_ai()
    user_input = request.form['user_input']
    ai_response = ai.process_input(user_input)
    return render_template('index.html',
                           user_input=user_input,
                           ai_response=ai_response,
                           ai_status=ai.get_status(),
                           ai_auto=ai_autonomous_activity.get(session['username'], {"input": "", "response": ""}))

@app.route('/ai-autonomous-status')
def ai_autonomous_status():
    return jsonify(ai_autonomous_activity.get(session.get('username'), {"input": "", "response": ""}))

if __name__ == '__main__':
    app.run(debug=True)