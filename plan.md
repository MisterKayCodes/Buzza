# Buzza Frontend & Backend Improvement Plan

## Phase A: Backend Changes

### A.1 Timer Cancellation
**Status: ✅ DONE**

### A.2 Wrong Answer Broadcasting
**Status: ✅ DONE**

### A.3 Correct Answer Broadcasting
**Status: ✅ DONE** (already had this)

### A.4 Next Question Request
**Status: ❌ NOT STARTED**

### A.5 Prevent Duplicate Next Question
**Status: ❌ NOT STARTED**

---

## Phase B: Frontend Game Page Changes

### B.1 Timer Countdown
**Status: ✅ DONE**

### B.2 True/False Buttons
**Status: ✅ DONE**

### B.3 Wrong Answer Feedback
**Status: ✅ DONE**

### B.4 Wrong Attempt Notification (Others)
**Status: ✅ DONE**

### B.5 Correct Answer Notification
**Status: ✅ DONE**

### B.6 Next Question Countdown
**Status: ❌ NOT STARTED**

### B.7 Timeout Handling
**Status: ✅ DONE** (already had this)

---

## Testing Checklist

- [x] Timer counts down from 15 to 0 visually
- [x] Timer bar shrinks smoothly
- [x] True/False questions show buttons, not text input
- [x] Wrong answer shows "try again" message
- [x] Input clears after wrong answer so player can retry
- [x] Other players see "Player X attempted but failed"
- [x] Correct answer shows winner name and correct answer
- [x] Timer cancels immediately when someone answers correctly
- [ ] Countdown overlay shows 3,2,1 after correct answer
- [ ] All players move to next question at same time
- [x] Timeout shows correct answer and auto proceeds
- [x] Score updates correctly for winner only

---

## What's Left

### Remaining Features:
1. **B.6 Next Question Countdown** - Show "Next question in 3...2...1..." overlay after correct answer
2. **A.4 Next Question Request** - Frontend requests next question instead of auto moving
3. **A.5 Prevent Duplicate Next Question** - Prevent race conditions

---
