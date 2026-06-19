import time
import pywifi
from pywifi import const

def get_wifi_networks():
    """
    Scans the air for Wi-Fi access points and returns a list of dictionaries.
    """
    
    wifi = pywifi.PyWiFi()
    
    # Check if any wireless interfaces are available
    if not wifi.interfaces():
        print("Error: No Wi-Fi interfaces found. Ensure Wi-Fi is enabled.")
        return []
        
    iface = wifi.interfaces()[0]
    
    # Disconnect temporarily if needed to ensure a clean scan
    iface.disconnect()
    time.sleep(1)
    
    # Trigger the hardware scan
    iface.scan()
    time.sleep(4)
    
    # Fetch the raw scan results from the OS
    scan_results = iface.scan_results()
    
    # Filter out duplicates
    networks_dict = {}
    
    for profile in scan_results:
        ssid = profile.ssid
        bssid = profile.bssid
        rssi = profile.signal
        
        # Handle hidden networks (empty SSID)
        if not ssid or ssid.strip() == "":
            ssid = "[Hidden Network]"
            
        # Categorise security type based on AKM (Authentication and Key Management)
        security = "Open"
        if profile.akm:
            akm_val = profile.akm[-1] # Fetch the highest security protocol listed
            if akm_val == const.AKM_TYPE_WPA:
                security = "WPA"
            elif akm_val in (const.AKM_TYPE_WPA2, const.AKM_TYPE_WPA2PSK):
                security = "WPA2"
            elif hasattr(const, 'AKM_TYPE_WPA3') and akm_val == getattr(const, 'AKM_TYPE_WPA3'):
                security = "WPA3"
            elif akm_val == const.AKM_TYPE_NONE:
                security = "Open"
            else:
                security = "Secured"

        # Determine the Wi-Fi channel from the raw frequency
        channel = get_channel_from_freq(profile.freq)

        # Update the dictionary. If we see the same BSSID again, keep the one with the stronger signal.
        if bssid not in networks_dict or rssi > networks_dict[bssid]['rssi']:
            networks_dict[bssid] = {
                "ssid": ssid,
                "bssid": bssid,
                "rssi": rssi,
                "channel": channel,
                "security": security
            }
            
    # Convert the filtered dictionary back into a standard list
    processed_results = list(networks_dict.values())
    
    # Sort networks by signal strength (RSSI) before returning
    sorted_networks = sorted(processed_results, key=lambda x: x['rssi'], reverse=True)
    
    return sorted_networks

def get_channel_from_freq(freq):
    """
    Helper function to convert frequency (in MHz) to standard Wi-Fi channels.
    Finds the 2.4 GHz and 5GHz channels.
    """
    try:
        freq = int(freq)
        # 2.4 GHz Band
        if 2412 <= freq <= 2484:
            if freq == 2484:
                return 14
            return (freq - 2412) // 5 + 1
        # 5 GHz Band
        elif 5170 <= freq <= 5825:
            return (freq - 5170) // 5 + 34
    except (ValueError, TypeError):
        pass
        
    return "N/A"