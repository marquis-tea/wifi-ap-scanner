# ==========================================
# DEVELOPER: Member 1 (UI/Frontend)
# FILE: scanner_frontend.py
# DESCRIPTION: Fixed premium UI with custom cell bars and diagnostic dashboard.
# ==========================================

import tkinter as tk
from tkinter import ttk

class WifiScannerApp:
    def __init__(self, root, scan_callback):
        self.root = root
        self.root.title("Desktop Wi-Fi AP Scanner")
        self.root.geometry("900x580")
        self.root.configure(bg="#0F1016")  # Premium, ultra-dark obsidian background
        
        # Link the backend system callback
        self.scan_callback = scan_callback
        
        # --- UI Color Palette ---
        self.bg_dark = "#0F1016"
        self.card_bg = "#171923"
        self.accent_green = "#10B981"
        self.accent_blue = "#3B82F6"
        self.text_main = "#FFFFFF"
        self.text_muted = "#A0AEC0"
        
        # Configure the Advanced TTK Style Engine for custom table looks
        self.setup_styles()
        
        # 1. TOP HEADER DASHBOARD
        self.header_frame = tk.Frame(root, bg=self.bg_dark)
        self.header_frame.pack(fill="x", padx=35, pady=(30, 15))
        
        title_container = tk.Frame(self.header_frame, bg=self.bg_dark)
        title_container.pack(side="left")
        
        self.title_label = tk.Label(
            title_container, 
            text="NET-SCANNER // IO", 
            font=("Consolas", 22, "bold"), 
            bg=self.bg_dark, 
            fg=self.accent_blue
        )
        self.title_label.pack(anchor="w")
        
        self.status_label = tk.Label(
            title_container,
            text="System core active. Ready for hardware query.",
            font=("Segoe UI", 10),
            bg=self.bg_dark,
            fg=self.text_muted
        )
        self.status_label.pack(anchor="w", pady=(2, 0))
        
        # Futuristic Cyberpunk Style Action Button (Fixed layout bug)
        self.scan_button = tk.Button(
            self.header_frame, 
            text="⚡ INITIALIZE SCAN", 
            font=("Segoe UI Black", 11), 
            command=self.run_scan, 
            bg=self.accent_green, 
            fg="#000000",
            activebackground="#059669",
            activeforeground="#000000",
            bd=0,
            cursor="hand2",
            padx=25, 
            pady=10,
            relief="flat"
        )
        self.scan_button.pack(side="right", pady=5)

        # 2. MINI METRIC DASHBOARD CARDS
        self.metrics_frame = tk.Frame(root, bg=self.bg_dark)
        self.metrics_frame.pack(fill="x", padx=35, pady=(0, 20))
        
        self.card_total = self.create_metric_card(self.metrics_frame, "TOTAL APs", "0", self.accent_blue)
        self.card_secure = self.create_metric_card(self.metrics_frame, "SECURE NETWORKS", "0", self.accent_green)
        self.card_best = self.create_metric_card(self.metrics_frame, "BEST SIGNAL", "N/A", "#8B5CF6")

        # 3. MAIN DATA TABLE AREA WITH GRAPHICS CONTAINER
        self.table_container = tk.Frame(root, bg=self.card_bg, bd=1, highlightbackground="#2D3748", highlightthickness=1)
        self.table_container.pack(fill="both", expand=True, padx=35, pady=(0, 30))
        
        self.columns = ("ssid", "bssid", "rssi_val", "rssi_graph", "channel", "security")
        self.tree = ttk.Treeview(self.table_container, columns=self.columns, show="headings")
        
        # Custom Column Formatting with exact Width Alignments
        self.tree.heading("ssid", text="SSID (Network Broadcast Name)")
        self.tree.heading("bssid", text="BSSID (MAC)")
        self.tree.heading("rssi_val", text="Signal")
        self.tree.heading("rssi_graph", text="Signal Visual Meter")
        self.tree.heading("channel", text="CH")
        self.tree.heading("security", text="Encryption")
        
        self.tree.column("ssid", width=240, anchor="w")
        self.tree.column("bssid", width=140, anchor="center")
        self.tree.column("rssi_val", width=80, anchor="center")
        self.tree.column("rssi_graph", width=160, anchor="w")  # Visual meter space
        self.tree.column("channel", width=50, anchor="center")
        self.tree.column("security", width=110, anchor="center")
        
        self.scrollbar = ttk.Scrollbar(self.table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def setup_styles(self):
        """Builds an absolute premium custom design configuration for the standard tables."""
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure(
            "Treeview",
            background=self.card_bg,
            foreground="#E2E8F0",
            rowheight=42,  # Wide spacing for modern UI breathing room
            fieldbackground=self.card_bg,
            font=("Segoe UI", 10),
            borderwidth=0
        )
        style.map("Treeview", background=[("selected", "#2A4365")], foreground=[("selected", "#FFFFFF")])
        
        style.configure(
            "Treeview.Heading",
            background="#1A202C",
            foreground="#EDF2F7",
            font=("Segoe UI Semibold", 10),
            padding=(12, 10),
            borderwidth=0
        )
        style.map("Treeview.Heading", background=[("active", "#2D3748")])

    def create_metric_card(self, parent, label_text, initial_val, accent_color):
        """Generates dynamic dashboard analytical metrics counters."""
        card = tk.Frame(parent, bg=self.card_bg, bd=1, highlightbackground="#2D3748", highlightthickness=1)
        card.pack(side="left", fill="x", expand=True, padx=(0, 15) if label_text != "BEST SIGNAL" else 0)
        
        lbl = tk.Label(card, text=label_text, font=("Segoe UI Bold", 9), bg=self.card_bg, fg=self.text_muted)
        lbl.pack(anchor="w", padx=15, pady=(12, 2))
        
        val_lbl = tk.Label(card, text=initial_val, font=("Consolas", 18, "bold"), bg=self.card_bg, fg=accent_color)
        val_lbl.pack(anchor="w", padx=15, pady=(0, 12))
        
        return val_lbl

    def generate_signal_bar(self, rssi):
        """Converts raw dBm metrics into highly illustrative structural text meters."""
        # Convert RSSI range (~ -100 to -30) into a percentage visual scale
        percentage = max(0, min(100, 2 * (rssi + 100)))
        bar_count = int(percentage / 10)
        
        # Construct cellular-like ascending text signal bars
        filled_bars = "█" * bar_count
        empty_bars = "░" * (10 - bar_count)
        
        if rssi >= -55:
            color_theme = "🟢 Good"
        elif rssi >= -75:
            color_theme = "🟡 Med"
        else:
            color_theme = "🔴 Low"
            
        return f"{filled_bars}{empty_bars} {color_theme}"

    def run_scan(self):
        """Triggers system communication routines cleanly with complete UI visual adjustments."""
        self.scan_button.configure(state="disabled", text="⚡ CORES ACTIVE...", bg="#2D3748", fg=self.text_muted)
        self.status_label.configure(text="Probing wireless environments and updating network registries...", fg=self.accent_blue)
        self.root.update_idletasks()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Standard isolated System Call mapping tracking team architectures
        networks = self.scan_callback()
        
        secure_count = 0
        best_rssi = -100
        best_ssid = "None"
        
        for net in networks:
            rssi_val = net['rssi']
            security = net['security']
            ssid = net['ssid'] if net['ssid'] else "<Hidden Frame Beacon>"
            
            # Calculate dynamic parameters to populate live metric display cards
            if security != "Open":
                secure_count += 1
            if rssi_val > best_rssi:
                best_rssi = rssi_val
                best_ssid = ssid if len(ssid) <= 12 else f"{ssid[:10]}..."
                
            # Render visually striking graphic representations
            signal_meter = self.generate_signal_bar(rssi_val)
            
            self.tree.insert("", "end", values=(
                ssid, 
                net['bssid'].upper(), 
                f"{rssi_val} dBm",
                signal_meter, 
                net['channel'], 
                f"🛡️ {security}" if security != "Open" else "🔓 Open"
            ))
            
        # Re-update Dashboard Card States Live
        self.card_total.configure(text=str(len(networks)))
        self.card_secure.configure(text=str(secure_count))
        self.card_best.configure(text=f"{best_ssid} ({best_rssi}dBm)")
        
        # Unlock Button Element and finalize UI render state
        self.scan_button.configure(state="normal", text="⚡ INITIALIZE SCAN", bg=self.accent_green, fg="#000000")
        self.status_label.configure(text="Scan sequence absolute. Display registers completely populated.", fg=self.accent_green)