# 📚 AI Study Buddy

A Streamlit chat app with five purpose-built study modes and a fully offline
local AI option, built after a conversation at my internship exit conference
sparked the idea to try building a chatbot myself.

**Live demo:** [ai-study-buddy-0.streamlit.app](https://ai-study-buddy-0.streamlit.app/)

## Background

At my internship exit conference at SERDAC-Luzon, a staff member mentioned their team was looking to build chatbots and asked if I'd be interested in helping out. I'd never built one before, so I decided to try and it turned out to be far more approachable than I expected.

Since chat-based AI is mostly what I already use day to day for studying, I shaped the project into a study companion instead of a generic chatbot. I also wanted it to run fully offline since every AI tool I'd used up to that point required a live connection, and offline capability is a real advantage during slow internet connection or power interruptions. These situations are common enough situations that it felt worth building in properly rather than treating as an edge case.

## What it does

- **Two selectable engines** — Gemini (cloud, `gemini-3.6-flash`) or Ollama
  (fully local and offline, `qwen2.5:3b`) — switch between them anytime
- **Five study modes**, each with its own tailored behavior (see below)
- **Upload your own PDF notes** — parsed with pdfplumber and fed directly into
  the conversation as context
- **LaTeX rendering** for math — equations render properly instead of showing
  raw notation, with automatic cleanup for models that output LaTeX in
  non-standard formats
- **Persistent chat session** with a one-click clear, so mode/engine switches
  don't leave stale context behind

## Study modes

| Mode | What it does |
|---|---|
| **Chat freely** | Open Q&A across any subject, plain-language first with more depth on request |
| **Quiz me** | Generates questions one at a time, scores answers, explains mistakes, tracks a running total |
| **Explain concept** | Breaks any topic into three layers: plain-English intuition, formal definition, real-world example |
| **Practice problems** | Serves problems in increasing difficulty, gives guiding hints instead of answers, only reveals full solutions after a second wrong attempt |
| **Summarize notes** | Turns raw notes into a structured summary: overview, key concepts, formulas, likely exam questions, and common pitfalls |

## Requirements

- Python 3.8+
- A Gemini API key (for the cloud engine) — get one from [Google AI Studio](https://aistudio.google.com)
- [Ollama](https://ollama.com) (for the local/offline engine, optional)

## Installation

```bash
pip install streamlit google-genai pdfplumber ollama
```

For the offline engine:

```bash
ollama pull qwen2.5:3b
```

Set your Gemini API key in `.streamlit/secrets.toml` (gitignored, never commit this file):

```toml
GEMINI_API_KEY = "your-key-here"
```

You can also paste a key directly into the sidebar at runtime instead of
storing one.

## Usage

```bash
streamlit run ai_study_buddy.py
```

## Project structure

```
ai-study-buddy/
├── ai_study_buddy.py   # Main Streamlit app
└── README.md
```

## Tech stack

- [Streamlit](https://streamlit.io) — web app framework
- [Gemini](https://ai.google.dev) (`gemini-3.6-flash`) — cloud AI engine
- [Ollama](https://ollama.com) + Qwen 2.5:3b — fully offline local AI engine
- [pdfplumber](https://github.com/jsvine/pdfplumber) — PDF text extraction
- Regex-based LaTeX normalization for consistent math rendering across engines

## Next Steps

- **Theme configuration** — light/dark and custom accent color options
- **Offline on mobile** — get the local Ollama engine usable from a phone, not just desktop
- **Model options with automatic fallback** — let users pick from multiple models per engine, and auto-switch when the current one hits a quota/rate limit instead of erroring out
- **Image-generating model support** — add an image-gen option for visual aids (diagrams, illustrations) alongside the text modes
- **Conversation export** — download a session (or a specific quiz/practice run) as PDF or Markdown for offline review or re-study later
- **Spaced repetition mode** — a sixth mode that resurfaces previously-missed quiz/practice questions after a delay, instead of only ever moving forward
- **Per-file context toggle** — when multiple PDFs are uploaded, let the user select which ones are active in the current conversation instead of always including all of them

## Author

**Danz Gabriel S. Gabuat**  
BS Mathematics with Specialization in Computer Applications  
Central Luzon State University

