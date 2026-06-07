# Buzza Frontend & Backend Improvement Plan

## Phase A: Backend Changes

### A.1 Timer Cancellation
**Status: ✅ DONE**

### A.2 Wrong Answer Broadcasting
**Status: ❌ NOT STARTED**

### A.3 Correct Answer Broadcasting
**Status: ❌ NOT STARTED**

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
**Status: ❌ NOT STARTED**

### B.4 Wrong Attempt Notification (Others)
**Status: ❌ NOT STARTED**

### B.5 Correct Answer Notification
**Status: ❌ NOT STARTED**

### B.6 Next Question Countdown
**Status: ❌ NOT STARTED**

### B.7 Timeout Handling
**Status: ❌ NOT STARTED**

---

## Testing Checklist

- [x] Timer counts down from 15 to 0 visually
- [x] Timer bar shrinks smoothly
- [x] True/False questions show buttons, not text input
- [ ] Wrong answer shows "try again" message
- [ ] Input clears after wrong answer so player can retry
- [ ] Other players see "Player X attempted but failed"
- [ ] Correct answer shows winner name and correct answer
- [x] Timer cancels immediately when someone answers correctly
- [ ] Countdown overlay shows 3,2,1 after correct answer
- [ ] All players move to next question at same time
- [ ] Timeout shows correct answer and auto proceeds
- [ ] Score updates correctly for winner only