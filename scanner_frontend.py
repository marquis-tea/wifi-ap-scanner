# ==========================================
# DEVELOPER: Member 1 (UI/Frontend)
# FILE: scanner_frontend.py
# DESCRIPTION: Handles the graphical user interface.
# ==========================================

import tkinter as tk
from tkinter import ttk

class WifiScannerApp:
    def __init__(self, root, scan_callback):
        self.root = root
        self.root.title("Desktop Wi-Fi AP Scanner")
        self.root.geometry("700x400")
        
        # Store the backend function passed from main.py
        self.scan_callback = scan_callback
        
        # 1. Create Title Label
        self.title_label = tk.Label(root, text="Wireless Access Point Scanner", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)
        
        # 2. Create the "Scan" Button
        self.scan_button = tk.Button(root, text="Scan Networks", font=("Arial", 11), command=self.run_scan, bg="#4CAF50", fg="white", padx=10, pady=5)
        self.scan_button.pack(pady=10)
        
        # 3. Create a Table (Treeview) to present Wi-Fi info clearly
        self.columns = ("ssid", "bssid", "rssi", "channel", "security")
        self.tree = ttk.Treeview(root, columns=self.columns, show="headings")
        
        # Define headings
        self.tree.heading("ssid", text="SSID (Network Name)")
        self.tree.heading("bssid", text="BSSID (MAC Address)")
        self.tree.heading("rssi", text="Signal Strength (RSSI)")
        self.tree.heading("channel", text="Channel")
        self.tree.heading("security", text="Security Type")
        
        # Column widths
        self.tree.column("ssid", width=180)
        self.tree.column("bssid", width=140)
        self.tree.column("rssi", width=130, anchor="center")
        self.tree.column("channel", width=80, anchor="center")
        self.tree.column("security", width=100, anchor="center")
        
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)

    def run_scan(self):
        """Triggers when the user clicks 'Scan Networks'."""
        # Clear existing rows in the table
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Call the backend script to fetch current networks
        networks = self.scan_callback()
        
        # Insert new data rows into the table
        for net in networks:
            # Format RSSI values visually to make it user-friendly
            rssi_str = f"{net['rssi']} dBm"
            
            self.tree.insert("", "end", values=(
                net['ssid'], 
                net['bssid'], 
                rssi_str, 
                net['channel'], 
                net['security']
            ))