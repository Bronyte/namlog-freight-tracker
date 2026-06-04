"""
NamLog Freight Tracker - Tkinter GUI
------------------------------------
This GUI follows the supplied NamLog wireframes and communicates with the Flask API
using requests. It does not access the database directly.

Expected API endpoints used by this GUI:
    GET     /api/trucks
    GET     /api/trucks/<id>
    POST    /api/trucks                  
    DELETE  /api/trucks/<id>
    GET     /api/deliveries              
    POST    /api/deliveries
    PUT     /api/deliveries/<id>

Run your Flask API first, then run:
    python gui.py
"""

from __future__ import annotations

import threading
from typing import Any, Callable

import requests
import tkinter as tk
from tkinter import ttk, messagebox


API_BASE_URL = "http://127.0.0.1:5000"
ADMIN_PASSWORD = "admin"


class NamLogGUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("NamLog Freight Tracker")
        self.geometry("1100x650")
        self.minsize(950, 580)
        self.configure(bg="#ff9fa3")

        self.role: str | None = None
        self.selected_delivery: dict[str, Any] | None = None
        self.selected_truck: dict[str, Any] | None = None

        self.colours = {
            "topbar": "#000000",
            "background": "#ff9fa3",
            "panel": "#d9d9d9",
            "button": "#cc0000",
            "button_hover": "#a80000",
            "text": "#111111",
            "white": "#ffffff",
            "success": "#168000",
        }

        self._configure_styles()
        self.show_login_options()

    def _configure_styles(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=self.colours["background"],
            fieldbackground=self.colours["background"],
            foreground=self.colours["text"],
            rowheight=34,
            font=("Arial", 12),
            borderwidth=0,
        )
        style.configure(
            "Treeview.Heading",
            background=self.colours["background"],
            foreground=self.colours["text"],
            font=("Arial", 13, "bold"),
            relief="flat",
        )
        style.map("Treeview", background=[("selected", "#f7c6c7")])

        style.configure(
            "TNotebook",
            background=self.colours["background"],
            borderwidth=0,
        )
        style.configure(
            "TNotebook.Tab",
            padding=(20, 8),
            font=("Arial", 11, "bold"),
        )

    def clear(self) -> None:
        for child in self.winfo_children():
            child.destroy()

    def make_topbar(self, parent: tk.Widget) -> None:
        tk.Frame(parent, bg=self.colours["topbar"], height=60).pack(fill="x", side="top")

    def red_button(self, parent: tk.Widget, text: str, command: Callable[[], None], width: int = 12) -> tk.Button:
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            width=width,
            bg=self.colours["button"],
            fg=self.colours["white"],
            activebackground=self.colours["button_hover"],
            activeforeground=self.colours["white"],
            relief="flat",
            font=("Arial", 12),
            cursor="hand2",
        )
        return btn

    def make_card(self, parent: tk.Widget, width: int = 430, height: int = 280) -> tk.Frame:
        card = tk.Frame(
            parent,
            bg=self.colours["panel"],
            width=width,
            height=height,
            highlightbackground="#777777",
            highlightthickness=1,
            bd=2,
            relief="raised",
        )
        card.pack_propagate(False)
        return card

    def api_call(
        self,
        method: str,
        endpoint: str,
        on_success: Callable[[Any], None],
        json_data: dict[str, Any] | None = None,
        expected_empty: bool = False,
    ) -> None:
        def worker() -> None:
            try:
                url = f"{API_BASE_URL}{endpoint}"
                response = requests.request(method, url, json=json_data, timeout=8)

                if response.status_code >= 400:
                    try:
                        error = response.json().get("error", response.text)
                    except ValueError:
                        error = response.text or f"HTTP {response.status_code}"
                    raise RuntimeError(error)

                if expected_empty or response.status_code == 204:
                    data: Any = None
                else:
                    data = response.json()

                self.after(0, lambda: on_success(data))
            except Exception as exc:
                error_message = str(exc)
                self.after(0, lambda: messagebox.showerror("API Error", error_message))

        threading.Thread(target=worker, daemon=True).start()


    def show_login_options(self) -> None:
        self.clear()
        self.make_topbar(self)

        body = tk.Frame(self, bg=self.colours["background"])
        body.pack(fill="both", expand=True)

        card = self.make_card(body, width=410, height=270)
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(card, text="NamLog", bg=self.colours["panel"], fg=self.colours["text"], font=("Arial", 22, "bold")).pack(pady=(55, 45))
        tk.Label(card, text="Please select your login option", bg=self.colours["panel"], fg=self.colours["text"], font=("Arial", 14)).pack()

        row = tk.Frame(card, bg=self.colours["panel"])
        row.pack(pady=22)
        self.red_button(row, "guest", lambda: self.enter_app("guest"), width=9).pack(side="left", padx=35)
        self.red_button(row, "admin", self.show_admin_login, width=9).pack(side="left", padx=35)

    def show_admin_login(self) -> None:
        self.clear()
        self.make_topbar(self)

        body = tk.Frame(self, bg=self.colours["background"])
        body.pack(fill="both", expand=True)

        card = self.make_card(body, width=450, height=330)
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            card,
            text="Admin Login",
            bg=self.colours["panel"],
            fg=self.colours["text"],
            font=("Arial", 16, "bold")
        ).pack(pady=(40, 20))

        tk.Label(
            card,
            text="Username:",
            bg=self.colours["panel"],
            fg=self.colours["text"],
            font=("Arial", 12)
        ).pack()

        username_entry = tk.Entry(
            card,
            width=24,
            font=("Arial", 14),
            bg=self.colours["background"],
            fg=self.colours["text"],
            relief="flat"
        )
        username_entry.pack(ipady=8, pady=(5, 15))

        tk.Label(
            card,
            text="Password:",
            bg=self.colours["panel"],
            fg=self.colours["text"],
            font=("Arial", 12)
        ).pack()

        password_entry = tk.Entry(
            card,
            show="*",
            width=24,
            font=("Arial", 14),
            bg=self.colours["background"],
            fg=self.colours["text"],
            relief="flat"
        )
        password_entry.pack(ipady=8, pady=(5, 20))

        username_entry.focus_set()

        def login() -> None:
            data = {
                "username": username_entry.get(),
                "password": password_entry.get(),
                "role": "admin"
            }

            self.api_call(
                "POST",
                "/api/login",
                lambda result: self.enter_app("admin"),
                data
            )

        row = tk.Frame(card, bg=self.colours["panel"])
        row.pack(pady=10)

        self.red_button(row, "back", self.show_login_options, width=10).pack(side="left", padx=38)
        self.red_button(row, "login", login, width=10).pack(side="left", padx=38)

        password_entry.bind("<Return>", lambda event: login())

    def enter_app(self, role: str) -> None:
        self.role = role
        self.show_dashboard()

    # ------------------------------------------------------------------
    # Main dashboard
    # ------------------------------------------------------------------
    def show_dashboard(self) -> None:
        self.clear()
        self.make_topbar(self)

        main = tk.Frame(self, bg=self.colours["background"])
        main.pack(fill="both", expand=True)

        header = tk.Frame(main, bg=self.colours["background"])
        header.pack(fill="x", padx=35, pady=(18, 5))
        tk.Label(header, text="NamLog Freight Tracker", bg=self.colours["background"], fg=self.colours["text"], font=("Arial", 20, "bold")).pack(side="left")
        self.red_button(header, "logout", self.show_login_options, width=9).pack(side="right")

        self.notebook = ttk.Notebook(main)
        self.notebook.pack(fill="both", expand=True, padx=35, pady=10)

        self.deliveries_frame = tk.Frame(self.notebook, bg=self.colours["background"])
        self.trucks_frame = tk.Frame(self.notebook, bg=self.colours["background"])

        self.notebook.add(self.deliveries_frame, text="Deliveries")
        self.notebook.add(self.trucks_frame, text="Trucks")

        self.build_deliveries_view()
        self.build_trucks_view()
        self.refresh_deliveries()
        self.refresh_trucks()

    # ------------------------------------------------------------------
    # Deliveries view
    # ------------------------------------------------------------------
    def build_deliveries_view(self) -> None:
        toolbar = tk.Frame(self.deliveries_frame, bg=self.colours["background"])
        toolbar.pack(fill="x", pady=(15, 12))
        self.red_button(toolbar, "refresh", self.refresh_deliveries, width=10).pack(side="left", padx=(0, 25))
        self.red_button(toolbar, "add", self.show_add_delivery_form, width=10).pack(side="left")

        self.delivery_stats = tk.Label(
            self.deliveries_frame,
            text="Total Delivered: 0        Total Pending: 0        Total Enroute: 0        Total: 0",
            bg=self.colours["panel"],
            fg=self.colours["text"],
            font=("Arial", 15),
            relief="solid",
            bd=1,
            pady=10,
        )
        self.delivery_stats.pack(fill="x", pady=(0, 14))

        table_panel = tk.Frame(self.deliveries_frame, bg=self.colours["panel"], bd=1, relief="solid")
        table_panel.pack(fill="both", expand=True)

        columns = ("id", "origin", "destination", "weight", "assigned_truck", "status", "action")
        self.delivery_tree = ttk.Treeview(table_panel, columns=columns, show="headings", height=10)
        headings = {
            "id": "ID",
            "origin": "Origin",
            "destination": "Destination",
            "weight": "Weight",
            "assigned_truck": "Assigned Truck",
            "status": "Status",
            "action": "double click to update",
        }
        widths = {"id": 80, "origin": 160, "destination": 160, "weight": 100, "assigned_truck": 180, "status": 130, "action": 120}
        for col in columns:
            self.delivery_tree.heading(col, text=headings[col])
            self.delivery_tree.column(col, width=widths[col], anchor="center")

        self.delivery_tree.pack(fill="both", expand=True, padx=18, pady=18)
        self.delivery_tree.bind("<Double-1>", lambda _event: self.show_update_delivery_form())
        self.delivery_tree.bind("<Return>", lambda _event: self.show_update_delivery_form())

    def refresh_deliveries(self) -> None:
        self.api_call("GET", "/api/deliveries", self.populate_deliveries)

    def populate_deliveries(self, deliveries: list[dict[str, Any]]) -> None:
        self.delivery_tree.delete(*self.delivery_tree.get_children())
        delivered = pending = enroute = 0

        for item in deliveries:
            status = str(item.get("status", "")).lower()
            if status == "delivered":
                delivered += 1
            elif status == "pending":
                pending += 1
            elif status in {"enroute", "in transit", "on route", "on_route"}:
                enroute += 1

            weight = item.get("weight") or item.get("weight_kg") or ""
            if isinstance(weight, (int, float)):
                weight = f"{weight:g} kg"

            truck = item.get("assigned_truck") or item.get("assigned_truck_id") or item.get("truck") or ""

            self.delivery_tree.insert(
                "",
                "end",
                values=(
                    item.get("id", ""),
                    item.get("origin", ""),
                    item.get("destination", ""),
                    weight,
                    truck,
                    item.get("status", ""),
                    "Update",
                ),
            )

        total = len(deliveries)
        self.delivery_stats.config(
            text=f"Total Delivered:  {delivered}        Total Pending: {pending}        Total Enroute: {enroute}        Total:  {total}"
        )

    def get_selected_delivery_id(self) -> int | None:
        selected = self.delivery_tree.selection()
        if not selected:
            messagebox.showinfo("Select delivery", "Please select a delivery first.")
            return None
        return int(self.delivery_tree.item(selected[0], "values")[0])

    def show_update_delivery_form(self) -> None:
        delivery_id = self.get_selected_delivery_id()
        if delivery_id is None:
            return
        self.api_call("GET", f"/api/deliveries/{delivery_id}", self.render_update_delivery_form)

    def render_update_delivery_form(self, delivery: dict[str, Any]) -> None:
        self.selected_delivery = delivery
        self.render_delivery_form(mode="update", data=delivery)

    def show_add_delivery_form(self) -> None:
        self.render_delivery_form(mode="add", data={})

    def render_delivery_form(self, mode: str, data: dict[str, Any]) -> None:
        win = tk.Toplevel(self)
        win.title("Update Delivery" if mode == "update" else "Add Delivery")
        win.geometry("520x420")
        win.configure(bg=self.colours["background"])
        win.transient(self)
        win.grab_set()

        card = self.make_card(win, width=420, height=330)
        card.place(relx=0.5, rely=0.5, anchor="center")

        fields = tk.Frame(card, bg=self.colours["panel"])
        fields.pack(pady=(28, 15))

        entries: dict[str, tk.Entry | ttk.Combobox] = {}

        def add_field(label: str, key: str, value: str = "") -> None:
            row = tk.Frame(fields, bg=self.colours["panel"])
            row.pack(fill="x", pady=5)
            tk.Label(row, text=label, width=16, anchor="e", bg=self.colours["panel"], font=("Arial", 13)).pack(side="left", padx=(0, 12))
            ent = tk.Entry(row, width=22, font=("Arial", 12), relief="flat")
            ent.pack(side="left", ipady=4)
            ent.insert(0, value)
            entries[key] = ent

        if mode == "update":
            tk.Label(fields, text=f"ID     {data.get('id', '')}", bg=self.colours["panel"], font=("Arial", 13)).pack(pady=2)

        add_field("Origin", "origin", str(data.get("origin", "")))
        add_field("Destination", "destination", str(data.get("destination", "")))
        add_field("Weight", "weight_kg", str(data.get("weight_kg", data.get("weight", ""))))
        add_field("Assigned Truck", "assigned_truck_id", str(data.get("assigned_truck_id", data.get("truck", ""))))

        row = tk.Frame(fields, bg=self.colours["panel"])
        row.pack(fill="x", pady=5)
        tk.Label(row, text="Status", width=16, anchor="e", bg=self.colours["panel"], font=("Arial", 13)).pack(side="left", padx=(0, 12))
        status_box = ttk.Combobox(row, width=20, values=("Pending", "Enroute", "Delivered", "Terminated"), state="readonly", font=("Arial", 12))
        status_box.pack(side="left", ipady=3)
        status_box.set(str(data.get("status", "Pending")))
        entries["status"] = status_box

        def save() -> None:
            payload = {
                "origin": entries["origin"].get(),
                "destination": entries["destination"].get(),
                "weight_kg": self._number_or_text(entries["weight_kg"].get()),
                "assigned_truck_id": self._number_or_text(entries["assigned_truck_id"].get()),
                "status": entries["status"].get(),
            }
            if mode == "update":
                endpoint = f"/api/deliveries/{data.get('id')}"
                self.api_call("PUT", endpoint, lambda _result: self._saved(win, self.refresh_deliveries), payload)
            else:
                self.api_call("POST", "/api/deliveries", lambda _result: self._saved(win, self.refresh_deliveries), payload)

        self.red_button(card, "save", save, width=10).pack(pady=(3, 0))

    # ------------------------------------------------------------------
    # Trucks view
    # ------------------------------------------------------------------
    def build_trucks_view(self) -> None:
        toolbar = tk.Frame(self.trucks_frame, bg=self.colours["background"])
        toolbar.pack(fill="x", pady=(15, 12))
        self.red_button(toolbar, "refresh", self.refresh_trucks, width=10).pack(side="left", padx=(0, 25))
        self.red_button(toolbar, "add", self.show_add_truck_form, width=10).pack(side="left", padx=(0, 25))
        self.red_button(toolbar, "delete selected", self.delete_selected_truck, width=14).pack(side="left")

        self.truck_stats = tk.Label(
            self.trucks_frame,
            text="Total Enroute: 0        Total Available: 0        Total: 0",
            bg=self.colours["panel"],
            fg=self.colours["text"],
            font=("Arial", 15),
            relief="solid",
            bd=1,
            pady=10,
        )
        self.truck_stats.pack(fill="x", pady=(0, 14))

        table_panel = tk.Frame(self.trucks_frame, bg=self.colours["panel"], bd=1, relief="solid")
        table_panel.pack(fill="both", expand=True)

        columns = ("id", "name", "location", "capacity", "registration", "available", "action")
        self.truck_tree = ttk.Treeview(table_panel, columns=columns, show="headings", height=10)
        headings = {
            "id": "ID",
            "name": "Name",
            "location": "Location",
            "capacity": "Cap.",
            "registration": "Registration",
            "available": "Available",
            "action": "Action",
        }
        widths = {"id": 80, "name": 160, "location": 180, "capacity": 110, "registration": 170, "available": 120, "action": 120}
        for col in columns:
            self.truck_tree.heading(col, text=headings[col])
            self.truck_tree.column(col, width=widths[col], anchor="center")

        self.truck_tree.pack(fill="both", expand=True, padx=18, pady=18)
        self.truck_tree.bind("<Double-1>", lambda _event: self.show_update_truck_form())
        self.truck_tree.bind("<Return>", lambda _event: self.show_update_truck_form())

    def refresh_trucks(self) -> None:
        self.api_call("GET", "/api/trucks", self.populate_trucks)

    def populate_trucks(self, trucks: list[dict[str, Any]]) -> None:
        self.truck_tree.delete(*self.truck_tree.get_children())
        available = enroute = 0

        for item in trucks:
            is_available = item.get("is_available", item.get("available", item.get("status", "")).__str__().lower() == "available")
            if bool(is_available):
                available += 1
            location = item.get("current_location", item.get("location", item.get("status", "")))
            if str(location).lower() in {"enroute", "in transit", "on route", "on_route"}:
                enroute += 1

            capacity = item.get("capacity_tonnes", item.get("capacity", ""))
            if isinstance(capacity, (int, float)):
                capacity = f"{capacity:g} Ton"

            self.truck_tree.insert(
                "",
                "end",
                values=(
                    item.get("id", ""),
                    item.get("name", ""),
                    location,
                    capacity,
                    item.get("registration", item.get("registration_number", "")),
                    str(bool(is_available)),
                    "Update",
                ),
            )

        self.truck_stats.config(text=f"Total Enroute:  {enroute}        Total Available:  {available}        Total:  {len(trucks)}")

    def get_selected_truck_id(self) -> int | None:
        selected = self.truck_tree.selection()
        if not selected:
            messagebox.showinfo("Select truck", "Please select a truck first.")
            return None
        return int(self.truck_tree.item(selected[0], "values")[0])

    def show_update_truck_form(self) -> None:
        truck_id = self.get_selected_truck_id()
        if truck_id is None:
            return
        self.api_call("GET", f"/api/trucks/{truck_id}", self.render_update_truck_form)

    def render_update_truck_form(self, truck: dict[str, Any]) -> None:
        self.render_truck_form(mode="update", data=truck)

    def show_add_truck_form(self) -> None:
        self.render_truck_form(mode="add", data={})

    def render_truck_form(self, mode: str, data: dict[str, Any]) -> None:
        win = tk.Toplevel(self)
        win.title("Update Truck" if mode == "update" else "Add Truck")
        win.geometry("520x420")
        win.configure(bg=self.colours["background"])
        win.transient(self)
        win.grab_set()

        card = self.make_card(win, width=430, height=330)
        card.place(relx=0.5, rely=0.5, anchor="center")
        fields = tk.Frame(card, bg=self.colours["panel"])
        fields.pack(pady=(35, 15))

        entries: dict[str, tk.Entry | ttk.Combobox] = {}

        if mode == "update":
            tk.Label(fields, text=f"ID     {data.get('id', '')}", bg=self.colours["panel"], font=("Arial", 13)).pack(pady=2)

        def add_field(label: str, key: str, value: str = "") -> None:
            row = tk.Frame(fields, bg=self.colours["panel"])
            row.pack(fill="x", pady=5)
            tk.Label(row, text=label, width=16, anchor="e", bg=self.colours["panel"], font=("Arial", 13)).pack(side="left", padx=(0, 12))
            ent = tk.Entry(row, width=22, font=("Arial", 12), relief="flat")
            ent.pack(side="left", ipady=4)
            ent.insert(0, value)
            entries[key] = ent

        add_field("Name", "name", str(data.get("name", "")))
        add_field("Location", "current_location", str(data.get("current_location", data.get("location", ""))))
        add_field("Capacity", "capacity_tonnes", str(data.get("capacity_tonnes", data.get("capacity", ""))))
        add_field("Registration", "registration", str(data.get("registration", data.get("registration_number", ""))))

        row = tk.Frame(fields, bg=self.colours["panel"])
        row.pack(fill="x", pady=5)
        tk.Label(row, text="Available", width=16, anchor="e", bg=self.colours["panel"], font=("Arial", 13)).pack(side="left", padx=(0, 12))
        available_box = ttk.Combobox(row, width=20, values=("True", "False"), state="readonly", font=("Arial", 12))
        available_box.pack(side="left", ipady=3)
        available_box.set(str(data.get("is_available", data.get("available", "True"))))
        entries["is_available"] = available_box

        def save() -> None:
            payload = {
                "name": entries["name"].get(),
                "current_location": entries["current_location"].get(),
                "capacity_tonnes": self._number_or_text(entries["capacity_tonnes"].get()),
                "registration": entries["registration"].get(),
                "registration_number": entries["registration"].get(),
                "is_available": entries["is_available"].get() == "True",
            }
            if mode == "update":
                # This endpoint is optional. Add it to api.py if you want truck editing.
                self.api_call("PUT", f"/api/trucks/{data.get('id')}", lambda _result: self._saved(win, self.refresh_trucks), payload)
            else:
                self.api_call("POST", "/api/trucks", lambda _result: self._saved(win, self.refresh_trucks), payload)

        self.red_button(card, "save", save, width=10).pack(pady=(3, 0))

    def delete_selected_truck(self) -> None:
        if self.role != "admin":
            messagebox.showerror("Permission denied", "Only admin users can delete trucks.")
            return
        truck_id = self.get_selected_truck_id()
        if truck_id is None:
            return
        if not messagebox.askyesno("Delete truck", f"Delete truck ID {truck_id}?"):
            return
        self.api_call("DELETE", f"/api/trucks/{truck_id}", lambda _result: self.refresh_trucks(), expected_empty=True)

    # ------------------------------------------------------------------
    # Shared helpers
    # ------------------------------------------------------------------
    def _number_or_text(self, value: str) -> Any:
        value = value.strip()
        if value == "":
            return value
        try:
            if "." in value:
                return float(value)
            return int(value)
        except ValueError:
            return value

    def _saved(self, window: tk.Toplevel, refresh_callback: Callable[[], None]) -> None:
        window.destroy()
        refresh_callback()
        messagebox.showinfo("Saved", "Record saved successfully.")

