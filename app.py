import streamlit as st
import google.generativeai as genai
import re

# -------------------------------
# CONFIGURATION
# -------------------------------
genai.configure(api_key="AIzaSyC8FOY-Ll1BPUl-4wYeYsxpBttwNwd4f08")
model = genai.GenerativeModel("models/gemini-2.5-flash")

st.set_page_config(page_title="AI English Grammar Quiz", layout="centered")

st.title("🧠 AI English Grammar Quiz")
st.markdown("""
Welcome to your AI-powered English Grammar Quiz!  
Choose a topic and start testing your grammar knowledge.
""")

# -------------------------------
# SELECT TOPIC
# -------------------------------
topics = [
    "Tenses", "Parts of Speech", "Articles", "Prepositions",
    "Active and Passive Voice", "Direct and Indirect Speech",
    "Subject-Verb Agreement", "Punctuation", "Conjunctions", "Random"
]
topic = st.selectbox("📘 Select a grammar topic:", topics)

# -------------------------------
# GENERATE QUESTIONS
# -------------------------------
@st.cache_data(show_spinner=True)
def generate_questions(selected_topic):
    prompt = f"""
    Generate 15 English grammar questions on the topic: {selected_topic}.
    - Questions 1–5: short answer (open-ended).
    - Questions 6–10: multiple choice (include 4 options A, B, C, D clearly listed).
    - Questions 11–15: descriptive/image upload type.
    Format example:
    1. What is a verb?
    6. Which of the following sentences correctly uses subject–verb agreement?
       (A) She go to school every day
       (B) She goes to school every day
       (C) She going to school every day
       (D) She gone to school every day
    11. Write a short paragraph describing your favorite teacher.
    Only output the questions, nothing else.
    """
    response = model.generate_content(prompt)
    text = response.text
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    return lines

if st.button("🎯 Generate Questions"):
    questions = generate_questions(topic)
    st.session_state["questions"] = questions

# -------------------------------
# QUIZ DISPLAY
# -------------------------------
if "questions" in st.session_state:
    questions = st.session_state["questions"]

    text_qs, mcq_qs, img_qs = [], [], []
    current_q = ""

    for line in questions:
        match = re.match(r"^(\d+)\.", line)
        if match:
            if current_q:
                num_match = re.match(r"^(\d+)\.", current_q.strip())
                if num_match:
                    q_num = int(num_match.group(1))
                    if 1 <= q_num <= 5:
                        text_qs.append(current_q.strip())
                    elif 6 <= q_num <= 10:
                        mcq_qs.append(current_q.strip())
                    elif 11 <= q_num <= 15:
                        img_qs.append(current_q.strip())
            current_q = line
        else:
            current_q += " " + line

    if current_q:
        num_match = re.match(r"^(\d+)\.", current_q.strip())
        if num_match:
            q_num = int(num_match.group(1))
            if 1 <= q_num <= 5:
                text_qs.append(current_q.strip())
            elif 6 <= q_num <= 10:
                mcq_qs.append(current_q.strip())
            elif 11 <= q_num <= 15:
                img_qs.append(current_q.strip())

    # -------------------------------
    # SECTION 1: SHORT ANSWER
    # -------------------------------
    st.subheader("1️⃣ Short Answer Questions")
    text_answers = {}
    for q in text_qs:
        text_answers[q] = st.text_input(q, key=q)

    # -------------------------------
    # SECTION 2: MULTIPLE CHOICE
    # -------------------------------
    st.subheader("2️⃣ Multiple Choice Questions")
    mcq_answers = {}
    for q in mcq_qs:
        q_text = re.split(r"\([A-D]\)", q)[0].strip()
        options = re.findall(r"\([A-D]\)\s*([^()]+)", q)
        if options and len(options) == 4:
            opts = [
                f"A) {options[0].strip()}",
                f"B) {options[1].strip()}",
                f"C) {options[2].strip()}",
                f"D) {options[3].strip()}"
            ]
            mcq_answers[q_text] = st.radio(q_text, opts, key=q)
        else:
            mcq_answers[q] = st.text_input(q, key=q)

    # -------------------------------
    # SECTION 3: IMAGE UPLOAD
    # -------------------------------
    st.subheader("3️⃣ Image Upload Questions")
    image_answers = {}
    for q in img_qs:
        uploaded = st.file_uploader(q, type=["jpg", "png", "jpeg"], key=q)
        image_answers[q] = uploaded

    # -------------------------------
    # SUBMIT AND EVALUATE
    # -------------------------------
    if st.button("✅ Submit Quiz"):
        st.success("Your answers have been submitted! Evaluating...")

        # --- Base text prompt
        eval_prompt = f"Evaluate these grammar answers for topic '{topic}'. Give marks out of 15 and short feedback.\n\n"

        for q, ans in text_answers.items():
            eval_prompt += f"Q: {q}\nA: {ans}\n\n"
        for q, ans in mcq_answers.items():
            eval_prompt += f"Q: {q}\nA: {ans}\n\n"
        for q, img in image_answers.items():
            eval_prompt += f"Q: {q}\nA: [Image attached below]\n\n" if img else f"Q: {q}\nA: No Image Uploaded\n\n"

        # --- Create multimodal request
        contents = [{"role": "user", "parts": [{"text": eval_prompt}]}]
        for q, img in image_answers.items():
            if img is not None:
                contents[0]["parts"].append({"text": f"Image answer for: {q}"})
                contents[0]["parts"].append({
                    "inline_data": {
                        "mime_type": img.type,
                        "data": img.getvalue()
                    }
                })

        try:
            evaluation = model.generate_content(contents)
            st.subheader("🧾 Evaluation Feedback")
            st.write(evaluation.text)

            match = re.search(r"(\d{1,2})/15", evaluation.text)
            if match:
                score = int(match.group(1))
                st.progress(score / 15)
                st.success(f"🏅 Total Score: {score}/15")
            else:
                st.info("Score not found in feedback — please read the evaluation above.")

        except Exception as e:
            st.error(f"⚠️ Evaluation failed: {e}")

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.caption("Developed by **Salveru Keerthana** — AI Grammar Assistant powered by Gemini")
