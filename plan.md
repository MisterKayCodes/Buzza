# Buzza Frontend & Backend Improvement Plan

## Current Issues

1. Timer not counting down visually
2. True/False questions show text input instead of buttons
3. Wrong answer just fails silently - no "try again" feedback
4. Players not notified when someone else answers (correct or wrong)
5. No countdown before next question
6. Timer doesn't cancel when someone answers correctly

---

## Phase A: Backend Changes

### A.1 Timer Cancellation
- Store timer task as variable when question is sent
- Cancel timer task when someone answers correctly
- Prevents duplicate scoring and timer timeout after winner

**Status: ✅ DONE**

### A.2 Wrong Answer Broadcasting
- Send event to all players when someone answers incorrectly
- Include nickname of player who failed
- Does NOT lock the question - others can still answer

**Status: ❌ NOT STARTED**

### A.3 Correct Answer Broadcasting
- Send event with winner nickname and correct answer
- Cancel the timer immediately
- DO NOT automatically move to next question
- Wait for frontend to request next question after countdown

**Status: ❌ NOT STARTED**

### A.4 Next Question Request
- Add new WebSocket action: `request_next_question`
- Frontend calls this after countdown finishes
- Prevents desync between players

**Status: ❌ NOT STARTED**

### A.5 Prevent Duplicate Next Question
- Add flag to room state: `moving_to_next`
- Prevent multiple next_question calls from racing

**Status: ❌ NOT STARTED**

---

## Phase B: Frontend Game Page Changes

### B.1 Timer Countdown
- Add local timer state (15 seconds)
- useEffect to decrement every second
- Visual timer bar that shrinks over time
- Timer turns red at 5 seconds remaining

**Status: ❌ NOT STARTED**

### B.2 True/False Buttons
- Check question_type === 'truefalse'
- Show two large buttons: ✅ True and ❌ False
- Clicking button submits that answer
- Hide the text input field for these questions

**Status: ❌ NOT STARTED**

### B.3 Wrong Answer Feedback
- Show toast notification: "Wrong answer! Try again."
- Clear input field so player can type again
- Do NOT change screen or lock question
- Player can keep trying until timer ends or someone wins

**Status: ❌ NOT STARTED**

### B.4 Wrong Attempt Notification (Others)
- When another player answers wrong: show toast
- Message: "Player X attempted but failed!"
- Question stays active for everyone else

**Status: ❌ NOT STARTED**

### B.5 Correct Answer Notification
- Show full screen overlay or prominent toast
- Message: "Player X got it right! Answer: [correct answer]"
- Award point shown in scoreboard
- Question locks immediately

**Status: ❌ NOT STARTED**

### B.6 Next Question Countdown
- After correct answer, show countdown overlay
- Countdown: 3... 2... 1...
- After countdown, send `request_next_question` to backend
- All players see same countdown simultaneously

**Status: ❌ NOT STARTED**

### B.7 Timeout Handling
- If timer reaches 0 with no winner
- Show timeout message with correct answer
- Auto proceed to next question after 2 seconds

**Status: ❌ NOT STARTED**

---

## Phase C: WebSocket Events (New/Updated)

### C.1 New Events from Backend

| Event | Payload | When | Status |
|-------|---------|------|--------|
| `answer_wrong_attempt` | `{nickname, message}` | Player answers incorrectly | ❌ |
| `question_correct` | `{winner, correct_answer, points_awarded, new_score}` | Someone answers correctly | ❌ |
| `timeout` | `{correct_answer, message}` | 15 seconds with no winner | ✅ (existing) |

### C.2 New Event from Frontend

| Event | Payload | When | Status |
|-------|---------|------|--------|
| `request_next_question` | `{room_code, nickname}` | After countdown finishes | ❌ |

---

## Phase D: UI Components to Add

### D.1 Toast Notification
- Floating message at bottom center
- Auto disappears after 2 seconds
- Different colors: green (correct), orange (wrong), blue (info)

**Status: ❌ NOT STARTED**

### D.2 Countdown Overlay
- Full screen semi-transparent dark overlay
- Large centered number: 3, 2, 1
- Appears only after correct answer or timeout
- Disappears after countdown finishes

**Status: ❌ NOT STARTED**

### D.3 Timer Progress Bar
- Horizontal bar at top of game screen
- Starts full width, shrinks to zero over 15 seconds
- Changes color: purple → yellow → red

**Status: ❌ NOT STARTED**

---

## Phase E: File Changes Summary

| File | What to change | Status |
|------|----------------|--------|
| `backend/app/game/manager.py` | Add timer cancellation, wrong attempt broadcast, correct answer broadcast, next_question flag | ⚠️ PARTIAL (timer cancellation done) |
| `backend/app/game/models.py` | Add `moving_to_next` flag to RoomState | ❌ |
| `backend/app/main.py` | Add `request_next_question` handler | ❌ |
| `frontend/src/pages/Game.jsx` | Add timer, true/false buttons, toasts, countdown overlay | ❌ |
| `frontend/src/components/Toast.jsx` | New file for toast notifications | ❌ |
| `frontend/src/components/CountdownOverlay.jsx` | New file for countdown overlay | ❌ |
| `frontend/src/App.jsx` | Add new event handlers for new WebSocket events | ❌ |

---

## Testing Checklist

- [ ] Timer counts down from 15 to 0 visually
- [ ] Timer bar shrinks smoothly
- [ ] True/False questions show buttons, not text input
- [ ] Wrong answer shows "try again" message
- [ ] Input clears after wrong answer so player can retry
- [ ] Other players see "Player X attempted but failed"
- [ ] Correct answer shows winner name and correct answer
- [x] Timer cancels immediately when someone answers correctly
- [ ] Countdown overlay shows 3,2,1 after correct answer
- [ ] All players move to next question at same time
- [ ] Timeout shows correct answer and auto proceeds
- [ ] Score updates correctly for winner only

---

## Priority Order

| Priority | Item | Status |
|----------|------|--------|
| 1 | Timer countdown visual | ❌ |
| 2 | True/False buttons | ❌ |
| 3 | Wrong answer feedback ("try again") | ❌ |
| 4 | Wrong attempt notification for others | ❌ |
| 5 | Correct answer broadcast + countdown | ❌ |
| 6 | Timer cancellation | ✅ DONE |
| 7 | Next question sync | ❌ |