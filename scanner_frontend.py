import tkinter as tk
from tkinter import ttk
import random
import time

# --- COLOR PALETTE (Modern Premium Dark Theme) ---
BG_COLOR = "#121212"          # Deep dark background
CARD_BG = "#1e1e1e"           # Slightly lighter dark container background
ACCENT_COLOR = "#10b981"      # Emerald / Teal green (primary focus indicator)
TEXT_PRIMARY = "#ffffff"      # Crisp white for main text
TEXT_SECONDARY = "#9ca3af"    # Muted gray for subtitles & secondary details
HIGHLIGHT_BG = "#2a2a2a"      # Hover/selection background
BORDER_COLOR = "#374151"      # Dark border lines
STATUS_GREEN = "#10b981"
STATUS_RED = "#ef4444"

class WiFiScannerFrontend:
    def __init__(self, root):
        self.root = root
        self.root.title("TWC6323 - Mobile & Wireless WiFi AP Scanner")
        self.root.geometry("900x600")
        self.root.configure(bg=BG_COLOR)
        self.root.minsize(800, 500)
        
        # Keep track of all scanned items for active search/filtering
        self.all_networks = []
        self.is_scanning = False
        
        # Configure custom modern styles
        self.setup_styles()
        
        # Build the entire application layout
        self.create_layout()
        
        # Load some initial mock items to show how it looks on launch
        self.load_sample_data()

    def setup_styles(self):
        """Configure ttk styles to modern dark-theme aesthetics"""
        self.style = ttk.Style()
        # Use 'clam' as it allows deep style override
        self.style.theme_use('clam')
        
        # Frame styles
        self.style.configure("TFrame", background=BG_COLOR)
        self.style.configure("Card.TFrame", background=CARD_BG, borderwidth=1, relief="flat")
        
        # Label styles
        self.style.configure("TLabel", background=BG_COLOR, foreground=TEXT_PRIMARY, font=("Segoe UI", 10))
        self.style.configure("Title.TLabel", background=BG_COLOR, foreground=TEXT_PRIMARY, font=("Segoe UI", 18, "bold"))
        self.style.configure("Subtitle.TLabel", background=BG_COLOR, foreground=TEXT_SECONDARY, font=("Segoe UI", 9))
        
        self.style.configure("CardTitle.TLabel", background=CARD_BG, foreground=TEXT_SECONDARY, font=("Segoe UI", 9, "bold"))
        self.style.configure("CardValue.TLabel", background=CARD_BG, foreground=ACCENT_COLOR, font=("Segoe UI", 16, "bold"))
        
        # Button styles
        self.style.configure("Scan.TButton", 
                             background=ACCENT_COLOR, 
                             foreground="#121212", 
                             font=("Segoe UI", 10, "bold"), 
                             borderwidth=0, 
                             focuscolor=ACCENT_COLOR)
        self.style.map("Scan.TButton",
                       background=[("active", "#34d399"), ("disabled", "#374151")],
                       foreground=[("disabled", "#9ca3af")])
        
        # Entry (Search box)
        self.style.configure("TEntry", 
                             fieldbackground=CARD_BG, 
                             foreground=TEXT_PRIMARY, 
                             bordercolor=BORDER_COLOR, 
                             lightcolor=BORDER_COLOR, 
                             darkcolor=BORDER_COLOR,
                             insertcolor=TEXT_PRIMARY)
        
        # Treeview (Main Results Table) Styling
        self.style.configure("Treeview", 
                             background=CARD_BG, 
                             fieldbackground=CARD_BG, 
                             foreground=TEXT_PRIMARY, 
                             rowheight=35, 
                             font=("Segoe UI", 10),
                             borderwidth=0)
        self.style.map("Treeview", 
                       background=[("selected", HIGHLIGHT_BG)], 
                       foreground=[("selected", ACCENT_COLOR)])
        
        # Treeview Header Styling
        self.style.configure("Treeview.Heading", 
                             background=BORDER_COLOR, 
                             foreground=TEXT_PRIMARY, 
                             font=("Segoe UI", 9, "bold"), 
                             borderwidth=0,
                             relief="flat")
        self.style.map("Treeview.Heading", 
                       background=[("active", HIGHLIGHT_BG)])

        # Progressbar styling
        self.style.configure("Scan.Horizontal.TProgressbar", 
                             troughcolor=CARD_BG, 
                             background=ACCENT_COLOR, 
                             thickness=6, 
                             borderwidth=0)

    def create_layout(self):
        """Draws the clean, structural responsive layouts"""
        
        # --- HEADER REGION ---
        header_frame = ttk.Frame(self.root, style="TFrame")
        header_frame.pack(fill="x", padx=25, pady=(20, 10))
        
        title_label = ttk.Label(header_frame, text="wifi-ap-scanner", style="Title.TLabel")
        title_label.pack(anchor="w")
        
        subtitle_text = "TWC6323 - Mobile and Wireless Communications Project | Dev: HACHIMI/MEGAT/AIDEL/SAHIL"
        subtitle_label = ttk.Label(header_frame, text=subtitle_text, style="Subtitle.TLabel")
        subtitle_label.pack(anchor="w", pady=(2, 0))
        
        # Divider Line
        divider = tk.Frame(self.root, height=1, bg=BORDER_COLOR)
        divider.pack(fill="x", padx=25, pady=(5, 15))
        
        # --- TOP CONTROL & KPIS ---
        control_frame = ttk.Frame(self.root, style="TFrame")
        control_frame.pack(fill="x", padx=25, pady=5)
        
        # KPI Card 1: Total APs Detected
        self.kpi_total_frame = ttk.Frame(control_frame, style="Card.TFrame", padding=10)
        self.kpi_total_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        ttk.Label(self.kpi_total_frame, text="TOTAL APs DETECTED", style="CardTitle.TLabel").pack(anchor="w")
        self.lbl_kpi_total = ttk.Label(self.kpi_total_frame, text="0", style="CardValue.TLabel")
        self.lbl_kpi_total.pack(anchor="w", pady=(5, 0))
        
        # KPI Card 2: Secured Networks
        self.kpi_secure_frame = ttk.Frame(control_frame, style="Card.TFrame", padding=10)
        self.kpi_secure_frame.pack(side="left", fill="both", expand=True, padx=10)
        ttk.Label(self.kpi_secure_frame, text="SECURE NETWORKS (WPA2/WPA3)", style="CardTitle.TLabel").pack(anchor="w")
        self.lbl_kpi_secure = ttk.Label(self.kpi_secure_frame, text="0", style="CardValue.TLabel")
        self.lbl_kpi_secure.pack(anchor="w", pady=(5, 0))
        
        # KPI Card 3: Strongest Signal Match
        self.kpi_signal_frame = ttk.Frame(control_frame, style="Card.TFrame", padding=10)
        self.kpi_signal_frame.pack(side="left", fill="both", expand=True, padx=(10, 0))
        ttk.Label(self.kpi_signal_frame, text="STRONGEST SIGNAL", style="CardTitle.TLabel").pack(anchor="w")
        self.lbl_kpi_signal = ttk.Label(self.kpi_signal_frame, text="N/A", style="CardValue.TLabel")
        self.lbl_kpi_signal.pack(anchor="w", pady=(5, 0))
        
        # --- ACTION PANEL (Buttons & Search bar) ---
        action_frame = ttk.Frame(self.root, style="TFrame")
        action_frame.pack(fill="x", padx=25, pady=(20, 10))
        
        self.btn_scan = ttk.Button(action_frame, text="⚡ START SCAN", style="Scan.TButton", command=self.trigger_scan, width=15)
        self.btn_scan.pack(side="left")
        
        # Search Filtering Elements
        search_lbl = ttk.Label(action_frame, text="Filter Results:", style="Subtitle.TLabel")
        search_lbl.pack(side="left", padx=(25, 5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self.filter_results)
        self.search_entry = ttk.Entry(action_frame, textvariable=self.search_var, width=30, style="TEntry")
        self.search_entry.pack(side="left")
        
        # Clear filter button
        self.btn_clear_search = tk.Button(action_frame, text="✕", bg=CARD_BG, fg=TEXT_SECONDARY, 
                                          activebackground=HIGHLIGHT_BG, activeforeground=TEXT_PRIMARY,
                                          bd=0, relief="flat", cursor="hand2", command=self.clear_search, padx=8)
        self.btn_clear_search.pack(side="left", padx=(5, 0))
        
        # Interface Picker (Mock Dropdown)
        ttk.Label(action_frame, text="Interface:", style="Subtitle.TLabel").pack(side="right", padx=(0, 5))
        self.interface_combobox = ttk.Combobox(action_frame, values=["wlan0 (Internal)", "wlan1 (External USB)"], state="readonly", width=22)
        self.interface_combobox.set("wlan0 (Internal)")
        self.interface_combobox.pack(side="right", padx=(0, 10))
        
        # --- THE RESULTS GRID (Treeview) ---
        grid_container = ttk.Frame(self.root, style="Card.TFrame", padding=1)
        grid_container.pack(fill="both", expand=True, padx=25, pady=(10, 5))
        
        columns = ("ssid", "bssid", "rssi", "channel", "frequency", "security", "signal_bar")
        self.tree = ttk.Treeview(grid_container, columns=columns, show="headings", selectmode="browse")
        
        # Scrollbars
        scrollbar_y = ttk.Scrollbar(grid_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        
        # Set up headers with sorting functionality
        self.tree.heading("ssid", text="SSID ↕", command=lambda: self.sort_column("ssid", False))
        self.tree.heading("bssid", text="BSSID (MAC Address)", command=lambda: self.sort_column("bssid", False))
        self.tree.heading("rssi", text="RSSI (dBm) ↕", command=lambda: self.sort_column("rssi", False))
        self.tree.heading("channel", text="CH ↕", command=lambda: self.sort_column("channel", False))
        self.tree.heading("frequency", text="Band", command=lambda: self.sort_column("frequency", False))
        self.tree.heading("security", text="Security Protocol", command=lambda: self.sort_column("security", False))
        self.tree.heading("signal_bar", text="Signal Index", command=lambda: self.sort_column("signal_bar", False))
        
        # Column width assignments & layout
        self.tree.column("ssid", width=180, minwidth=120, anchor="w")
        self.tree.column("bssid", width=150, minwidth=130, anchor="center")
        self.tree.column("rssi", width=100, minwidth=80, anchor="center")
        self.tree.column("channel", width=60, minwidth=50, anchor="center")
        self.tree.column("frequency", width=80, minwidth=70, anchor="center")
        self.tree.column("security", width=160, minwidth=130, anchor="w")
        self.tree.column("signal_bar", width=100, minwidth=90, anchor="center")
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        
        # --- SCAN PROGRESS ELEMENT ---
        self.progress_bar = ttk.Progressbar(self.root, style="Scan.Horizontal.TProgressbar", mode="determinate")
        self.progress_bar.pack(fill="x", padx=25, pady=5)
        
        # --- FOOTER STATUS STRIP ---
        status_strip = tk.Frame(self.root, height=30, bg=CARD_BG)
        status_strip.pack(fill="x", side="bottom")
        
        self.lbl_status = tk.Label(status_strip, text="● Interface idle. Ready to analyze workspace.", 
                                   bg=CARD_BG, fg=TEXT_SECONDARY, font=("Segoe UI", 9))
        self.lbl_status.pack(side="left", padx=25, pady=5)
        
        self.lbl_system = tk.Label(status_strip, text="Front-End Engine Mode: Demo/Sandbox active", 
                                   bg=CARD_BG, fg=TEXT_SECONDARY, font=("Segoe UI", 9))
        self.lbl_system.pack(side="right", padx=25, pady=5)

    def load_sample_data(self):
        """Loads default realistic networking items so the user interface isn't bare on run"""
        self.all_networks = [
            {"ssid": "UTeM_WiFi_Secure", "bssid": "A4:93:3F:8B:12:0A", "rssi": -42, "channel": 6, "frequency": "2.4 GHz", "security": "WPA3-Enterprise", "signal_bar": "█████ (Excellent)"},
            {"ssid": "CelcomHome_5G_Ext", "bssid": "C0:06:C3:FF:1E:E2", "rssi": -55, "channel": 149, "frequency": "5.0 GHz", "security": "WPA2-PSK (AES)", "signal_bar": "████░ (Very Good)"},
            {"ssid": "Coffee_Shop_Guest", "bssid": "8C:11:0C:6D:4C:D4", "rssi": -72, "channel": 11, "frequency": "2.4 GHz", "security": "WEP / Open Network", "signal_bar": "██░░░ (Weak)"},
            {"ssid": "HACHIMI_PersonalHotspot", "bssid": "9E:F2:B1:33:AA:99", "rssi": -30, "channel": 36, "frequency": "5.0 GHz", "security": "WPA3-Personal", "signal_bar": "█████ (Excellent)"}
        ]
        self.update_tree_view(self.all_networks)

    def trigger_scan(self):
        """Disables controls, animates a mock real-time spectrum scanning, and populates randomized real networks"""
        if self.is_scanning:
            return
            
        self.is_scanning = True
        self.btn_scan.configure(state="disabled")
        self.interface_combobox.configure(state="disabled")
        self.search_entry.configure(state="disabled")
        self.lbl_status.configure(text="● Initializing receiver card... scanning channels...", fg=ACCENT_COLOR)
        
        self.all_networks = []
        self.update_tree_view([])
        self.progress_bar["value"] = 0
        
        # Stepwise animation timeline simulation
        self.simulate_scan_progress(0)

    def simulate_scan_progress(self, current_step):
        if current_step <= 100:
            self.progress_bar["value"] = current_step
            self.lbl_status.configure(text=f"● Actively scanning spectrum... Channel {int(current_step/8) + 1}/13 - Progress: {current_step}%")
            
            # Slow and fast variable jumps for looking organic
            delay = random.randint(30, 150)
            self.root.after(delay, lambda: self.simulate_scan_progress(current_step + random.randint(4, 10)))
        else:
            self.complete_scan()

    def complete_scan(self):
        """Generates rich, randomized, and authentic networks after loading completes"""
        self.progress_bar["value"] = 100
        self.is_scanning = False
        
        # Populate clean mock data representing actual devices
        ssids = ["UTeM_Campus", "Celcom_Guest", "Maxis_Home_40A2", "Unifi_My_Playground", "Intel_Internal_Dev", 
                 "Direct-SmartTV", "Starbucks_Open_WiFi", "TP-Link_AP_7820", "HACHIMI_Hotspot_5G", "Huawei_P40_Pro"]
        
        securities = ["WPA3-Personal", "WPA2-PSK (AES)", "WPA2/WPA3-Enterprise", "WEP / Open Network", "WPA-PSK (TKIP)"]
        
        for i in range(random.randint(6, 15)):
            rssi = random.randint(-90, -30)
            
            # Choose a consistent representation of frequency & channel
            freq_choice = random.choice(["2.4 GHz", "5.0 GHz"])
            if freq_choice == "2.4 GHz":
                channel = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 13])
            else:
                channel = random.choice([36, 40, 44, 48, 149, 153, 161])
                
            # Define graphical signals based on DBm
            if rssi >= -50:
                sig_bar = "█████ (Excellent)"
            elif rssi >= -65:
                sig_bar = "████░ (Very Good)"
            elif rssi >= -75:
                sig_bar = "███░░ (Good)"
            elif rssi >= -85:
                sig_bar = "██░░░ (Weak)"
            else:
                sig_bar = "█░░░░ (Very Poor)"

            # Construct MAC address structure
            bssid = ":".join(f"{random.randint(0, 255):02X}" for _ in range(6))
            
            self.all_networks.append({
                "ssid": random.choice(ssids) if random.random() > 0.1 else f"Hidden Network SSID ({i})",
                "bssid": bssid,
                "rssi": rssi,
                "channel": channel,
                "frequency": freq_choice,
                "security": random.choice(securities),
                "signal_bar": sig_bar
            })
            
        # Re-sort list based on RSSI strength (strongest first) as default sorting behaviour
        self.all_networks.sort(key=lambda x: x["rssi"], reverse=True)
        
        # Update user elements
        self.update_tree_view(self.all_networks)
        
        self.btn_scan.configure(state="normal")
        self.interface_combobox.configure(state="readonly")
        self.search_entry.configure(state="normal")
        self.lbl_status.configure(text=f"● Scan Success. Found {len(self.all_networks)} Active Transmitting Devices.", fg=STATUS_GREEN)

    def update_tree_view(self, dataset):
        """Clears and re-inserts a dataset into the UI table grid and refreshes KPIs"""
        self.tree.delete(*self.tree.get_children())
        
        secured_count = 0
        strongest_val = -100
        
        for item in dataset:
            self.tree.insert("", "end", values=(
                item["ssid"],
                item["bssid"],
                f"{item['rssi']} dBm",
                item["channel"],
                item["frequency"],
                item["security"],
                item["signal_bar"]
            ))
            
            # Count secured networks
            if "Open" not in item["security"]:
                secured_count += 1
                
            # Track strongest RSSI
            if item["rssi"] > strongest_val:
                strongest_val = item["rssi"]
                
        # Format and apply dashboard KPIs
        self.lbl_kpi_total.configure(text=str(len(dataset)))
        self.lbl_kpi_secure.configure(text=str(secured_count))
        
        if len(dataset) > 0:
            self.lbl_kpi_signal.configure(text=f"{strongest_val} dBm")
        else:
            self.lbl_kpi_signal.configure(text="N/A")

    def filter_results(self, *args):
        """Dynamically filters the current view based on user string query"""
        query = self.search_var.get().lower()
        if not query:
            self.update_tree_view(self.all_networks)
            return
            
        filtered = [item for item in self.all_networks if query in item["ssid"].lower() or query in item["security"].lower() or query in item["bssid"].lower()]
        self.update_tree_view(filtered)

    def clear_search(self):
        self.search_var.set("")

    def sort_column(self, col, reverse):
        """Handles columns clicking to sort content dynamically"""
        # Get list values
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        
        # Extract numerical integer for DBm values/Channel levels if comparing those columns
        if col == "rssi":
            # Strip " dBm" string before sorting
            l.sort(key=lambda t: int(t[0].split()[0]), reverse=not reverse)
        elif col == "channel":
            l.sort(key=lambda t: int(t[0]), reverse=reverse)
        else:
            l.sort(reverse=reverse)

        # Rearrange elements in DOM tree
        for index, (val, k) in enumerate(l):
            self.tree.move(k, "", index)
            
        # Swap heading command trigger parameter for alternate toggles
        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))

if __name__ == "__main__":
    root = tk.Tk()
    app = WiFiScannerFrontend(root)
    root.mainloop()