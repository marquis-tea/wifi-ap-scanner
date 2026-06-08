# ==========================================
# FILE: main.py
# DESCRIPTION: The main entry point linking frontend and backend.
# ==========================================

import tkinter as tk
from scanner_backend import get_wifi_networks
from scanner_frontend import WifiScannerApp

def main():
    # Initialize the core Tkinter window engine
    root = tk.Tk()
    
    # Launch the UI, passing the backend scanning function as a tool for the UI to use
    app = WifiScannerApp(root, scan_callback=get_wifi_networks)
    
    # Keep the window running until closed
    root.mainloop()

if __name__ == "__main__":
    main()