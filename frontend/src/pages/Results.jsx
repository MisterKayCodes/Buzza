function Results({ leaderboard, onPlayAgain }) {
  return (
    <div style={{ maxWidth: '600px', margin: '100px auto', padding: '20px', textAlign: 'center' }}>
      <h1>Game Over!</h1>
      <h2 style={{ marginBottom: '30px' }}>🏆 Winner: {leaderboard[0]?.nickname} 🏆</h2>
      
      <div style={{ marginTop: '20px' }}>
        {leaderboard.map((player, idx) => (
          <div key={idx} style={{ display: 'flex', justifyContent: 'space-between', padding: '12px', borderBottom: '1px solid var(--border)' }}>
            <span>{idx + 1}. {player.nickname}</span>
            <span>{player.score} points</span>
          </div>
        ))}
      </div>
      
      <button
        onClick={onPlayAgain}
        style={{
          marginTop: '40px',
          padding: '14px 28px',
          fontSize: '18px',
          borderRadius: '8px',
          border: 'none',
          background: 'var(--accent)',
          color: 'white',
          cursor: 'pointer'
        }}
      >
        Play Again
      </button>
    </div>
  )
}

export default Results