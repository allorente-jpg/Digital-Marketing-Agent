import { useEffect, useState } from 'react';
import { getCustomers, createCustomer, getInvoices, createInvoice, getWorkflows, createWorkflow } from './api';

const emptyCustomer = { name: '', email: '', phone: '', notes: '' };
const emptyInvoice = { customer_id: 0, amount: 0, due_date: '', description: '' };
const emptyWorkflow = { name: '', description: '', trigger: 'invoice_due', action: 'send_email' };

function App() {
  const [customers, setCustomers] = useState([]);
  const [invoices, setInvoices] = useState([]);
  const [workflows, setWorkflows] = useState([]);
  const [customerForm, setCustomerForm] = useState(emptyCustomer);
  const [invoiceForm, setInvoiceForm] = useState(emptyInvoice);
  const [workflowForm, setWorkflowForm] = useState(emptyWorkflow);
  const [message, setMessage] = useState('');

  useEffect(() => {
    async function load() {
      try {
        setCustomers(await getCustomers());
        setInvoices(await getInvoices());
        setWorkflows(await getWorkflows());
      } catch (error) {
        setMessage(error.message);
      }
    }
    load();
  }, []);

  const handleCustomerSubmit = async (event) => {
    event.preventDefault();
    try {
      const data = await createCustomer(customerForm);
      setCustomers((current) => [...current, data]);
      setCustomerForm(emptyCustomer);
      setMessage('Customer added.');
    } catch (error) {
      setMessage(error.message);
    }
  };

  const handleInvoiceSubmit = async (event) => {
    event.preventDefault();
    try {
      const data = await createInvoice(invoiceForm);
      setInvoices((current) => [...current, data]);
      setInvoiceForm(emptyInvoice);
      setMessage('Invoice created.');
    } catch (error) {
      setMessage(error.message);
    }
  };

  const handleWorkflowSubmit = async (event) => {
    event.preventDefault();
    try {
      const data = await createWorkflow(workflowForm);
      setWorkflows((current) => [...current, data]);
      setWorkflowForm(emptyWorkflow);
      setMessage('Workflow created.');
    } catch (error) {
      setMessage(error.message);
    }
  };

  return (
    <div className="container">
      <header>
        <h1>Digital Marketing Agent</h1>
        <p>Manage clients, invoices and marketing workflows in one place.</p>
      </header>

      {message && <div className="message">{message}</div>}

      <section className="panel">
        <h2>Customers</h2>
        <form onSubmit={handleCustomerSubmit}>
          <div className="grid">
            <input value={customerForm.name} placeholder="Name" onChange={(e) => setCustomerForm({ ...customerForm, name: e.target.value })} required />
            <input value={customerForm.email} placeholder="Email" onChange={(e) => setCustomerForm({ ...customerForm, email: e.target.value })} />
            <input value={customerForm.phone} placeholder="Phone" onChange={(e) => setCustomerForm({ ...customerForm, phone: e.target.value })} />
            <input value={customerForm.notes} placeholder="Notes" onChange={(e) => setCustomerForm({ ...customerForm, notes: e.target.value })} />
          </div>
          <button type="submit">Add Customer</button>
        </form>
        <div className="list">
          {customers.length ? customers.map((customer) => (
            <div key={customer.id} className="item">
              <strong>{customer.name}</strong>
              <span>{customer.email || 'No email'}</span>
              <span>{customer.phone || 'No phone'}</span>
            </div>
          )) : <p>No customers yet.</p>}
        </div>
      </section>

      <section className="panel">
        <h2>Invoices</h2>
        <form onSubmit={handleInvoiceSubmit}>
          <div className="grid">
            <input type="number" value={invoiceForm.customer_id} placeholder="Customer ID" onChange={(e) => setInvoiceForm({ ...invoiceForm, customer_id: Number(e.target.value) })} required />
            <input type="number" step="0.01" value={invoiceForm.amount} placeholder="Amount" onChange={(e) => setInvoiceForm({ ...invoiceForm, amount: Number(e.target.value) })} required />
            <input type="text" value={invoiceForm.due_date} placeholder="Due date" onChange={(e) => setInvoiceForm({ ...invoiceForm, due_date: e.target.value })} />
            <input type="text" value={invoiceForm.description} placeholder="Description" onChange={(e) => setInvoiceForm({ ...invoiceForm, description: e.target.value })} />
          </div>
          <button type="submit">Create Invoice</button>
        </form>
        <div className="list">
          {invoices.length ? invoices.map((invoice) => (
            <div key={invoice.id} className="item">
              <strong>Invoice #{invoice.id}</strong>
              <span>{invoice.description || 'No description'}</span>
              <span>{invoice.amount.toFixed(2)} USD</span>
              <span>Status: {invoice.status}</span>
            </div>
          )) : <p>No invoices yet.</p>}
        </div>
      </section>

      <section className="panel">
        <h2>Workflows</h2>
        <form onSubmit={handleWorkflowSubmit}>
          <div className="grid">
            <input value={workflowForm.name} placeholder="Workflow name" onChange={(e) => setWorkflowForm({ ...workflowForm, name: e.target.value })} required />
            <input value={workflowForm.trigger} placeholder="Trigger" onChange={(e) => setWorkflowForm({ ...workflowForm, trigger: e.target.value })} required />
            <input value={workflowForm.action} placeholder="Action" onChange={(e) => setWorkflowForm({ ...workflowForm, action: e.target.value })} required />
            <input value={workflowForm.description} placeholder="Description" onChange={(e) => setWorkflowForm({ ...workflowForm, description: e.target.value })} />
          </div>
          <button type="submit">Create Workflow</button>
        </form>
        <div className="list">
          {workflows.length ? workflows.map((workflow) => (
            <div key={workflow.id} className="item">
              <strong>{workflow.name}</strong>
              <span>Trigger: {workflow.trigger}</span>
              <span>Action: {workflow.action}</span>
            </div>
          )) : <p>No workflows yet.</p>}
        </div>
      </section>
    </div>
  );
}

export default App;
