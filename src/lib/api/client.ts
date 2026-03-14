const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function createHelpRequest(data: {
  name: string;
  location: string;
  help_type: string;
  description: string;
  language: string;
  contact_info?: string;
}) {
  const res = await fetch(`${BASE}/help-request`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function getHelpRequests(filters?: { location?: string; help_type?: string }) {
  const params = new URLSearchParams();
  if (filters?.location) params.set('location', filters.location);
  if (filters?.help_type) params.set('help_type', filters.help_type);
  const q = params.toString();
  const res = await fetch(`${BASE}/help-requests${q ? '?' + q : ''}`);
  if (!res.ok) throw new Error(await res.text());
  const json = await res.json();
  return json.items ?? [];
}

export async function getHelpRequest(id: string) {
  const res = await fetch(`${BASE}/help-requests/${id}`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function getNgos(location?: string) {
  const q = location ? '?location=' + encodeURIComponent(location) : '';
  const res = await fetch(`${BASE}/ngos${q}`);
  if (!res.ok) throw new Error(await res.text());
  const json = await res.json();
  return json.items ?? [];
}

export async function getNgosNearby(location: string) {
  const res = await fetch(`${BASE}/ngos/nearby?location=${encodeURIComponent(location)}`);
  if (!res.ok) throw new Error(await res.text());
  const json = await res.json();
  return json.items ?? [];
}

export async function createNgo(data: {
  name: string;
  services: string;
  location: string;
  contact_info: string;
}) {
  const res = await fetch(`${BASE}/ngo`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function getStats(): Promise<{ help_requests: number; ngos: number }> {
  const res = await fetch(`${BASE}/stats`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function seedDemo(): Promise<{ message: string; help_requests: number; ngos: number }> {
  const res = await fetch(`${BASE}/seed`, { method: 'POST' });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}
