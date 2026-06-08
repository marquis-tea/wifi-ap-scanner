# ==========================================
# DEVELOPER: Member 2 (Systems/Backend)
# FILE: scanner_backend.py
# DESCRIPTION: Handles communication with wireless hardware.
# ==========================================

import time
# import pywifi  # Un-comment this once pywifi is installed via pip

def get_wifi_networks():
    """
    Scans the air for Wi-Fi access points and returns a list of dictionaries.
    Currently uses mock data for safe initial development.
    """
    
    # TODO: Member 2 will implement real pywifi code here.
    # Example flow: 
    # wifi = pywifi.PyWiFi()
    # iface = wifi.interfaces()[0]
    # iface.scan()
    # time.sleep(2)
    # results = iface.scan_results()
    
    # Mock data for frontend testing
    mock_scan_results = [
        {"ssid": "Home_WiFi_2.4G", "bssid": "AA:BB:CC:DD:EE:01", "rssi": -45, "channel": 1, "security": "WPA2"},
        {"ssid": "Neighbour_Network", "bssid": "11:22:33:44:55:66", "rssi": -72, "channel": 6, "security": "WPA2"},
        {"ssid": "Starbucks_Guest", "bssid": "99:88:77:66:55:44", "rssi": -85, "channel": 11, "security": "Open"},
        {"ssid": "Uni_Campus_WiFi", "bssid": "00:11:22:33:44:55", "rssi": -60, "channel": 36, "security": "WPA3"}
    ]
    
    # Sort networks by signal strength (RSSI) before returning
    # -45 dBm is stronger than -85 dBm
    sorted_networks = sorted(mock_scan_results, key=lambda x: x['rssi'], reverse=True)
    
    return sorted_networks