import tkinter as tk
import cv2
import threading
from PIL import Image, ImageTk
import time

class AttendanceTracker:
    def __init__(self, master):
        self.master = master
        self.master.title("Attendance Tracker")
        self.master.geometry("520x480")
        self.master.configure(bg="#1C1C1C") 

        self.cap = None
        self.is_running = False

     
        self.start_camera()

       
        self.camera_frame = tk.Label(self.master, bg="#2A2A2A", text="Camera Feed", font=("Arial", 16), fg="white")
        self.camera_frame.place(x=30, y=20, width=460, height=340)

       
        button_frame = tk.Frame(self.master, bg="#1C1C1C")
        button_frame.place(x=30, y=380, width=460, height=100)

    
        self.mark_button = tk.Button(button_frame, text="Mark Attendance", command=self.mark_attendance,
                                     font=("Arial", 12, "bold"), bg="#E67E22", fg="white", width=20,
                                     borderwidth=2, relief="raised")
        self.mark_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.mark_button.bind("<Enter>", lambda e: self.mark_button.config(bg="#D76D16"))
        self.mark_button.bind("<Leave>", lambda e: self.mark_button.config(bg="#E67E22"))

        
        self.view_button = tk.Button(button_frame, text="View Records", command=self.view_records,
                                     font=("Arial", 12, "bold"), bg="#E67E22", fg="white", width=20,
                                     borderwidth=2, relief="raised")
        self.view_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.view_button.bind("<Enter>", lambda e: self.view_button.config(bg="#D76D16"))
        self.view_button.bind("<Leave>", lambda e: self.view_button.config(bg="#E67E22"))

       
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

       
        self.status_bar = tk.Label(self.master, text="Camera is running...", bg="#2A2A2A", fg="white", font=("Arial", 10))
        self.status_bar.pack(side="bottom", fill="x")

      
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_camera(self):
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                print("Error: Could not open camera.")
                return

            self.is_running = True
            threading.Thread(target=self.update_camera_feed, daemon=True).start()  
        except Exception as e:
            print(f"Error starting camera: {e}")

    def update_camera_feed(self):
        while self.is_running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Failed to capture image.")
                break
            
           
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)

           
            self.camera_frame.imgtk = imgtk
            self.camera_frame.configure(image=imgtk)

   
            time.sleep(0.01)  


        if self.cap:
            self.cap.release()

    def mark_attendance(self):
        self.status_bar.config(text="Attendance marked successfully!")
        print("Mark Attendance Placeholder")

    def view_records(self):
        self.status_bar.config(text="Viewing records...")
        print("View Records Placeholder")

    def on_closing(self):
        self.is_running = False
        if self.cap and self.cap.isOpened():
            self.cap.release()
        self.master.destroy()

root = tk.Tk()
app = AttendanceTracker(root)
root.mainloop()
