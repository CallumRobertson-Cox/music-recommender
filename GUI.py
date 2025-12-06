import tkinter as tk
from tkinter import messagebox
import threading
from Model import *   # make sure Model.py defines get_suggsested_tracks

SPOTIFY_GREEN = "#1DB954"

def start():
    def exit_app():
        root.destroy()

    def minimize_app():
        # Minimize the window to the taskbar
        root.iconify()

    def show_spinner():
        # Create spinner canvas
        spinner_canvas = tk.Canvas(root, width=100, height=100,
                                   bg=SPOTIFY_GREEN, highlightthickness=0)
        spinner_canvas.place(relx=0.5, rely=0.5, anchor="center")

        arc = spinner_canvas.create_arc(10, 10, 90, 90,
                                        start=0, extent=90,
                                        width=8, style="arc", outline="white")

        job_id = None

        def rotate(angle=0):
            nonlocal job_id
            if spinner_canvas.winfo_exists():  # only update if canvas still exists
                spinner_canvas.itemconfig(arc, start=angle)
                job_id = root.after(50, rotate, (angle + 10) % 360)

        rotate()

        # Return both canvas and a stop function
        def stop():
            if job_id:
                root.after_cancel(job_id)
            if spinner_canvas.winfo_exists():
                spinner_canvas.destroy()

        return stop

    def submit_all():
        client_id = client_id_entry.get().strip()
        client_secret = client_secret_entry.get().strip()
        playlist_id = playlist_id_entry.get().strip()

        if not client_id or not client_secret or not playlist_id:
            messagebox.showwarning("Oi!",
                "You forgot to fill in all the boxes!\nStop being lazy and type them in!")
        else:
            stop_spinner = show_spinner()  # show spinner

            def task():
                results = get_suggsested_tracks(playlist_id, client_id, client_secret)
                print("Suggested tracks:", results)
                stop_spinner()  # stop and remove spinner
                messagebox.showinfo("Success", "All credentials submitted successfully!")

            threading.Thread(target=task).start()

    # Main window
    root = tk.Tk()
    root.title("Spotify Credentials")
    root.configure(bg=SPOTIFY_GREEN)
    root.attributes("-fullscreen", True)

    # Exit button (top right)
    exit_button = tk.Button(root, text="X", command=exit_app,
                            font=("Arial", 14, "bold"),
                            bg="red", fg="white", bd=0)
    exit_button.place(relx=0.98, rely=0.02, anchor="ne")

    # Minimize button (next to exit)
    minimize_button = tk.Button(root, text="_", command=minimize_app,
                                font=("Arial", 14, "bold"),
                                bg="white", fg=SPOTIFY_GREEN, bd=0)
    minimize_button.place(relx=0.94, rely=0.02, anchor="ne")

    # Fonts
    label_font = ("Arial", 16, "bold")
    entry_font = ("Arial", 14)

    # Client ID
    tk.Label(root, text="Client ID:", bg=SPOTIFY_GREEN, fg="white", font=label_font).pack(pady=(50, 10))
    client_id_entry = tk.Entry(root, show="*", font=entry_font, width=40)
    client_id_entry.pack(pady=5)

    # Client Secret
    tk.Label(root, text="Client Secret:", bg=SPOTIFY_GREEN, fg="white", font=label_font).pack(pady=(30, 10))
    client_secret_entry = tk.Entry(root, show="*", font=entry_font, width=40)
    client_secret_entry.pack(pady=5)

    # Playlist ID
    tk.Label(root, text="Playlist ID:", bg=SPOTIFY_GREEN, fg="white", font=label_font).pack(pady=(30, 10))
    playlist_id_entry = tk.Entry(root, show="*", font=entry_font, width=40)
    playlist_id_entry.pack(pady=5)

    # Submit All button
    submit_button = tk.Button(root, text="Submit All", command=submit_all,
                              font=("Arial", 14, "bold"), bg="white", fg=SPOTIFY_GREEN)
    submit_button.pack(pady=40)

    root.mainloop()

start()