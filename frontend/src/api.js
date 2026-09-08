// Wrapper fetch per l'API SAL Web (stessa origine, cookie di sessione).
async function request(path, options = {}) {
  const res = await fetch(path, {
    credentials: 'same-origin',
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    let detail = `Errore ${res.status}`
    try {
      detail = (await res.json()).detail || detail
    } catch {
      /* corpo non JSON */
    }
    throw new Error(detail)
  }
  return res.json()
}

export const api = {
  me: () => request('/api/me'),
  login: (username, password) =>
    request('/api/login', { method: 'POST', body: JSON.stringify({ username, password }) }),
  logout: () => request('/api/logout', { method: 'POST' }),
  listCantieri: () => request('/api/cantieri'),
  createCantiere: (data) => request('/api/cantieri', { method: 'POST', body: JSON.stringify(data) }),
}
