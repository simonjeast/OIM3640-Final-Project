# OIM3640-Final-Project
# Team Member: Simon East

# BabsonGPT

A local ChatGPT-style web app for Babson College students, built with Python, Flask, and the OpenAI API.

---

# Context
I am taking your Web Tech class next semester, so in anticipation for that I wanted to do something more focused on the front end side of development. I still had some left over OpenAI API credits of my own from my last project, so I thought it could be fun to use those in something front end related. Upon thinking about what I wanted to do, asking ChatGPT for suggestions, and thoughts about some other ideas I had, I thought it could be fun to recreate the ChatGPT website (albeit much simpler) using the Babson branding (I had to find the exact hexadecimal green they use from their official Canva templates) and call it something fun like "**BabsonGPT**". With my knowledge from the course and completing my previous projects, alongside quite a bit of help from ChatGPT learning some HTML/CSS and even a little JavaScript, I managed to get my vision up and running. Thus,

## 1. Big Idea / Project Goal

The goal of this project is to recreate the *experience* of ChatGPT as a **local web app** that runs using Flask, HTML/CSS, Python, and the OpenAI API

**BabsonGPT** has:

* A left sidebar with recent chats
* A main chat panel that looks and feels like ChatGPT
* Babson College branding (core green `#006644`)
* Support for multiple chats that are saved locally in the browser

The main purpose is to:

* Practice working with external APIs (OpenAI)
* Build a small, realistic web application with a client–server architecture
* Explore how to maintain multi-turn conversation history in a simple and safe way

### Example Use Case

A Babson student opens BabsonGPT and:

1. Starts a new chat called "OIM HW 3".
2. Asks: "Explain arrays in simple terms and give me a small example."
3. Gets a step-by-step explanation from BabsonGPT in the main panel.
4. Later clicks back on that chat in the sidebar to revisit the explanation or ask follow-up questions.

All of this runs locally at `http://127.0.0.1:5000`

---

## 2. User Instructions / How to Run

### Prerequisites

* Python 3.9+
* A terminal (Command Prompt, PowerShell, or similar)
* An OpenAI API key with access to the `gpt-5-nano` model

### Clone or Download the Repo

Download from my github (https://github.com/simonjeast/OIM3640-Final-Project/tree/main)

### Open Code

Open the code in VSCode (or another IDE) through github

### Install Dependencies

Make sure all necessary packages are installed (Flask, OpenAI, Python, etc)

### Set Up Your API Key

Create a file named `.env` in the project root:

OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx

### Run the App

You should see output similar to:

 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

Open a browser and go to:

http://127.0.0.1:5000/

You will see the BabsonGPT interface.

### Basic Usage

* Type a message in the input box ("Message BabsonGPT…").
* Press **Send** or hit **Enter** (Shift+Enter for a newline).
* BabsonGPT replies in the main chat window.
* Use **+ New chat** in the sidebar to start a fresh conversation.
* Click on items under **Recent** to switch between saved chats.

Chats are saved **locally** in your browser using `localStorage`. They persist across page reloads on the same browser/computer, rather then uploading to a website. (Maybe I will buy the 'BabsonGPT.com' domain in the future!)

---

## 3. Implementation Details

This section describes the system at an architectural level

### High-Level Architecture

BabsonGPT is a classic small web app:

* **Frontend (browser)**

  * HTML/CSS/JavaScript in `templates/index.html` and `static/style.css`
  * Renders the chat UI and sidebar
  * Manages chat state in JavaScript and `localStorage`
  * Sends requests to the Flask backend for model responses

* **Backend (Flask)**

  * `app.py` uses:

    * `GET /` – serves `index.html`
    * `POST /chat` – receives the conversation, calls OpenAI API, returns the reply
    * `GET /health` – additional simple health check to make sure API is working
  * Loads `OPENAI_API_KEY` from `.env` using `python-dotenv`
  * Uses the OpenAI Python client to call `gpt-5-nano`

**Very rough diagram:**
Courtesy of ChatGPT!
```text
Browser (HTML/CSS/JS)  <--HTTP-->  Flask (app.py)  <--API-->  OpenAI
       |                                 |
  localStorage                    .env / OPENAI_API_KEY
```

### Backend: `app.py`

Key pieces:

* Loads environment variables via `load_dotenv()` and reads `OPENAI_API_KEY`.
* Initializes `OpenAI()` client once at the top.
* `/chat` endpoint:

  * Expects JSON `{ "messages": [...] }`.
  * Calls `client.chat.completions.create(...)` with:

    * `model="gpt-5-nano"`
    * A list of `{"role": ..., "content": ...}` messages (system + user + assistant)
    * A modest `temperature` for slightly creative but not wild responses
  * Returns `{"reply": "...text from model..."}` or `{"error": "..."}`
* Error handling:

  * Catches exceptions and sends back an error JSON

### Frontend: `index.html` and `style.css`

**Layout**

* Left **sidebar** (solid Babson green `#006644`):

  * Logo and "BabsonGPT" title
  * "+ New chat" button
  * "Recent" list, showing saved conversations
  * Account label ("Student · Babson College")

* Main area:

  * Top **green banner** header with the title and subtitle.
  * Large white **chat window** in the center.
  * Bottom input box and "Send" button.

**Chat State and Logic (JavaScript in `<script>` tag)**

* Uses a `SYSTEM_MESSAGE` to make it appear more Babson related:

  ```js
  const SYSTEM_MESSAGE = {
    role: "system",
    content: "You are BabsonGPT, a helpful assistant for a Babson College student.",
  };
  ```

* Maintains an array of **chats**:

  ```js
  chats = [
    {
      id: "timestamp",
      title: "First question about ...",
      messages: [SYSTEM_MESSAGE, {role: "assistant", ...}, {role: "user", ...}, ...],
      createdAt: 1700000000000
    },
    ...
  ];
  ```

* Also tracks `activeChatId` so it knows which chat is open.

* Uses `localStorage`:

  ```js
  localStorage.setItem("babsongpt_chats_v2", JSON.stringify({ chats, activeChatId }));
  ```

* On page load:

  * Tries to load chats from `localStorage`.
  * If found, renders the sidebar list and the active chat.
  * If not found, creates an initial "Welcome chat" with a greeting.

* When the user sends a message:

  * Adds the message to the current chat’s `messages` array.
  * If it’s the first user message, uses it to auto-generate a short chat title.
  * Sends `{ messages }` to `/chat` via `fetch("/chat", {...})`.
  * Displays the assistant’s response and saves back to `localStorage`.

* When the user clicks **+ New chat**:

  * Creates a new chat with a default greeting from BabsonGPT.
  * Sets it as the active chat and updates the sidebar and main view.

* When the user clicks a chat in the **Recent** list:

  * Switches `activeChatId` to that chat.
  * Re-renders the main chat log with its messages.

### Design Decisions

Some explicit choices:

* **Flask vs. other frameworks**
  Chose Flask for simplicity and because it's what I'm used to from class.

* **LocalStorage instead of a database**
  The project is meant to run on a student’s laptop, and this is definitely not production ready. Storing the information locally, however, is a nice touch to my project in my opinion. Storing locally is enough to persist chats between page reloads and doesn’t require any extra infrastructure.

* **gpt-5-nano model**
  This model is inexpensive and good enough for class-level chatbot tasks. It keeps the cost very low even if many prompts are sent during testing.
---

## 4. Results & Capabilities

### What BabsonGPT Can Do

* Hold **multi-turn conversations** with context, similar to ChatGPT.
* Save multiple chats and let you switch between them in the **Recent** sidebar.
* Maintain a visually clean, ChatGPT-like interface using Babson’s green as the primary color.
* Run entirely on **localhost**, with only the model calls going over the network to OpenAI.

### Example Interactions

A few example prompts:

1. **Course help**

   * *User:* "Explain the difference between gross margin and net margin in simple terms."
   * *BabsonGPT:* Provides definitions, formulas, and a small example.

2. **Brainstorming**

   * *User:* "Give me 5 startup ideas related to sustainability on a college campus."
   * *BabsonGPT:* Produces a list of ideas (e.g., reusable container system, energy dashboard, etc.).

3. **Programming help**

   * *User:* "Help me understand what a Flask route is and show a tiny example."
   * *BabsonGPT:* Explains the concept and gives a `@app.route` snippet.

These conversations remain accessible in the sidebar until the user clears browser storage.

### imitations

* BabsonGPT depends on internet access and a valid API key.
* It is unrelated to Babson College, they may be mad at me for using their branding. 
* As with any large language model (it’s just a thin interface on top of the OpenAI model) it can still **hallucinate** or give incorrect answers.

---

## 5. Project Evolution & Narrative

The project evolved in several stages:

1. **Basic Flask + API call**

   * Started with a minimal Flask app returning "Hello, World."
   * Added a `/chat` route that accepted a fixed prompt and returned a model response.

2. **Simple chat page**

   * Created `index.html` with a basic text area and "Send" button.
   * Connected frontend to backend using `fetch` and JSON.
   * Implemented a basic message history array in JavaScript to maintain context.

3. **Styling and Babson branding**

   * Added `style.css` to move toward a ChatGPT-like layout.
   * Introduced a left sidebar and main chat area.
   * Switched the color palette to match Babson’s green (`#006644`) and made the chat window white for readability.

4. **Multiple chats + saving**

   * Initially, only one conversation existed and resetting the app cleared it.
   * Upgraded to a **multi-chat model**:

     * `chats = [...]` array
     * `activeChatId` to track which chat is open
     * Sidebar "Recent" list populated from `chats`
   * Added `localStorage` persistence so chats stay around across page reloads.

5. **Polish and error handling**

   * Introduced a simple loading state (`Send` → `Thinking...`).
   * Displayed error messages inside the chat if an API call failed.
   * Cleaned up titles and made the first user message set the chat name.

Overall, the project moved from "a single API call demo" to a small but realistic product.

---

## 6. Attribution & Resources

This project builds on several tools, docs, and resources:

* **OpenAI Python Client & API Docs**
  For understanding how to call `gpt-5-nano` and structure `messages`.

* **Flask Documentation**
  For setting up routes, templates, and basic server behavior.

* **ChatGPT**
  For extensive help throughout the project, especially in the front-end development of the project, using JavaScript features (`fetch`, event listeners) and `localStorage`, etc.

* **CSS Reference / layout patterns**
  For inspiration on building a two-column layout with a header and content area.

No external icon sets or custom fonts were imported; the app uses system fonts and simple text-based UI.

---

## 7. AI Use

AI was very useful in making this project come to life, so it deserves credit as well.

* I used **ChatGPT** as a coding assistant to:

  * Brainstorm the project requirements for a local ChatGPT clone.
  * Help draft early versions of the Flask app, HTML structure, and CSS styling.
  * How best to implement multi-chat support.

* I **reviewed, edited, and integrated** all AI-generated code:

  * I made sure to frequently ask questions along the way on how certain features were working, and most importantly, working together.
  * I debugged errors (e.g., import issues, missing keys, API errors) on my own.
  * I made decisions about architecture (Flask vs. other frameworks, using `localStorage`, model choice).

* I understand how the AI-assisted code works:

  * I can explain how `/chat` processes requests and calls the OpenAI API.
  * I can explain the structure of `messages`, the role of the system prompt, and how context is built.
  * I learned how to implement local storage in order to store and restore chats
---

## 8. Future Work

Ideas for further improvement:

* **Streaming responses** – Show the model’s answer as it generates text, rather than all at once.
* **Settings panel** – Allow the user to change the model, temperature, and maximum token settings from the UI.
* **Export / import chats** – Let the user download a chat transcript as a `.txt` or `.md` file.
* **Authentication & multi-user mode** – If this were deployed, add user accounts and server-side storage (e.g., a small database) instead of localStorage.
* **Content filters / safety** – Add additional checks to encourage safe and appropriate use.

Overall, BabsonGPT is a compact, local tool that demonstrates how to tie together Python, web development, and the OpenAI API in a way that covers the scope of our course.

