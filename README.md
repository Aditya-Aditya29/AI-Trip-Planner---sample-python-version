AI Trip Planner (Sample) · Streamlit + Google Gemini

This is a minimal Streamlit app that talks to Google’s Gemini models. It’s framed as a sample for an “AI Trip Planner” type project, but right now it’s a generic AI chat interface where you can:
<img width="1918" height="1019" alt="image" src="https://github.com/user-attachments/assets/efb9d090-4939-4f9c-91eb-86596121a952" />

pick a Gemini model from the sidebar

<img width="1919" height="954" alt="image" src="https://github.com/user-attachments/assets/9fc191e8-e702-4ed4-9684-b04ec00ab33a" />

adjust creativity (temperature)

chat with the model

clear the conversation

It’s a good starting point if you plan to add trip-planning logic, itinerary building, or tool calling later.
<img width="1919" height="957" alt="image" src="https://github.com/user-attachments/assets/e05aeafb-7bdf-4fb5-acf1-b3c2de590091" />
Features

✅ Streamlit chat UI (st.chat_message, st.chat_input)

✅ Dynamic Gemini model listing (falls back to safe defaults)

✅ Per-model chat session (switch model, session resets)

✅ Temperature slider in sidebar

✅ “Clear Chat” button

✅ Dark-ish background styling

✅ Reads GOOGLE_API_KEY from .env


Requirements

Python 3.9+ (recommended)

A Google Gemini API key

The following Python packages:

streamlit

python-dotenv

google-generativeai


Getting Started
1. Clone the repo
git clone https://github.com/your-username/ai-trip-planner-sample.git
cd ai-trip-planner-sample

2. Create and activate a virtual environment (optional but smart)
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

3. Install dependencies
pip install streamlit python-dotenv google-generativeai


You can also create a requirements.txt like:

streamlit
python-dotenv
google-generativeai


and then

pip install -r requirements.txt

4. Set up your .env

In the project root, create a file named .env:

GOOGLE_API_KEY=your_real_key_here


If this key is missing, the app shows an error and stops. That’s intentional.

Run the app
streamlit run app.py


(or whatever you name the file; in your snippet it’s just the code in a single file.)

Streamlit will show you a local URL such as:

Local URL: http://localhost:8501


Open that in your browser.

How It Works

Env loading
The app uses python-dotenv to load GOOGLE_API_KEY from .env. If it can’t find it, it stops.

Model discovery
It tries to call genai.list_models() and filters out those that support generateContent. If that fails, it falls back to a static list:

gemini-2.5-flash

gemini-2.5-flash-lite

gemini-2.5-pro

gemini-flash-latest

Per-model chat session
When you pick a model in the sidebar, ensure_chat(...) recreates the chat with that model and resets history for that model.

UI

Sidebar: model select, temperature slider, clear chat

Main: chat history render + st.chat_input

Simple CSS to make the background dark

Chat
User prompt goes to chat.send_message(...) with temperature and max_output_tokens set.

