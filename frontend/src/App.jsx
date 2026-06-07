import { useState, useEffect } from 'react'
import { useWebSocket } from './hooks/useWebSocket'
import Home from './pages/Home'
import Lobby from './pages/Lobby'
import Game from './pages/Game'
import Results from './pages/Results'
import './App.css'

function App() {
  const [nickname, setNickname] = useState('')
  const [roomCode, setRoomCode] = useState('')
  const [screen, setScreen] = useState('home')
  const [players, setPlayers] = useState([])
  const [isHost, setIsHost] = useState(false)
  const [currentQuestion, setCurrentQuestion] = useState(null)
  const [scores, setScores] = useState({})
  const [leaderboard, setLeaderboard] = useState([])
  const [wrongMessage, setWrongMessage] = useState('')
  const [wrongAttemptMessage, setWrongAttemptMessage] = useState('')
  const [correctMessage, setCorrectMessage] = useState('')
  const [showCountdown, setShowCountdown] = useState(false)

  const { isConnected, messages, sendMessage, connect, disconnect } = useWebSocket()

  // Handle messages
  useEffect(() => {
    messages.forEach((msg) => {
      const { event, data } = msg
      
      switch (event) {
        case 'room_created':
          setRoomCode(data.room_code)
          setIsHost(data.is_host)
          setScreen('lobby')
          break
        case 'room_joined':
          setRoomCode(data.room_code)
          setIsHost(data.is_host)
          setScreen('lobby')
          break
        case 'player_list_update':
          setPlayers(data.players)
          break
        case 'game_started':
          setScreen('game')
          break
        case 'question_show':
          setCurrentQuestion(data)
          // Clear all messages when new question arrives
          setWrongMessage('')
          setWrongAttemptMessage('')
          setCorrectMessage('')
          setShowCountdown(false)
          break
        case 'answer_correct':
          setScores(prev => ({ ...prev, [data.nickname]: data.new_score }))
          setCorrectMessage(`${data.nickname} got it right! Answer: ${data.correct_answer}`)
          // Clear old wrong messages when someone answers correctly
          setWrongMessage('')
          setWrongAttemptMessage('')
          setTimeout(() => setCorrectMessage(''), 5000)
          break
        case 'question_locked':
          // Show countdown overlay after someone answers correctly
          setShowCountdown(true)
          break
        case 'answer_wrong':
          setWrongMessage(data.message)
          setTimeout(() => setWrongMessage(''), 2000)
          break
        case 'answer_wrong_attempt':
          setWrongAttemptMessage(data.message)
          setTimeout(() => setWrongAttemptMessage(''), 2000)
          break
        case 'game_over':
          setLeaderboard(data.leaderboard)
          setScreen('results')
          break
        default:
          break
      }
    })
  }, [messages])

  // Connect to backend
  useEffect(() => {
    connect('ws://localhost:8000/ws')
    return () => disconnect()
  }, [connect, disconnect])

  const handleJoin = (action, name, code = null) => {
    setNickname(name)
    if (action === 'create') {
      sendMessage({ action: 'create_room', nickname: name })
    } else {
      sendMessage({ action: 'join_room', nickname: name, room_code: code })
    }
  }

  const handleStartGame = () => {
    sendMessage({ action: 'start_game', room_code: roomCode, nickname })
  }

  const handleSubmitAnswer = (answer) => {
    sendMessage({ action: 'submit_answer', room_code: roomCode, nickname, answer })
  }

  const requestNextQuestion = () => {
    setShowCountdown(false)
    sendMessage({ action: 'request_next_question', room_code: roomCode })
  }

  const handleLeave = () => {
    setScreen('home')
    setNickname('')
    setRoomCode('')
    setPlayers([])
    setScores({})
    setCurrentQuestion(null)
    setWrongMessage('')
    setWrongAttemptMessage('')
    setCorrectMessage('')
    setShowCountdown(false)
  }

  const handlePlayAgain = () => {
    setScreen('home')
    setNickname('')
    setRoomCode('')
    setPlayers([])
    setScores({})
    setCurrentQuestion(null)
    setLeaderboard([])
    setWrongMessage('')
    setWrongAttemptMessage('')
    setCorrectMessage('')
    setShowCountdown(false)
  }

  if (screen === 'home') {
    return <Home onJoin={handleJoin} isConnected={isConnected} />
  }

  if (screen === 'lobby') {
    return (
      <Lobby
        nickname={nickname}
        roomCode={roomCode}
        players={players}
        isHost={isHost}
        onStartGame={handleStartGame}
        onLeave={handleLeave}
      />
    )
  }

  if (screen === 'game' && currentQuestion) {
    return (
      <Game
        currentQuestion={currentQuestion}
        scores={scores}
        nickname={nickname}
        onSubmitAnswer={handleSubmitAnswer}
        wrongMessage={wrongMessage}
        wrongAttemptMessage={wrongAttemptMessage}
        correctMessage={correctMessage}
        showCountdown={showCountdown}
        onCountdownComplete={requestNextQuestion}
      />
    )
  }

  if (screen === 'results') {
    return <Results leaderboard={leaderboard} onPlayAgain={handlePlayAgain} />
  }

  return null
}

export default App