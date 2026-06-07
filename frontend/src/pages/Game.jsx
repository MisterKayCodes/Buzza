import { useState, useEffect } from 'react'

function Game({ currentQuestion, scores, nickname, onSubmitAnswer, wrongMessage, wrongAttemptMessage, correctMessage, showCountdown, onCountdownComplete }) {
  const [answer, setAnswer] = useState('')
  const [timeLeft, setTimeLeft] = useState(15)
  const [showWrongMessage, setShowWrongMessage] = useState('')
  const [showAttemptMessage, setShowAttemptMessage] = useState('')
  const [showCorrectMessage, setShowCorrectMessage] = useState('')
  const [nextCountdown, setNextCountdown] = useState(5)
  const [questionLocked, setQuestionLocked] = useState(false)
  const [winnerInfo, setWinnerInfo] = useState(null)

  // Reset timer and messages when new question arrives
  useEffect(() => {
    if (currentQuestion) {
      setTimeLeft(currentQuestion.timer_seconds || 15)
      setAnswer('')
      setShowWrongMessage('')
      setShowAttemptMessage('')
      setShowCorrectMessage('')
      setQuestionLocked(false)
      setWinnerInfo(null)
      setNextCountdown(5)
    }
  }, [currentQuestion])

  // Handle countdown (bottom countdown, not full screen)
  useEffect(() => {
    if (showCountdown) {
      setNextCountdown(5)
      const interval = setInterval(() => {
        setNextCountdown(prev => {
          if (prev <= 1) {
            clearInterval(interval)
            onCountdownComplete()
            return 0
          }
          return prev - 1
        })
      }, 1000)
      return () => clearInterval(interval)
    }
  }, [showCountdown, onCountdownComplete])

  // Handle correct message from props - also lock question and show banner
  useEffect(() => {
    if (correctMessage) {
      setShowCorrectMessage(correctMessage)
      setQuestionLocked(true)
      const match = correctMessage.match(/(.+) got it right! Answer: (.+)/)
      if (match) {
        setWinnerInfo({
          nickname: match[1],
          answer: match[2]
        })
      }
      setTimeout(() => setShowCorrectMessage(''), 3000)
    }
  }, [correctMessage])

  // Handle wrong message from props
  useEffect(() => {
    if (wrongMessage) {
      setShowWrongMessage(wrongMessage)
      setTimeout(() => setShowWrongMessage(''), 2000)
    }
  }, [wrongMessage])

  // Handle wrong attempt message from props
  useEffect(() => {
    if (wrongAttemptMessage) {
      setShowAttemptMessage(wrongAttemptMessage)
      setTimeout(() => setShowAttemptMessage(''), 2000)
    }
  }, [wrongAttemptMessage])

  // Timer countdown (only if not locked)
  useEffect(() => {
    if (timeLeft > 0 && !showCountdown && !questionLocked) {
      const interval = setInterval(() => {
        setTimeLeft(prev => prev - 1)
      }, 1000)
      return () => clearInterval(interval)
    }
  }, [timeLeft, showCountdown, questionLocked])

  const handleTrueFalseAnswer = (value) => {
    if (!questionLocked) {
      onSubmitAnswer(value)
      setAnswer('')
    }
  }

  const handleTextSubmit = () => {
    if (!questionLocked && answer.trim()) {
      onSubmitAnswer(answer)
      setAnswer('')
    }
  }

  const isTrueFalse = currentQuestion?.question_type === 'truefalse'

  return (
    <div style={{ maxWidth: '800px', margin: '50px auto', padding: '20px' }}>
      {/* Floating Toast Notifications */}
      {(showWrongMessage || showAttemptMessage || showCorrectMessage) && (
        <>
          {showCorrectMessage && (
            <div style={{
              position: 'fixed',
              bottom: '20px',
              left: '50%',
              transform: 'translateX(-50%)',
              padding: '12px 24px',
              borderRadius: '8px',
              background: '#00c851',
              color: 'white',
              zIndex: 1001,
              textAlign: 'center',
              fontSize: '14px',
              boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
              pointerEvents: 'none'
            }}>
              {showCorrectMessage}
            </div>
          )}
          
          {showWrongMessage && (
            <div style={{
              position: 'fixed',
              bottom: '20px',
              left: '50%',
              transform: 'translateX(-50%)',
              padding: '12px 24px',
              borderRadius: '8px',
              background: '#ff4444',
              color: 'white',
              zIndex: 1001,
              textAlign: 'center',
              fontSize: '14px',
              boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
              pointerEvents: 'none'
            }}>
              {showWrongMessage}
            </div>
          )}
          
          {showAttemptMessage && (
            <div style={{
              position: 'fixed',
              bottom: '20px',
              left: '50%',
              transform: 'translateX(-50%)',
              padding: '12px 24px',
              borderRadius: '8px',
              background: '#ff8800',
              color: 'white',
              zIndex: 1001,
              textAlign: 'center',
              fontSize: '14px',
              boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
              pointerEvents: 'none'
            }}>
              {showAttemptMessage}
            </div>
          )}
        </>
      )}

      {/* Winner Banner (shows at top when someone answers correctly) */}
      {winnerInfo && (
        <div style={{
          background: '#00c851',
          color: 'white',
          padding: '16px',
          borderRadius: '8px',
          marginBottom: '20px',
          textAlign: 'center',
          fontSize: '18px',
          fontWeight: 'bold'
        }}>
          ✅ {winnerInfo.nickname} got it right! Answer: {winnerInfo.answer}
        </div>
      )}

      {/* Timer Progress Bar */}
      <div style={{
        width: '100%',
        height: '8px',
        background: 'var(--border)',
        borderRadius: '4px',
        marginBottom: '20px'
      }}>
        <div style={{
          width: questionLocked ? '100%' : `${(timeLeft / 15) * 100}%`,
          height: '100%',
          background: questionLocked ? '#00c851' : (timeLeft < 5 ? 'red' : 'var(--accent)'),
          borderRadius: '4px',
          transition: 'width 1s linear'
        }} />
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
        <div>Question {currentQuestion.question_number}/{currentQuestion.total_questions}</div>
        <div style={{ color: timeLeft < 5 && !questionLocked ? 'red' : 'inherit', fontWeight: 'bold' }}>
          ⏱️ {questionLocked ? 'LOCKED' : `${timeLeft}s`}
        </div>
      </div>
      
      <div style={{ background: 'var(--code-bg)', padding: '40px', borderRadius: '16px', marginBottom: '30px' }}>
        <h2 style={{ margin: 0 }}>{currentQuestion.question_text}</h2>
      </div>
      
      {/* Answer Input Area - disabled when question locked */}
      {isTrueFalse ? (
        <div style={{ display: 'flex', gap: '20px', justifyContent: 'center' }}>
          <button
            onClick={() => handleTrueFalseAnswer('True')}
            disabled={questionLocked}
            style={{
              padding: '20px 40px',
              fontSize: '24px',
              fontWeight: 'bold',
              borderRadius: '12px',
              border: 'none',
              background: questionLocked ? '#666' : 'green',
              color: 'white',
              cursor: questionLocked ? 'not-allowed' : 'pointer',
              flex: 1,
              maxWidth: '200px',
              opacity: questionLocked ? 0.5 : 1
            }}
          >
            ✅ True
          </button>
          <button
            onClick={() => handleTrueFalseAnswer('False')}
            disabled={questionLocked}
            style={{
              padding: '20px 40px',
              fontSize: '24px',
              fontWeight: 'bold',
              borderRadius: '12px',
              border: 'none',
              background: questionLocked ? '#666' : 'red',
              color: 'white',
              cursor: questionLocked ? 'not-allowed' : 'pointer',
              flex: 1,
              maxWidth: '200px',
              opacity: questionLocked ? 0.5 : 1
            }}
          >
            ❌ False
          </button>
        </div>
      ) : (
        <div style={{ display: 'flex', gap: '10px' }}>
          <input
            type="text"
            placeholder={questionLocked ? "Question locked - waiting for next round" : "Type your answer..."}
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter' && !questionLocked) {
                handleTextSubmit()
              }
            }}
            disabled={questionLocked}
            style={{
              flex: 1,
              padding: '14px',
              fontSize: '16px',
              borderRadius: '8px',
              border: '1px solid var(--border)',
              background: questionLocked ? 'var(--code-bg)' : 'var(--bg)',
              color: 'var(--text-h)',
              opacity: questionLocked ? 0.6 : 1
            }}
          />
          <button
            onClick={handleTextSubmit}
            disabled={questionLocked}
            style={{
              padding: '14px 24px',
              fontSize: '16px',
              borderRadius: '8px',
              border: 'none',
              background: questionLocked ? '#666' : 'var(--accent)',
              color: 'white',
              cursor: questionLocked ? 'not-allowed' : 'pointer',
              opacity: questionLocked ? 0.5 : 1
            }}
          >
            Submit
          </button>
        </div>
      )}
      
      {/* Bottom Countdown (appears after correct answer) */}
      {showCountdown && (
        <div style={{
          marginTop: '30px',
          textAlign: 'center',
          padding: '12px',
          background: 'var(--code-bg)',
          borderRadius: '8px',
          fontSize: '18px',
          fontWeight: 'bold',
          color: 'var(--accent)'
        }}>
          Next question in {nextCountdown}...
        </div>
      )}
      
      <div style={{ marginTop: '30px' }}>
        <h3>Scores</h3>
        <div style={{ display: 'flex', justifyContent: 'center', gap: '20px', flexWrap: 'wrap' }}>
          {Object.entries(scores).map(([name, score]) => (
            <div key={name} style={{ padding: '8px 16px', background: 'var(--code-bg)', borderRadius: '8px' }}>
              {name}: {score}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default Game