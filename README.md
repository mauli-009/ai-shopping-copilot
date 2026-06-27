# AI Shopping Copilot

AI-powered Chrome Extension that helps users make smarter clothing purchase decisions.

## Tech Stack
- Backend: FastAPI, PostgreSQL, Redis
- Extension: Chrome Manifest V3, Vanilla JS
- AI: Groq, LangChain
- Deployment: Render (backend), Vercel (dashboard)

## Setup
Coming soon...


### Basic Architecture

                    USER
                      │
          Opens Amazon/Myntra/Ajio
                      │
                      ▼
      Chrome Extension Detects Product
                      │
                      ▼
      Extract Product Information
                      │
                      ▼
      Send Product Data to Backend
                      │
                      ▼
         Backend Checks Authentication
                      │
              Is User Logged In?
              ┌────────┴─────────┐
             No                 Yes
             │                   │
        Login/Register           │
             │                   ▼
             └──────────► Analyze Product
                              │
                ┌─────────────┼─────────────┐
                ▼             ▼             ▼
          Review Summary  Outfit AI   Style Score
                │             │             │
                └─────────────┼─────────────┘
                              ▼
                     Return AI Response
                              │
                              ▼
                Display Floating AI Panel
                              │
                              ▼
         User Saves / Chats / Tracks / Shares
                              │
                              ▼
                  Store Data in Database