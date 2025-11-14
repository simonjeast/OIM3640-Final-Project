# proposal.md

## 1) Concept idea

Build a small **local ChatGPT-style web app** that talks to the **OpenAI API** that's Babson College themed (using same branding, colors etc)
**MVP:** one chat thread, non-streaming replies, API key from '.env', simple UI, basic error messages.
**Maybes:** multiple saved chats, prompt presets, local JSON persistence, simple usage/rate-limit display, porting to my own domain.

## 2) Learning Objectives

* call the OpenAI API safely/cheaply; maintain multi-turn chat history; ship a usable local web app
* backend (Flask endpoints, error/backoff), frontend (clean chat UI, markdown), integrations (keys/config, model choices).

## 3) Implementation Plan

* **Backend (Flask):** 'POST /chat' accepts '{messages:[...]}', calls 'openai', returns '{reply: ...}'
* **Frontend (HTML/CSS/JS):** one page with chat pane + input; render basic markdown; keep 'messages' array in the browser.
* **Data:** 'messages = [{"role":"system|user|assistant","content": "..."}]'.

## 4) Project Schedule

* Over the next 4-5 weeks I'll be experimenting with various implementations of the project; creating some "bare bones" designs for the website, asking chatgpt for a lot of help.

## 5) Collaboration Plan

* I will be working on this project solo so the workflow is entirely up to me, which I prefer anyways

## 6) Risks and Limitations

* **Rate limits/latency**
* **Key security**
* **Scope creep**
* **Cost:** will only be using gpt-5-nano or gpt-5 to keep costs down
* **Online dependency:** requires internet/API 

## 7) Additional Course Content
* Flask, OpenAI API, HTML/CSS/JavaScript, other misc packages
