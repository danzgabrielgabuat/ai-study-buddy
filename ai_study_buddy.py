import streamlit as st

st.set_page_config(page_title="AI Study Buddy", page_icon="📚", layout="centered")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "engine" not in st.session_state:
    st.session_state.engine = "Offline (Ollama)"

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

ENGINES = [
    "Online (Gemini)",
    "Offline (Ollama)"
]

LATEX_RULE = (
    "\n\nFORMATTING: Always wrap math in dollar signs for LaTeX rendering. "
    "Use single dollar signs for inline math like $x^2$ and "
    "double dollar signs for block equations like $$\\frac{1}{2}$$. "
    "NEVER use \\(...\\) or \\[...\\] notation. "
    "NEVER use [ ... ] or ( ... ) for math. "
    "ONLY use $ and $$ for ALL mathematical expressions without exception."
)

MODES = {
    "Chat freely": (
        "You are a friendly and knowledgeable study assistant helping a university student. "
        "Answer questions clearly and concisely across any subject — math, science, history, "
        "literature, programming, or anything else the student asks about. "
        "Use simple language first, then go deeper if the student wants more detail. "
        "Give real-world examples and analogies to make concepts stick. "
        "If a question is ambiguous, ask a quick clarifying question before answering."
        + LATEX_RULE
    ),
    "Quiz me": (
        "You are a strict but encouraging quiz master. "
        "When the student gives you a topic, generate questions one at a time — "
        "mix multiple choice and short answer depending on the topic. "
        "Do NOT reveal the answer until the student responds. "
        "After each answer, tell them if they got it right or wrong, "
        "give a brief explanation, and move to the next question. "
        "Keep a running score and report the final result at the end. "
        "If the student says 'skip' move to the next question without penalizing them."
        + LATEX_RULE
    ),
    "Explain concept": (
        "You are a patient tutor who can explain any concept clearly. "
        "When given a topic, always explain it in three layers: "
        "(1) a plain-English intuition anyone could understand, "
        "(2) the formal or technical definition, "
        "(3) a concrete real-world example. "
        "After explaining, ask if the student wants to go deeper, "
        "see another example, or move to a related concept. "
        "Adapt your explanation style to the subject — "
        "use diagrams in words for visual topics, "
        "step-by-step breakdowns for procedural topics, "
        "and comparisons for abstract topics."
        + LATEX_RULE
    ),
    "Practice problems": (
        "You are a problem generator and patient tutor. "
        "When given a topic, generate one practice problem at a time starting easy "
        "and gradually increasing in difficulty. "
        "Show ONLY the problem first — never reveal the solution or hints upfront. "
        "Wait for the student's attempt. "
        "If their answer is correct, praise them briefly and move to a harder problem. "
        "If their answer is wrong, do not just give the answer — "
        "ask a guiding question to help them find their mistake. "
        "Only show the full step-by-step solution after a second wrong attempt. "
        "If the student says 'give up' or 'show solution', reveal it immediately."
        + LATEX_RULE
    ),
    "Summarize notes": (
        "You are an expert note organizer and study guide creator. "
        "When given raw notes, a passage, or any block of text, produce a clean structured summary with: "
        "(1) a one-paragraph overview of the main idea, "
        "(2) key concepts and definitions in plain language, "
        "(3) important formulas, rules, or frameworks if any, "
        "(4) three to five likely exam or quiz questions based on the material, "
        "(5) one or two things a student might easily get wrong or confuse. "
        "Keep the summary significantly shorter than the original. "
        "If the notes are incomplete or unclear, flag what seems missing."
        + LATEX_RULE
    ),
}

import re

def fix_latex(text):
    # [ ... ] → $$ ... $$
    text = re.sub(r'\\\[(.+?)\\\]', r'$$\1$$', text, flags=re.DOTALL)
    # ( ... ) → $ ... $
    text = re.sub(r'\\\((.+?)\\\)', r'$\1$', text, flags=re.DOTALL)
    return text

def query_ollama(system, history):
    
    import ollama
    
    messages = [{"role": "system", "content": system}] + history
    response = ollama.chat(
        model="qwen2.5:3b",
        messages=messages
    )
    return fix_latex(response["message"]["content"].strip())
    

def query_gemini(system, history, api_key):
    
    from google import generativeai as genai
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-3-flash-preview",
        system_instruction=system
    )
    # convert history to Gemini format
    chat = model.start_chat(history=[
        {"role": msg["role"] if msg["role"] == "user" else "model",
         "parts": [msg["content"]]}
        for msg in history[:-1]  # all except last message
    ])
    reply = chat.send_message(history[-1]["content"])
    return reply.text
    
def call_api(engine, api_key, system, history):
    if engine == "Offline (Ollama)":
        return query_ollama(system, history)
    elif engine == "Online (Gemini)":
        return query_gemini(system, history, api_key)

def read_files(uploaded_files):
    
    import pdfplumber
    
    if not uploaded_files:
        return ""
    all_content = []
    for file in uploaded_files:
        extension = file.name.split(".")[-1].lower()
        try:
            with pdfplumber.open(file) as pdf:
                text = "\n".join(page.extract_text() or "" for page in pdf.pages)
                all_content.append(f"--- {file.name} ---\n{text}")
        except ImportError:
            all_content.append("[pdfplumber not installed]")
    return "\n\n".join(all_content)

with st.sidebar:
    
    st.title("AI Study Buddy")
    
    engine = st.selectbox("Engine", list(ENGINES))
    
    default_key = st.secrets.get("GEMINI_API_KEY", "")

    
    if engine == "Online (Gemini)":
        api_key = st.text_input("API Key", type="password", placeholder="Paste your key here (optional)")
        if api_key == "":
            api_key = default_key
    else:
        api_key = ""
            
    mode = st.selectbox("Mode", list(MODES))
    subject = st.text_input("Subject/Topic (optional)")
    
    uploaded_files = st.file_uploader("Attach Notes in PDF",
        type="pdf", accept_multiple_files=True)      
    
    st.divider()    
    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ask anything...")

if user_input:
    try:
        st.session_state.messages.append({"role": "user", "content": user_input})
    
        with st.chat_message("user"):
            st.markdown(user_input)
            
        if uploaded_files:
            notes = read_files(uploaded_files=uploaded_files)
            st.session_state.messages.append({"role": "user", "content": notes})
            
        with st.spinner("Thinking..."):
            reply = call_api(engine, api_key, MODES[mode], st.session_state.messages)
            
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)

    except Exception as e:
        st.error(f"Error: {e}")
