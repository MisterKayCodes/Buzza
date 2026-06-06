import { useState } from 'react'

function Game({ currentQuestion, scores, nickname, onSubmitAnswer }) {
  const [answer, setAnswer] = useState('')
  const [timer, setTimer] = useState(currentQuestion?.timer_seconds || 15)

  return (
    <div style={{ maxWidth: '800px', margin: '50px auto', padding: '20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
        <div>Question {currentQuestion.question_number}/{currentQuestion.total_questions}</div>
        <div style={{ color: timer < 5 ? 'red' : 'inherit' }}>⏱️ {timer}s</div>
      </div>
      
      <div style={{ background: 'var(--code-bg)', padding: '40px', borderRadius: '16px', marginBottom: '30px' }}>
        <h2 style={{ margin: 0 }}>{currentQuestion.question_text}</h2>
      </div>
      
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