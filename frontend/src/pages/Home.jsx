import { useState } from 'react'

function Home({ onJoin, isConnected }) {
  const [nickname, setNickname] = useState('')
  const [roomCode, setRoomCode] = useState('')

  const handleCreate = () => {
    if (!nickname.trim()) {
      alert('Please enter a nickname')
      return
    }
    onJoin('create', nickname)
  }

  const handleJoin = () => {
    if (!nickname.trim()) {
      alert('Please enter a nickname')
      return
    }
    if (!roomCode.trim()) {
      alert('Please enter a room code')
      return
    }
    onJoin('join', nickname, roomCode.toUpperCase())
  }

  return (
    <div style={{ maxWidth: '400px', margin: '100px auto', padding: '20px' }}>
      <h1>BUZZA</h1>
      <p>Real-time Multiplayer Trivia</p>
      
      <div style={{ marginTop: '40px' }}>
        <input
          type="text"
          placeholder="Enter your nickname"
          value={nickname}
          onChange={(e) => setNickname(e.target.value)}
          style={{
            width: '100%',
            padding: '12px',
            fontSize: '16px',
            borderRadius: '8px',
            border: '1px solid var(--border)',
            background: 'var(--bg)',
            color: 'var(--text-h)',
            marginBottom: '20px'
          }}
        />
        
        <button
          onClick={handleCreate}
          style={{
            width: '100%',
            padding: '12px',
            fontSize: '18px',
            borderRadius: '8px',
            border: 'none',
            background: 'var(--accent)',
            color: 'white',
            cursor: 'pointer',
            marginBottom: '12px'
          }}
        >
          🎮 Create New Room
        </button>
        
        <div style={{ textAlign: 'center', margin: '10px 0' }}>or</div>
        
        <div style={{ display: 'flex', gap: '10px' }}>
          <input
            type="text"
            placeholder="Room Code"
            value={roomCode}
            onChange={(e) => setRoomCode(e.target.value.toUpperCase())}
            style={{
              flex: 1,
              padding: '12px',
              fontSize: '16px',
              borderRadius: '8px',
              border: '1px solid var(--border)',
              background: 'var(--bg)',
              color: 'var(--text-h)'
            }}
          />
          <button
            onClick={handleJoin}
            style={{
              padding: '12px 20px',
              fontSize: '16px',
              borderRadius: '8px',
              border: '1px solid var(--accent)',
              background: 'transparent',
              color: 'var(--accent)',
              cursor: 'pointer'
            }}
          >
            Join
          </button>
        </div>
      </div>
      
      <div style={{ marginTop: '20px', fontSize: '12px', color: 'var(--text)' }}>
        Status: {isConnected ? '🟢 Connected' : '🔴 Connecting to server...'}
      </div>
    </div>
  )
}

export default Home