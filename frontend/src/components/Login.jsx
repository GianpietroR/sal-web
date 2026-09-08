import { useState } from 'react'
import { api } from '../api.js'

export default function Login({ onLogin }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  async function submit(e) {
    e.preventDefault()
    setBusy(true)
    setError('')
    try {
      await api.login(username, password)
      onLogin()
    } catch (err) {
      setError(err.message || 'Errore di accesso')
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="app">
      <form className="card" onSubmit={submit}>
        <h1 style={{ marginTop: 0 }}>SAL Web</h1>
        <p className="muted">Accedi con il tuo account.</p>
        <label>Nome utente</label>
        <input value={username} onChange={(e) => setUsername(e.target.value)} autoComplete="username" />
        <label>Password</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          autoComplete="current-password"
        />
        {error && (
          <p style={{ color: '#c62828', fontSize: '0.9rem' }}>{error}</p>
        )}
        <button className="primary" disabled={busy}>
          {busy ? 'Accesso…' : 'Accedi'}
        </button>
      </form>
    </div>
  )
}
