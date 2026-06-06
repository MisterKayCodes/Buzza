# Buzza Development Plan

## Phase 1: Backend Core (Week 1)
- [✅] **1.1 Database Setup** (`database/db.py`, `database/models.py`)
  - ✅ SQLite connection with SQLAlchemy
  - ✅ Models: Room, Player, GameSession, Question
  - ❌ Alembic migrations setup (Not done)

- [✅] **1.2 Game Manager Core** (`game/manager.py`)
  - ✅ GameManager class with room/player management
  - ✅ WebSocket connection handling
  - ✅ Room code generator (6 chars, alphanumeric)
  - ✅ In-memory state management
  - ✅ Game flow methods (start, next question, scoring, timer)

- [✅] **1.3 Question Service** (`game/questions.py`)
  - ✅ Questions stored in SQLite (130 questions)
  - ✅ Random question fetching (20 per game)
  - ✅ Support for factual, list, truefalse, fillblank types
  - ❌ OpenTDB API integration (Not needed - we pre-fetched once)

- [❌] **1.4 WebSocket Events** (`game/websocket.py`)
  - ❌ Connection lifecycle management (Handled in main.py)
  - ❌ Event handlers for all game events (Partially in manager.py)
  - ❌ Broadcast utilities (In manager.py)

## Phase 2: Backend Game Logic (Week 1-2)
- [✅] **2.1 Room Lifecycle**
  - ✅ Create room
  - ✅ Join room (validate code)
  - ✅ Leave room
  - ✅ Host transfer if host leaves

- [✅] **2.2 Game Flow**
  - ✅ Start game (host only, min 2 players)
  - ✅ Fetch and validate questions
  - ✅ Sequential question delivery
  - ✅ 15-second timer per question
  - ✅ Answer validation (server-side)

- [✅] **2.3 Scoring System**
  - ✅ First correct answer wins point
  - ✅ No penalty for wrong answers
  - ✅ Point awarded immediately via WebSocket
  - ✅ Scoreboard tracking

- [✅] **2.4 Game States**
  - ✅ LOBBY (waiting for players)
  - ✅ PLAYING (game active)
  - ✅ RESULTS (game over)

## Phase 3: Frontend Core (Week 2)
- [❌] **3.1 Project Setup** (`frontend/`)
  - ❌ React + Vite setup
  - ❌ Tailwind CSS for styling
  - ❌ Native WebSocket
  - ❌ React Router for navigation

- [❌] **3.2 WebSocket Hook** (`hooks/useWebSocket.js`)
  - ❌ Connection management
  - ❌ Event listeners
  - ❌ Reconnection logic

- [❌] **3.3 State Management**
  - ❌ Context API or Zustand
  - ❌ Game state store
  - ❌ Player store

## Phase 4: Frontend Pages (Week 3)
- [❌] **4.1 Home Page**
  - ❌ Nickname input
  - ❌ Create room button
  - ❌ Join room input + button

- [❌] **4.2 Lobby Page**
  - ❌ Room code display
  - ❌ Player list with host crown
  - ❌ Start game button (host only)
  - ❌ Leave room button

- [❌] **4.3 Game Page**
  - ❌ Question text
  - ❌ Answer input field
  - ❌ Countdown timer (15s visual)
  - ❌ Live scoreboard sidebar
  - ❌ Question counter

- [❌] **4.4 Results Page**
  - ❌ Final leaderboard
  - ❌ Winner announcement
  - ❌ Play again button

## Phase 5: Polish & Features (Week 4)
- [❌] **5.1 UI/UX Improvements**
  - ❌ Sound effects
  - ❌ Confetti animation
  - ❌ Mobile responsive design
  - ❌ Loading states

- [❌] **5.2 Error Handling**
  - ❌ Disconnection handling
  - ❌ Room full errors
  - ❌ Duplicate nickname handling
  - ❌ Timeout handling

- [❌] **5.3 Nigerian Questions Database**
  - ❌ More Nigerian-specific questions
  - ❌ Categories: History, Culture, Entertainment, Sports, Geography

## Phase 6: Deployment (Week 4)
- [❌] **6.1 Backend Deployment**
  - ❌ Setup on VPS
  - ❌ Systemd service for FastAPI
  - ❌ Nginx reverse proxy
  - ❌ SSL certificate

- [❌] **6.2 Frontend Deployment**
  - ❌ Vercel project setup
  - ❌ Environment variables
  - ❌ Production build

- [❌] **6.3 Testing**
  - ❌ Load testing
  - ❌ Cross-browser testing
  - ❌ Mobile testing

---

## Summary

| Status | Count |
|--------|-------|
| ✅ Complete | 8 |
| ❌ Not Started | Rest |

## Backend Status: ✅ COMPLETE AND TESTED

All backend features are working:
1. Database with 130 questions
2. Room creation and joining
3. Game start with 20 random questions
4. 15-second timer per question
5. Answer validation (supports multiple correct answers for list-style)
6. Scoring (first correct answer wins)
7. Game over with leaderboard

## What needs to be done NEXT:

**Phase 3: Build the Frontend**
- React app setup
- WebSocket connection
- Home, Lobby, Game, and Results pages

The backend is ready to accept frontend connections at `ws://localhost:8000/ws`