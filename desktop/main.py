import sys
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

BASE_DIR = Path(__file__).resolve().parent
BACKEND_APP_DIR = BASE_DIR.parent / "backend" / "app"
if str(BACKEND_APP_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_APP_DIR))

import crud
import schemas
from database import SessionLocal


class BusinessDesktopApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Digital Marketing Agent — Desktop")
        self.geometry("900x700")
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        self.db = SessionLocal()

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=12)

        self.customer_frame = ttk.Frame(self.notebook)
        self.invoice_frame = ttk.Frame(self.notebook)
        self.workflow_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.customer_frame, text="Customers")
        self.notebook.add(self.invoice_frame, text="Invoices")
        self.notebook.add(self.workflow_frame, text="Workflows")

        self.customer_widgets()
        self.invoice_widgets()
        self.workflow_widgets()

        self.refresh_all()

    def customer_widgets(self):
        frame = self.customer_frame
        form = ttk.Labelframe(frame, text="New Customer")
        form.pack(fill="x", padx=10, pady=10)

        self.customer_name = tk.StringVar()
        self.customer_email = tk.StringVar()
        self.customer_phone = tk.StringVar()
        self.customer_notes = tk.StringVar()

        entries = [
            ("Name", self.customer_name),
            ("Email", self.customer_email),
            ("Phone", self.customer_phone),
            ("Notes", self.customer_notes),
        ]
        for label, var in entries:
            row = ttk.Frame(form)
            row.pack(fill="x", pady=4)
            ttk.Label(row, text=f"{label}:", width=12).pack(side="left")
            ttk.Entry(row, textvariable=var, width=40).pack(side="left", fill="x", expand=True)

        ttk.Button(form, text="Add Customer", command=self.create_customer).pack(pady=8)

        self.customer_list = ttk.Treeview(frame, columns=("email", "phone", "notes"), show="headings")
        self.customer_list.heading("email", text="Email")
        self.customer_list.heading("phone", text="Phone")
        self.customer_list.heading("notes", text="Notes")
        self.customer_list.pack(fill="both", expand=True, padx=10, pady=10)

    def invoice_widgets(self):
        frame = self.invoice_frame
        form = ttk.Labelframe(frame, text="New Invoice")
        form.pack(fill="x", padx=10, pady=10)

        self.invoice_customer_id = tk.StringVar()
        self.invoice_amount = tk.DoubleVar()
        self.invoice_due_date = tk.StringVar()
        self.invoice_description = tk.StringVar()

        entries = [
            ("Customer ID", self.invoice_customer_id),
            ("Amount", self.invoice_amount),
            ("Due date", self.invoice_due_date),
            ("Description", self.invoice_description),
        ]
        for label, var in entries:
            row = ttk.Frame(form)
            row.pack(fill="x", pady=4)
            ttk.Label(row, text=f"{label}:", width=12).pack(side="left")
            ttk.Entry(row, textvariable=var, width=40).pack(side="left", fill="x", expand=True)

        ttk.Button(form, text="Create Invoice", command=self.create_invoice).pack(pady=8)

        self.invoice_list = ttk.Treeview(frame, columns=("customer", "amount", "status", "due"), show="headings")
        self.invoice_list.heading("customer", text="Customer ID")
        self.invoice_list.heading("amount", text="Amount")
        self.invoice_list.heading("status", text="Status")
        self.invoice_list.heading("due", text="Due Date")
        self.invoice_list.pack(fill="both", expand=True, padx=10, pady=10)

    def workflow_widgets(self):
        frame = self.workflow_frame
        form = ttk.Labelframe(frame, text="New Workflow")
        form.pack(fill="x", padx=10, pady=10)

        self.workflow_name = tk.StringVar()
        self.workflow_trigger = tk.StringVar(value="invoice_due")
        self.workflow_action = tk.StringVar(value="send_email")
        self.workflow_description = tk.StringVar()

        entries = [
            ("Name", self.workflow_name),
            ("Trigger", self.workflow_trigger),
            ("Action", self.workflow_action),
            ("Description", self.workflow_description),
        ]
        for label, var in entries:
            row = ttk.Frame(form)
            row.pack(fill="x", pady=4)
            ttk.Label(row, text=f"{label}:", width=12).pack(side="left")
            ttk.Entry(row, textvariable=var, width=40).pack(side="left", fill="x", expand=True)

        ttk.Button(form, text="Create Workflow", command=self.create_workflow).pack(pady=8)

        self.workflow_list = ttk.Treeview(frame, columns=("trigger", "action", "active"), show="headings")
        self.workflow_list.heading("trigger", text="Trigger")
        self.workflow_list.heading("action", text="Action")
        self.workflow_list.heading("active", text="Active")
        self.workflow_list.pack(fill="both", expand=True, padx=10, pady=10)

    def refresh_all(self):
        self.refresh_customers()
        self.refresh_invoices()
        self.refresh_workflows()

    def refresh_customers(self):
        for item in self.customer_list.get_children():
            self.customer_list.delete(item)
        customers = crud.get_customers(self.db, owner_id=1)
        for cust in customers:
            self.customer_list.insert("", "end", iid=cust.id, values=(cust.email or "", cust.phone or "", cust.notes or ""))

    def refresh_invoices(self):
        for item in self.invoice_list.get_children():
            self.invoice_list.delete(item)
        invoices = crud.get_invoices(self.db, owner_id=1)
        for inv in invoices:
            self.invoice_list.insert("", "end", iid=inv.id, values=(inv.customer_id, f"{inv.amount:.2f}", inv.status, inv.due_date or ""))

    def refresh_workflows(self):
        for item in self.workflow_list.get_children():
            self.workflow_list.delete(item)
        workflows = crud.get_workflows(self.db, owner_id=1)
        for wf in workflows:
            self.workflow_list.insert("", "end", iid=wf.id, values=(wf.trigger, wf.action, str(wf.is_active)))

    def create_customer(self):
        try:
            customer = schemas.CustomerCreate(
                name=self.customer_name.get().strip(),
                email=self.customer_email.get().strip() or None,
                phone=self.customer_phone.get().strip() or None,
                notes=self.customer_notes.get().strip() or None,
            )
            if not customer.name:
                raise ValueError("Customer name is required")
            crud.create_customer(self.db, customer, owner_id=1)
            self.refresh_customers()
            self.customer_name.set("")
            self.customer_email.set("")
            self.customer_phone.set("")
            self.customer_notes.set("")
            messagebox.showinfo("Success", "Customer added.")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def create_invoice(self):
        try:
            invoice = schemas.InvoiceCreate(
                customer_id=int(self.invoice_customer_id.get()),
                amount=float(self.invoice_amount.get()),
                due_date=self.invoice_due_date.get().strip() or None,
                description=self.invoice_description.get().strip() or None,
            )
            crud.create_invoice(self.db, invoice, owner_id=1)
            self.refresh_invoices()
            self.invoice_customer_id.set("")
            self.invoice_amount.set(0.0)
            self.invoice_due_date.set("")
            self.invoice_description.set("")
            messagebox.showinfo("Success", "Invoice created.")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def create_workflow(self):
        try:
            workflow = schemas.WorkflowCreate(
                name=self.workflow_name.get().strip(),
                description=self.workflow_description.get().strip() or None,
                trigger=self.workflow_trigger.get().strip(),
                action=self.workflow_action.get().strip(),
            )
            if not workflow.name:
                raise ValueError("Workflow name is required")
            crud.create_workflow(self.db, workflow, owner_id=1)
            self.refresh_workflows()
            self.workflow_name.set("")
            self.workflow_trigger.set("invoice_due")
            self.workflow_action.set("send_email")
            self.workflow_description.set("")
            messagebox.showinfo("Success", "Workflow created.")
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def on_close(self):
        self.db.close()
        self.destroy()


if __name__ == "__main__":
    app = BusinessDesktopApp()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
