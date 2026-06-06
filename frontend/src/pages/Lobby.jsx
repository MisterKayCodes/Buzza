function Lobby({ nickname, roomCode, players, isHost, onStartGame, onLeave }) {
  return (
    <div style={{ maxWidth: '600px', margin: '50px auto', padding: '20px', textAlign: 'center' }}>
      <h1>Lobby</h1>
      <p>Welcome, {nickname}!</p>
      <p>
        Room code: <code style={{ fontSize: '24px', padding: '8px 16px' }}>{roomCode}</code>
        <button
          onClick={() => {
            navigator.clipboard.writeText(roomCode)
            alert('Room code copied!')
          }}
          style={{
            marginLeft: '10px',
            padding: '4px 12px',
            fontSize: '14px',
            borderRadius: '6px',
            border: '1px solid var(--border)',
            background: 'transparent',
            cursor: 'pointer'
          }}
        >
          📋 Copy
        </button>
      </p>
      
      <div style={{ marginTop: '40px' }}>
        <h2>Players ({players.length})</h2>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', alignItems: 'center', marginTop: '16px' }}>
          {players.map((p, idx) => (
            <div key={idx} style={{ padding: '8px 16px', background: 'var(--code-bg)', borderRadius: '8px', minWidth: '200px' }}>
              {p.nickname} {p.is_host && '👑'} {p.nickname === nickname && '(you)'}
            </div>
          ))}
        </div>
      </div>
      
      {isHost && players.length >= 2 ? (
        <button
          onClick={onStartGame}
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
          🚀 Start Game
        </button>
      ) : isHost && players.length < 2 ? (
        <p style={{ marginTop: '40px', color: 'var(--text)' }}>Waiting for at least 2 players... (Need {2 - players.length} more)</p>
      ) : null}
      
      <button
        onClick={onLeave}
        style={{
          marginTop: '40px',
          padding: '10px 20px',
          background: 'transparent',
          border: '1px solid var(--border)',
          borderRadius: '8px',
          color: 'var(--text)',
          cursor: 'pointer'
        }}
      >
        Leave Room
      </button>
    </div>
  )
}

export default Lobby