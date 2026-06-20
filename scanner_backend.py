import asyncio
import platform

try:
    from winsdk.windows.devices.wifi import WiFiAdapter
except ImportError:
    print("Error: The 'winsdk' library is missing. Please run: pip install winsdk")
    WiFiAdapter = None

async def _scan_winrt_async():
    """
    Asynchronously communicates with the Windows Runtime (WinRT) 
    to command the physical Wi-Fi adapter to scan the airwaves.
    """
    if not WiFiAdapter:
        return []

    # Request access to the Wi-Fi hardware
    adapters_result = await WiFiAdapter.find_all_adapters_async()
    
    if not adapters_result or adapters_result.size == 0:
        print("Error: No Wi-Fi adapters found via WinRT.")
        return []
        
    # Grab the primary physical Wi-Fi adapter
    adapter = adapters_result.get_at(0)
    
    # Trigger the hardware scan
    await adapter.scan_async()
    
    # Retrieve the generated report natively from the OS
    report = adapter.network_report
    networks_dict = {}
    
    # Iterate through all detected network APs
    for network in report.available_networks:
        ssid = network.ssid
        if not ssid:
            ssid = "[Hidden Network]"
            
        bssid = network.bssid.upper()
        rssi = network.network_rssi_in_decibel_milliwatts
        
        # Convert frequency from kHz to MHz to determine the Wi-Fi channel
        freq_mhz = network.channel_center_frequency_in_kilohertz / 1000
        channel = get_channel_from_freq(freq_mhz)
        
        # Categorise the security protocol
        auth_type = network.security_settings.network_authentication_type.name
        
        security = "Secured"
        if "WPA3" in auth_type:
            security = "WPA3"
        elif "RSNA" in auth_type:
            security = "WPA2"
        elif "WPA" in auth_type:
            security = "WPA"
        elif "OPEN" in auth_type or "None" in auth_type:
            security = "Open"

        # Filter duplicates, storing only the router broadcast with the strongest signal
        if bssid not in networks_dict or rssi > networks_dict[bssid]['rssi']:
            networks_dict[bssid] = {
                "ssid": ssid,
                "bssid": bssid,
                "rssi": rssi,
                "channel": channel,
                "security": security
            }
            
    # Return the final dictionary as a sorted list
    return sorted(networks_dict.values(), key=lambda x: x['rssi'], reverse=True)

def get_wifi_networks():
    """
    Synchronous wrapper for the Tkinter frontend to call.
    It initialises the asyncio event loop and runs the WinRT scanner.
    """
    if platform.system() != "Windows":
        print("Error: The WinRT API is strictly for Windows 10/11.")
        return []
        
    # Run the asynchronous scan and return the results cleanly to the UI
    return asyncio.run(_scan_winrt_async())

def get_channel_from_freq(freq):
    """
    Helper function to convert frequency (in MHz) to standard Wi-Fi channels.
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