import tkinter as tk
from tkinter import Canvas
import psutil
from datetime import datetime
import math


class SystemResourceMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("System Resource Monitor")
        self.root.geometry("500x500")
        self.root.configure(bg="#1E1E1E")  # Dark background for a modern look
        
        # Title
        self.title_label = tk.Label(
            self.root, 
            text="System Resource Monitor", 
            font=("Helvetica", 18, "bold"), 
            bg="#1E1E1E", 
            fg="#00FF00"
        )
        self.title_label.pack(pady=20)
        
        # Circular progress bars
        self.canvas_cpu = self.create_circular_progress_bar(100, "CPU")
        self.canvas_memory = self.create_circular_progress_bar(200, "Memory")
        self.canvas_disk = self.create_circular_progress_bar(300, "Disk")
        
        # Footer
        self.footer_label = tk.Label(
            self.root, 
            text="Developed by Farhad Ali", 
            font=("Helvetica", 10, "italic"), 
            bg="#1E1E1E", 
            fg="#00FF00"
        )
        self.footer_label.pack(side="bottom", pady=10)
        
        # Start updating stats
        self.update_stats()
    
    def create_circular_progress_bar(self, y_offset, label):
        """Create a circular progress bar."""
        canvas = Canvas(self.root, width=200, height=200, bg="#1E1E1E", highlightthickness=0)
        canvas.pack(pady=10)
        
        # Draw the background circle
        canvas.create_oval(20, 20, 180, 180, outline="#444", width=8)  # Static background circle
        
        # Add the label (CPU, Memory, Disk)
        canvas.create_text(100, 100, text=label, fill="#00FF00", font=("Helvetica", 14, "bold"), tags="label")
        
        return canvas

    def update_circular_progress_bar(self, canvas, percentage):
        """Update the circular progress bar based on percentage."""
        canvas.delete("arc")  # Remove previous arc
        
        # Calculate the angle for the arc
        angle = percentage * 3.6  # Percentage to degrees (360 degrees = 100%)
        
        # Draw the arc (progress)
        canvas.create_arc(
            20, 20, 180, 180, 
            start=90,  # Start at the top
            extent=-angle,  # Sweep counterclockwise
            outline="#00FF00", 
            width=8, 
            style="arc", 
            tags="arc"
        )
        
        # Update the percentage label
        canvas.delete("percentage")
        canvas.create_text(100, 140, text=f"{percentage}%", fill="white", font=("Helvetica", 12), tags="percentage")
    
    def update_stats(self):
        # CPU Usage
        cpu_usage = int(psutil.cpu_percent(interval=0.5))
        self.update_circular_progress_bar(self.canvas_cpu, cpu_usage)
        
        # Memory Usage
        memory_info = psutil.virtual_memory()
        memory_usage = int(memory_info.percent)
        self.update_circular_progress_bar(self.canvas_memory, memory_usage)
        
        # Disk Usage
        disk_info = psutil.disk_usage('/')
        disk_usage = int(disk_info.percent)
        self.update_circular_progress_bar(self.canvas_disk, disk_usage)
        
        # Refresh every second
        self.root.after(1000, self.update_stats)


# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = SystemResourceMonitor(root)
    root.mainloop()
