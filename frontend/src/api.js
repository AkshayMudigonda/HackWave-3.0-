const configuredBaseUrl = import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, '');

export const API_BASE_URL = configuredBaseUrl || 'http://localhost:8000';

export async function submitGoal(message) {
  const response = await fetch(`${API_BASE_URL}/api/assist`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  });

  let payload;
  try {
    payload = await response.json();
  } catch {
    throw new Error('The assistant returned an invalid response.');
  }

  if (!response.ok || !payload.success) {
    throw new Error(payload?.error || 'The assistant could not complete this request.');
  }

  return payload;
}
