import { useState, useEffect } from 'react'

function Game({ currentQuestion, scores, nickname, onSubmitAnswer, wrongMessage, wrongAttemptMessage, correctMessage }) {
  const [answer, setAnswer] = useState('')
  const [timeLeft, setTimeLeft] = useState(15)
  const [showWrongMessage, setShowWrongMessage] = useState('')
  const [showAttemptMessage, setShowAttemptMessage] = useState('')
  const [showCorrectMessage, setShowCorrectMessage] = useState('')

  // Reset timer and messages when new question arrives
  useEffect(() => {
    if (currentQuestion) {
      setTimeLeft(currentQuestion.timer_seconds || 15)
      setAnswer('')
      setShowWrongMessage('')
      setShowAttemptMessage('')
      setShowCorrectMessage('')
    }
  }, [currentQuestion])

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

  // Handle correct message from props
  useEffect(() => {
    if (correctMessage) {
      setShowCorrectMessage(correctMessage)
      setTimeout(() => setShowCorrectMessage(''), 3000)
    }
  }, [correctMessage])

  // Timer countdown
  useEffect(() => {
    if (timeLeft > 0) {
      const interval = setInterval(() => {
        setTimeLeft(prev => prev - 1)
      }, 1000)
      return () => clearInterval(interval)
    }
  }, [timeLeft])

  const handleTrueFalseAnswer = (value) => {
    onSubmitAnswer(value)
    setAnswer('')
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
              bottom: '100px',
              left: '50%',
              transform: 'translateX(-50%)',
              padding: '12px 24px',
              borderRadius: '8px',
              background: '#00c851',
              color: 'white',
              zIndex: 1000,
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
              bottom: '100px',
              left: '50%',
              transform: 'translateX(-50%)',
              padding: '12px 24px',
              borderRadius: '8px',
              background: '#ff4444',
              color: 'white',
              zIndex: 1000,
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
              bottom: '100px',
              left: '50%',
              transform: 'translateX(-50%)',
              padding: '12px 24px',
              borderRadius: '8px',
              background: '#ff8800',
              color: 'white',
              zIndex: 1000,
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

      {/* Timer Progress Bar */}
      <div style={{
        width: '100%',
        height: '8px',
        background: 'var(--border)',
        borderRadius: '4px',
        marginBottom: '20px'
      }}>
        <div style={{
          width: `${(timeLeft / 15) * 100}%`,
          height: '100%',
          background: timeLeft < 5 ? 'red' : 'var(--accent)',
          borderRadius: '4px',
          transition: 'width 1s linear'
        }} />
      </div>

      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
        <div>Question {currentQuestion.question_number}/{currentQuestion.total_questions}</div>
        <div style={{ color: timeLeft < 5 ? 'red' : 'inherit', fontWeight: 'bold' }}>
          ⏱️ {timeLeft}s
        </div>
      </div>
      
      <div style={{ background: 'var(--code-bg)', padding: '40px', borderRadius: '16px', marginBottom: '30px' }}>
        <h2 style={{ margin: 0 }}>{currentQuestion.question_text}</h2>
      </div>
      
      {/* Answer Input Area */}
      {isTrueFalse ? (
        // True/False Buttons
        <div style={{ display: 'flex', gap: '20px', justifyContent: 'center' }}>
          <button
            onClick={() => handleTrueFalseAnswer('True')}
            style={{
              padding: '20px 40px',
              fontSize: '24px',
              fontWeight: 'bold',
              borderRadius: '12px',
              border: 'none',
              background: 'green',
              color: 'white',
              cursor: 'pointer',
              flex: 1,
              maxWidth: '200px'
            }}
          >
            ✅ True
          </button>
          <button
            onClick={() => handleTrueFalseAnswer('False')}
            style={{
              padding: '20px 40px',
              fontSize: '24px',
              fontWeight: 'bold',
              borderRadius: '12px',
              border: 'none',
              background: 'red',
              color: 'white',
              cursor: 'pointer',
              flex: 1,
              maxWidth: '200px'
            }}
          >
            ❌ False
          </button>
        </div>
      ) : (
        // Text Input for other question types
        <div style={{ display: 'flex', gap: '10px' }}>
          <input
            type="text"
            placeholder="Type your answer..."
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter') {
                onSubmitAnswer(answer)
                setAnswer('')
              }
            }}
            style={{
              flex: 1,
              padding: '14px',
              fontSize: '16px',
              borderRadius: '8px',
              border: '1px solid var(--border)',
              background: 'var(--bg)',
              color: 'var(--text-h)'
            }}
          />
          <button
            onClick={() => {
              onSubmitAnswer(answer)
              setAnswer('')
            }}
            style={{
              padding: '14px 24px',
              fontSize: '16px',
              borderRadius: '8px',
              border: 'none',
              background: 'var(--accent)',
              color: 'white',
              cursor: 'pointer'
            }}
          >
            Submit
          </button>
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