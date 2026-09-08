import { useEffect, useState } from 'react'
import { api } from './api.js'
import Login from './components/Login.jsx'
import SchedeBar from './components/SchedeBar.jsx'
import NewCantiereForm from './components/NewCantiereForm.jsx'

export default function App() {
  const [user, setUser] = useState(null)
  const [checking, setChecking] = useState(true)
  const [cantieri, setCantieri] = useState([])
  const [showNew, setShowNew] = useState(false)
  // Ogni scheda del browser è una sessione autonoma: la scheda attiva vive
  // solo in questa finestra (sessionStorage), mai condivisa tra utenti.
  const [activeId, setActiveId] = useState(
    () => Number(sessionStorage.getItem('sal_active_cantiere')) || null,
  )

  useEffect(() => {
    api.me()
      .then((u) => setUser(u))
      .catch(() => setUser(null))
      .finally(() => setChecking(false))
  }, [])

  useEffect(() => {
    if (!user) return
    api.listCantieri().then(setCantieri).catch(console.error)
  }, [user])

  function open(id) {
    setActiveId(id)
    sessionStorage.setItem('sal_active_cantiere', String(id))
    setShowNew(false)
  }

  async function logout() {
    await api.logout()
    setUser(null)
    setCantieri([])
    setActiveId(null)
    sessionStorage.removeItem('sal_active_cantiere')
  }

  if (checking) return <div className="app"><p>Caricamento…</p></div>
  if (!user) {
    return <Login onLogin={async () => setUser(await api.me())} />
  }

  const active = cantieri.find((c) => c.id === activeId) || null

  return (
    <div className="app">
      <SchedeBar
        cantieri={cantieri}
        activeId={activeId}
        onOpen={open}
        onNew={() => setShowNew(true)}
      />
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
        <span className="muted">
          {cantieri.length === 0
            ? 'Nessuna scheda aperta.'
            : `Scheda attiva: ${active ? active.nome : '—'}`}
        </span>
        <button className="secondary" style={{ marginTop: 0 }} onClick={logout}>
          Esci ({user.display_name || user.username})
        </button>
      </div>

      {showNew && (
        <NewCantiereForm onCreated={(id) => open(id)} onCancel={() => setShowNew(false)} />
      )}

      {!showNew && active && (
        <div className="card wide">
          <h2 style={{ marginTop: 0 }}>{active.nome}</h2>
          <p className="muted">
            Scheda aperta. Computo, SAL e dashboard arrivano nelle prossime fasi.
          </p>
        </div>
      )}

      {!showNew && !active && cantieri.length > 0 && (
        <div className="card wide">
          <p style={{ marginTop: 0 }}>Seleziona una scheda in alto per lavorare sul cantiere.</p>
        </div>
      )}
    </div>
  )
}
