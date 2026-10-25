
const API_BASE_URL = '/api'

export async function simulatePhoton(parameters, signal) {
  const response = await fetch(`${API_BASE_URL}/simulate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(parameters),
    signal,
  })

  if (!response.ok) {
    const message = await response.text()
    throw new Error(`Simulation failed (${response.status}): ${message}`)
  }

  return response.json()
}
