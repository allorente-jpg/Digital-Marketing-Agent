const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });

  if (!res.ok) {
    const error = await res.text();
    throw new Error(error || 'API request failed');
  }

  return res.json();
}

export async function getCustomers() {
  return request('/customers/');
}

export async function createCustomer(customer) {
  return request('/customers/', {
    method: 'POST',
    body: JSON.stringify(customer),
  });
}

export async function getInvoices() {
  return request('/invoices/');
}

export async function createInvoice(invoice) {
  return request('/invoices/', {
    method: 'POST',
    body: JSON.stringify(invoice),
  });
}

export async function getWorkflows() {
  return request('/workflows/');
}

export async function createWorkflow(workflow) {
  return request('/workflows/', {
    method: 'POST',
    body: JSON.stringify(workflow),
  });
}

export async function getAgents() {
  return request('/agents/');
}

export async function createAgent(agent) {
  return request('/agents/', {
    method: 'POST',
    body: JSON.stringify(agent),
  });
}

export async function startAgent(id) {
  return request(`/agents/${id}/start`, { method: 'POST' });
}

export async function stopAgent(id) {
  return request(`/agents/${id}/stop`, { method: 'POST' });
}
