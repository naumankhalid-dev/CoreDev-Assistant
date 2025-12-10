<h1 align="center">🌐 CoreDev Assistant (Hybrid)</h1>
<h3 align="center">A Professional Hybrid AI Chatbot using Local FAQs + Grok API Fallback</h3>
<p align="center">
Modern GUI • Developer Assistant • Auto History • Smart FAQ Engine • Grok Fallback
</p>

<hr>

<h2>🚀 Overview</h2>
<p>
<strong>CoreDev Assistant</strong> is a hybrid AI chatbot built in Python that combines:
</p>

<ul>
  <li>⚡ <strong>Local FAQ Engine</strong> for instant offline responses</li>
  <li>🧠 <strong>Grok API fallback</strong> when the FAQ does not cover a question</li>
  <li>🎨 <strong>GPT-style modern GUI</strong> with dark mode</li>
  <li>💬 <strong>Conversation history</strong> (auto saved & loaded)</li>
  <li>🧩 <strong>Smart NLP-based matching</strong> for accurate FAQ selection</li>
</ul>

<p>
Ideal for LinkedIn demo, portfolio projects, full desktop assistant apps, or expanding into your own AI platform.
</p>

<hr>

<h2>🖼️ GUI Preview</h2>

<p align="center">
<img src="https://github.com/naumankhalid-dev/CoreDev-Assistant/blob/main/images/10.12.2025_15.30.17_REC.png?raw=true" 
     alt="Screenshot" width="700" style="border-radius:12px;">
</p>

<hr>

<h2>🧠 How It Works</h2>

<h3>1️⃣ Local FAQ Engine (Primary)</h3>
<p>
The bot first checks your <code>faqs.json</code> file.  
It uses:
</p>
<ul>
  <li>Semantic similarity</li>
  <li>Keyword matching</li>
  <li>Developer FAQ database</li>
</ul>
<p>
If match score ≥ <strong>0.75</strong>, FAQ response is returned instantly.
</p>

<h3>2️⃣ Grok API Fallback (Secondary)</h3>
<p>
If no FAQ matches, the assistant automatically uses the Grok API to generate high-quality answers.
</p>

<hr>

<h2>📁 Project Structure</h2>

<pre>
📦 CoreDev Assistant
│
├── data/
│   └── faqs.json
│
├── src/
│   ├── gui_chatbot_pro.py      # Main GUI
│   ├── main.py                 # Terminal version
│   ├── response.py             # Hybrid logic
│   ├── nlp.py                  # Text similarity
│   ├── utils.py                # Helpers
│   └── chat_history/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
</pre>

<hr>

<h2>⚙️ Features</h2>

<ul>
  <li>🧠 Hybrid intelligence (FAQ → Grok fallback)</li>
  <li>🎨 GPT-style modern GUI</li>
  <li>📜 Conversation history (auto saved)</li>
  <li>🌓 Dark professional theme</li>
  <li>⬆️ Auto-scroll</li>
  <li>💻 Syntax & code block friendly</li>
  <li>🔐 API key protected using <code>.env</code></li>
</ul>

<hr>

<h2>🔧 Installation</h2>

<h3>1️⃣ Clone the Repository</h3>
<pre>
git clone https://github.com/naumankhalid-dev/CoreDev-Assistant/CoreDev-Assistant.git
cd CoreDev-Assistant
</pre>

<h3>2️⃣ Create & Activate Virtual Environment</h3>

<h4>Windows:</h4>
<pre>
python -m venv env
env\Scripts\activate
</pre>

<h3>3️⃣ Install Dependencies</h3>
<pre>
pip install -r requirements.txt
</pre>

<h3>4️⃣ Add Your API Key</h3>
<p>Create a <code>.env</code> file in the root:</p>

<pre>
GROQ_API_KEY=your_api_key_here
</pre>

<h3>5️⃣ Run the GUI</h3>

<pre>
python src/gui_chatbot_pro.py
</pre>

<hr>

<h2>📘 Example Questions to Ask</h2>

<ul>
  <li>What is OOP?</li>
  <li>Explain Python decorators.</li>
  <li>What is Java used for?</li>
  <li>What is an API?</li>
  <li>Explain machine learning.</li>
  <li>How does a constructor work?</li>
  <li>What is abstraction?</li>
  <li>What is a REST API?</li>
</ul>

<hr>

<h2>🔮 Future Enhancements</h2>

<ul>
  <li>Export chats as PDF</li>
  <li>Voice input</li>
  <li>Grok Vision integration</li>
  <li>Code execution sandbox</li>
  <li>Desktop app bundling (EXE)</li>
</ul>

<hr>

<h2>🤝 Contributing</h2>
<p>Pull requests are welcome. Feel free to open issues or propose improvements.</p>

<hr>

<h2>⭐ Support the Project</h2>
<p>If this project helped you, please consider:</p>

<ul>
  <li>⭐ Starring the repository on GitHub</li>
  <li>🔁 Sharing your demo on LinkedIn</li>
  <li>📣 Mentioning CoreDev Assistant in your posts</li>
</ul>

<hr>

<h2>📬 Contact</h2>
<p><strong>Developer:</strong> Nauman Khalid<br>
<strong>Project:</strong> CoreDev Assistant (Hybrid)</p>

<hr>
