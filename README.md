# 🧠 AI English Grammar Quiz
Developed by **Salveru Keerthana**  


---

## 📘 Project Overview
The **AI English Grammar Quiz** is a Streamlit web app that uses **Google’s Gemini API** to generate grammar questions, evaluate user responses, and provide instant marks and feedback. It dynamically creates:
- 5 Short-answer questions  
- 5 Multiple-choice questions (MCQs)  
- 5 Image-upload descriptive questions  

---

## 🚀 Features
✅ AI-generated grammar quizzes on multiple topics  
✅ Automatic evaluation and scoring using Gemini LLM  
✅ Supports image-based answers  
✅ Works on both desktop and mobile devices  
✅ Accessible through a secure ngrok link even from phones  

---

## 🧰 Technologies Used
| Library | Purpose |
|----------|----------|
| **Streamlit** | User interface for the web app |
| **Google Generative AI (Gemini)** | Generates and evaluates questions |
| **Pyngrok** | Exposes Colab/Localhost to the web |
| **Regex** | Extracts and formats question data |
| **Threading** | Runs Streamlit and ngrok concurrently |

---

## ⚙️ Installation & Setup

### 1️⃣ Upload app.py to Google Colab
```python
from google.colab import files
uploaded = files.upload()
```

### 2️⃣ Install Dependencies
```bash
!pip install streamlit pyngrok google-generativeai -q
!pip install -U google-generativeai
```

### 3️⃣ Authenticate ngrok
Get your token from [https://dashboard.ngrok.com](https://dashboard.ngrok.com)  
```bash
!ngrok config add-authtoken YOUR_TOKEN_HERE
```

### 4️⃣ Run the App
```python
from pyngrok import ngrok
import threading, time, os

def run_streamlit():
    os.system("streamlit run app.py --server.port 8501")

thread = threading.Thread(target=run_streamlit)
thread.start()

time.sleep(8)
public_url = ngrok.connect(8501)
print("🌐 Public URL:", public_url)
```

### 5️⃣ Stop the App
```bash
!pkill streamlit
!pkill ngrok
```

---

## 🌍 How ngrok Makes the App Accessible Anywhere
Ngrok enables your Streamlit app to be accessed from any device — including mobile phones — by creating a **secure HTTPS tunnel** to your Colab runtime.  

It transforms the local address (`localhost:8501`) into a shareable public link (e.g., `https://xyz.ngrok.io`).  
Thus, even users on phones or external networks can open and use your app while your Colab session is active.

---

## 💡 How It Works
1. User selects a grammar topic.  
2. Gemini generates 15 questions (5 text, 5 MCQs, 5 image-based).  
3. User answers and submits.  
4. Gemini evaluates and provides marks out of 15.  
5. The app displays score and personalized feedback.

---

## 🧠 Model Used
**`models/gemini-2.5-flash`**
- Optimized for real-time responses  
- Supports text + image evaluation  
- Ideal for educational and interactive apps  

---

## 🏁 Example Output
```
You scored 13/15.
Strong understanding of grammar. Improve punctuation and descriptive writing.
```

---

## 👩‍💻 Developer
**Salveru Keerthana**  
Project: *AI English Grammar Quiz*  
Powered by **Google Gemini API** and **Streamlit**  

---

## 🖇️ References
- [Google AI Studio](https://aistudio.google.com)  
- [Streamlit Documentation](https://docs.streamlit.io)  
- [Ngrok Documentation](https://ngrok.com/docs)  
