const BASE_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

export async function fetchMeetings() {
  const res = await fetch(`${BASE_URL}/meetings`)
  if (!res.ok) throw new Error('Failed to fetch meetings')
  return await res.json()
}

export async function fetchMeetingById(id) {
  const res = await fetch(`${BASE_URL}/meetings/${id}`)
  if (!res.ok) throw new Error('Failed to fetch meeting')
  return await res.json()
}

export async function uploadMeeting(data) {
  const res = await fetch(`${BASE_URL}/meetings`, {
    method: 'POST',
    body: data, // FormData directly
  });

  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(`Failed to upload meeting: ${errorText}`);
  }

  return await res.json();
}

