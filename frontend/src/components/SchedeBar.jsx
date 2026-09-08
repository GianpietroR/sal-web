export default function SchedeBar({ cantieri, activeId, onOpen, onNew }) {
  return (
    <div className="topbar">
      <span className="brand">SAL Web</span>
      <div className="schede">
        {cantieri.map((c) => (
          <button
            key={c.id}
            className={'scheda' + (c.id === activeId ? ' active' : '')}
            onClick={() => onOpen(c.id)}
          >
            {c.nome}
          </button>
        ))}
        <button className="scheda new" onClick={onNew}>
          + Nuovo cantiere
        </button>
      </div>
    </div>
  )
}
