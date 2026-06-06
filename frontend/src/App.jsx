import { useState } from 'react'
import './App.css'

function App() {
  const [nickname, setNickname] = useState('')
  const [roomCode, setRoomCode] = useState('')
  const [screen, setScreen] = useState('home') // home, lobby, game, results

  // For demo - will connect to WebSocket later
  const handleCreateRoom = () => {
    if (!nickname.trim()) {
      alert('Please enter a nickname')
      return
    }
    console.log('Creating room for:', nickname)
    setScreen('lobby')
  }

  const handleJoinRoom = () => {
    if (!nickname.trim()) {
      alert('Please enter a nickname')
      return
    }
    if (!roomCode.trim()) {
      alert('Please enter a room code')
      return
    }
    console.log('Joining room:', roomCode, 'as:', nickname)
    setScreen('lobby')
  }

  // Home screen
  if (screen === 'home') {
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
            onClick={handleCreateRoom}
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
              onClick={handleJoinRoom}
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
      </div>
    )
  }

  // Lobby screen (temporary)
  if (screen === 'lobby') {
    return (
      <div style={{ maxWidth: '600px', margin: '100px auto', padding: '20px', textAlign: 'center' }}>
        <h1>Lobby</h1>
        <p>Welcome, {nickname}!</p>
        <p>Room code: <strong>{roomCode || 'CREATING...'}</strong></p>
        <div style={{ marginTop: '40px' }}>
          <div className="ticks"></div>
          <p>Waiting for players...</p>
          <div className="ticks"></div>
        </div>
        <button
          onClick={() => setScreen('home')}
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

  return null
}

export default App