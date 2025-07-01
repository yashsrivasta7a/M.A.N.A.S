# M.A.N.A.S (Mostly Automated, Naturally Awesome Sidekick)

M.A.N.A.S is a context-aware, voice-activated personal assistant for Windows, designed to help with daily tasks, answer questions, execute commands, and provide helpful, clear, and sometimes witty responses. It leverages Azure OpenAI for intelligent conversation and Azure Speech Services for high-quality speech synthesis in Indian voices.

## Features

- **Voice Recognition:** Listens for your commands using your microphone.
- **Natural Language Understanding:** Uses Azure OpenAI to generate intelligent, context-aware responses.
- **Text-to-Speech (TTS):** Replies in a natural Indian voice using Azure Speech Services.
- **Open Folders:** Can open common folders (Downloads, Documents, Project, Pictures) on your system by voice command.
- **Customizable Personality:** Responds as "M.A.N.A.S" (Mostly Automated, Naturally Awesome Sidekick) and adapts tone based on context.
- **Secure Configuration:** All API keys and sensitive data are stored in a `.env` file (not tracked by Git).

## Setup

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd M.A.N.A.S/VoiceAssistant
   ```
2. **Create and activate a virtual environment (optional but recommended):**
   ```sh
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Add your Azure API keys and config to `.env`:**
   (See `.env.example` for required variables)

5. **Run the assistant:**
   ```sh
   python listen.py
   ```

## Example Voice Commands
- "Open downloads"
- "Open project"
- "What is the weather today?"
- "Goodbye" or "Stop" (to exit)
- "Shutdown the computer"
- "Restart the computer"
- "Lock the computer"
- "Open command prompt"
- "Take a screenshot"

## File Structure
- `listen.py` — Main assistant logic (voice recognition, Azure OpenAI, TTS, folder opening)
- `main.py` — Simple TTS demo using pyttsx3
- `.env` — Your API keys (not tracked by git)
- `.gitignore` — Prevents secrets from being committed

## Requirements
- Python 3.8+
- Microphone
- Azure OpenAI and Azure Speech Service credentials

## Security
- **Never share your `.env` file or API keys.**
- The `.env` file is ignored by git for your safety.

## License
MIT

---

> Built for Yash A. by M.A.N.A.S — your Mostly Automated, Naturally Awesome Sidekick!
