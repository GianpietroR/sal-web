import { useState } from 'react'
import { api } from '../api.js'

const EMPTY = { nome: '', committente: '', impresa: '', tecnico: '', oggetto: '' }

export default function NewCantiereForm({ onCreated, onCancel }) {
  const [form, setForm] = useState(EMPTY)
  const [busy, setBusy] = useState(false)

  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value })

  async function submit(e) {
    e.preventDefault()
    if (!form.nome.trim()) return
    setBusy(true)
    try {
      const res = await api.createCantiere(form)
      onCreated(res.id)
    } finally {
      setBusy(false)
    }
  }

  return (
    <form className="card" onSubmit={submit}>
      <h2 style={{ marginTop: 0 }}>Nuovo cantiere</h2>
      <p className="muted">I campi compaiono sulla copertina del PDF.</p>
      <label>Nome cantiere *</label>
      <input value={form.nome} onChange={set('nome')} />
      <label>Committente</label>
      <input value={form.committente} onChange={set('committente')} />
      <label>Impresa</label>
      <input value={form.impresa} onChange={set('impresa')} />
      <label>Tecnico / professionista</label>
      <input value={form.tecnico} onChange={set('tecnico')} />
      <label>Oggetto dei lavori</label>
      <input value={form.oggetto} onChange={set('oggetto')} />
      <button className="primary" disabled={busy}>
        {busy ? 'Creazione…' : 'Crea cantiere'}
      </button>
      {onCancel && (
        <button type="button" className="secondary" onClick={onCancel}>
          Annulla
        </button>
      )}
    </form>
  )
}
