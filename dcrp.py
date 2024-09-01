import base64
from pypresence import Presence
from pycaw.pycaw import AudioUtilities
from pygetwindow import getWindowsWithTitle
import time
import tkinter as tk

encoded_id = ' '
client_id = base64.b64decode(encoded_id).decode()
RPC = Presence(client_id)
RPC.connect()

# Sayaç başlangıç zamanını program başlangıcında ayarlayın
start_time = time.time()

current_state = "Anime izlemeye hazırlanıyor"
current_details = "Arigato!"
RPC.update(
    state=current_state,
    details=current_details,
    large_image="large_image_key",
    large_text="Çok zor ya...",
    small_image="small_image_key",
    small_text="Bu program ladyofdarknes tarafından yazılmıştır!",
    start=start_time  # Sabit başlangıç zamanını kullanın
)

media_update_enabled = True

def get_media_info():
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process:
            process_name = session.Process.name().lower()
            if process_name in ["chrome.exe", "vlc.exe", "spotify.exe"]: 
                windows = getWindowsWithTitle(process_name.replace('.exe', ''))
                if windows:
                    return windows[0].title 
    return None 

def update_state():
    global current_state
    new_state = state_entry.get()
    current_state = new_state
    update_rpc()
    print(f"State güncellendi: {current_state}")

def update_details():
    global current_details
    new_details = details_entry.get()
    current_details = new_details
    update_rpc()
    print(f"Details güncellendi: {current_details}")

def toggle_media_update():
    global media_update_enabled
    media_update_enabled = not media_update_enabled
    if media_update_enabled:
        toggle_button.config(text="Medya Güncellemelerini Kapat")
        print("Medya güncellemeleri açıldı.")
    else:
        toggle_button.config(text="Medya Güncellemelerini Aç")
        print("Medya güncellemeleri kapatıldı.")
        RPC.update(
            state=current_state,
            details=current_details,
            large_image="large_image_key",
            large_text="Çok zor ya...",
            small_image="small_image_key",
            small_text="Bu program ladyofdarknes tarafından yazılmıştır!",
            start=start_time
        )

def update_rpc():
    if media_update_enabled:
        media_info = get_media_info() or "No active media"
    else:
        media_info = current_details 
    RPC.update(
        state=current_state,
        details=media_info,
        large_image="large_image_key",
        large_text="Çok zor ya...",
        small_image="small_image_key",
        small_text="Bu program ladyofdarknes tarafından yazılmıştır!",
        start=start_time
    )
    if media_update_enabled:
        root.after(15000, update_rpc)

root = tk.Tk()
root.title("Discord RPC Updater")

tk.Label(root, text="State:").pack()
state_entry = tk.Entry(root)
state_entry.pack()
state_entry.insert(0, current_state)
tk.Button(root, text="State Güncelle", command=update_state).pack()

tk.Label(root, text="Details:").pack()
details_entry = tk.Entry(root)
details_entry.pack()
details_entry.insert(0, current_details)
tk.Button(root, text="Details Güncelle", command=update_details).pack()

toggle_button = tk.Button(root, text="Medya Güncellemelerini Kapat", command=toggle_media_update)
toggle_button.pack()

root.mainloop()
