import tkinter as tk
from tkinter import ttk, messagebox
from playwright.sync_api import sync_playwright, TimeoutError

from scanner.dom_hidden import scan_dom_hidden
from scanner.angular_scope import scan_angular_permissions
from scanner.network_permissions import attach_network_listener


class NgXrayUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NgX-Ray")
        self.root.geometry("1000x650")

        self.hidden_data = []
        self.angular_data = []
        self.network_data = []

        self.build_ui()

    def build_ui(self):
        # URL input
        top = ttk.Frame(self.root)
        top.pack(fill="x", padx=8, pady=5)

        ttk.Label(top, text="URL:").pack(side="left")
        self.url_var = tk.StringVar()
        ttk.Entry(top, textvariable=self.url_var, width=70).pack(side="left", padx=5)
        ttk.Button(top, text="Scan", command=self.run_scan).pack(side="left")

        # Search bar
        search_frame = ttk.Frame(self.root)
        search_frame.pack(fill="x", padx=8, pady=5)

        ttk.Label(search_frame, text="Live Search:").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self.refresh_tabs())
        ttk.Entry(search_frame, textvariable=self.search_var, width=50).pack(side="left", padx=5)

        # Notebook tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)
        self.notebook.bind("<<NotebookTabChanged>>", lambda _: self.refresh_tabs())

        # Tabs
        self.hidden_tab = ttk.Frame(self.notebook)
        self.angular_tab = ttk.Frame(self.notebook)
        self.network_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.hidden_tab, text="Hidden Elements")
        self.notebook.add(self.angular_tab, text="Angular Permissions")
        self.notebook.add(self.network_tab, text="Network Permissions")

        # Trees
        self.hidden_tree = self.create_tree(self.hidden_tab, ["tag", "id", "qa-id", "ngShow", "ngIf", "reasons"])
        self.angular_tree = self.create_tree(self.angular_tab, ["tag", "qa-id", "ngShow", "ngIf", "permissions"])
        self.network_tree = self.create_tree(self.network_tab, ["url", "path", "value", "type"])

    def create_tree(self, parent, columns):
        tree = ttk.Treeview(parent, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200, anchor="w")
        tree.pack(fill="both", expand=True)
        return tree

    # ──────────────────────────── SCAN ────────────────────────────

    def run_scan(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("NgX-Ray", "Please enter a URL.")
            return

        self.hidden_data = []
        self.angular_data = []
        self.network_data = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            ctx = browser.new_context()
            page = ctx.new_page()

            attach_network_listener(page, self.network_data)

            page.goto(url)
            messagebox.showinfo("NgX-Ray", "Login if needed, navigate to page, then press OK.")

            try:
                page.wait_for_load_state("networkidle", timeout=15000)
            except TimeoutError:
                pass

            self.hidden_data = scan_dom_hidden(page)
            self.angular_data = scan_angular_permissions(page)

            browser.close()

        self.refresh_tabs()
        messagebox.showinfo("NgX-Ray", "Scan complete.")

    # ─────────────────────────── REFRESH ───────────────────────────

    def refresh_tabs(self):
        tab = self.notebook.index(self.notebook.select())
        search = (self.search_var.get() or "").lower()

        if tab == 0:
            self.populate_hidden(search)
        elif tab == 1:
            self.populate_angular(search)
        elif tab == 2:
            self.populate_network(search)

    def populate_hidden(self, search):
        self.hidden_tree.delete(*self.hidden_tree.get_children())
        for item in self.hidden_data:
            if search not in str(item).lower():
                continue
            self.hidden_tree.insert("", "end", values=[
                item.get("tag"), item.get("id"), item.get("dataQaId"),
                item.get("ngShow"), item.get("ngIf"),
                ", ".join(item.get("hiddenReasons") or [])
            ])

    def populate_angular(self, search):
        self.angular_tree.delete(*self.angular_tree.get_children())
        for item in self.angular_data:
            perms = "; ".join(f"{p['path']}={p['value']}" for p in item.get("permissions", []))
            block = (perms + str(item.get("ngShow")) + str(item.get("ngIf"))).lower()
            if search not in block:
                continue
            self.angular_tree.insert("", "end", values=[
                item.get("tag"), item.get("dataQaId"),
                item.get("ngShow"), item.get("ngIf"), perms
            ])

    def populate_network(self, search):
        self.network_tree.delete(*self.network_tree.get_children())
        for item in self.network_data:
            block = f"{item['url']} {item['path']} {item['value']}".lower()
            if search not in block:
                continue
            self.network_tree.insert("", "end", values=[
                item["url"], item["path"], str(item["value"]), item["type"]
            ])
