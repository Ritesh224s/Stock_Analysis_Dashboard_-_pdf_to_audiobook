import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import fitz  # PyMuPDF
import pyttsx3
from gtts import gTTS
import os
import pygame

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# ------------------ PDF to Text ------------------
def extract_text_from_pdf(pdf_path, start_page=0, end_page=None):
    text = ""
    doc = fitz.open(pdf_path)
    if end_page is None:
        end_page = len(doc) - 1
    for page_num in range(start_page, end_page + 1):
        text += doc[page_num].get_text()
    return text.strip()

# ------------------ Text to Speech (pyttsx3) ------------------
def convert_to_speech(text, rate=150, volume=1.0, save_path=None):
    engine = pyttsx3.init()
    engine.setProperty("rate", rate)
    engine.setProperty("volume", volume)

    if save_path:
        engine.save_to_file(text, save_path)
        engine.runAndWait()
        return save_path
    else:
        engine.say(text)
        engine.runAndWait()
        return None

# ------------------ Text to MP3 (gTTS) ------------------
def convert_to_mp3(text, save_path="output.mp3", lang="en"):
    tts = gTTS(text=text, lang=lang)
    tts.save(save_path)
    return save_path

# ------------------ Play Audio ------------------
def play_audio(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def stop_audio():
    pygame.mixer.music.stop()

# ------------------ GUI ------------------
class PDFToAudiobookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📖 PDF to Audiobook Converter")
        self.root.geometry("600x400")

        self.file_path = ""
        self.text = ""

        # File Selection
        self.upload_btn = tk.Button(root, text="Upload PDF", command=self.load_pdf)
        self.upload_btn.pack(pady=10)

        # Page Range
        self.page_frame = tk.Frame(root)
        self.page_frame.pack(pady=5)
        tk.Label(self.page_frame, text="Start Page:").grid(row=0, column=0)
        self.start_page = tk.Entry(self.page_frame, width=5)
        self.start_page.grid(row=0, column=1)
        tk.Label(self.page_frame, text="End Page:").grid(row=0, column=2)
        self.end_page = tk.Entry(self.page_frame, width=5)
        self.end_page.grid(row=0, column=3)

        # Controls
        self.rate = tk.Scale(root, from_=100, to=250, orient="horizontal", label="Speed (WPM)")
        self.rate.set(150)
        self.rate.pack(pady=5)

        self.volume = tk.Scale(root, from_=0, to=1, resolution=0.1, orient="horizontal", label="Volume")
        self.volume.set(1.0)
        self.volume.pack(pady=5)

        # Buttons
        self.convert_btn = tk.Button(root, text="Convert & Play", command=self.convert_and_play)
        self.convert_btn.pack(pady=5)

        self.export_btn = tk.Button(root, text="Export as MP3", command=self.export_mp3)
        self.export_btn.pack(pady=5)

        self.stop_btn = tk.Button(root, text="Stop", command=stop_audio)
        self.stop_btn.pack(pady=5)

        # Progress
        self.progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)

    def load_pdf(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.file_path:
            messagebox.showinfo("Success", "PDF Loaded Successfully!")

    def convert_and_play(self):
        if not self.file_path:
            messagebox.showerror("Error", "Upload a PDF first!")
            return

        start = int(self.start_page.get() or 0)
        end = self.end_page.get()
        end = int(end) if end else None

        self.text = extract_text_from_pdf(self.file_path, start, end)
        if not self.text:
            messagebox.showerror("Error", "No text found in PDF!")
            return

        temp_file = "temp_output.mp3"
        convert_to_speech(self.text, rate=self.rate.get(), volume=self.volume.get(), save_path=temp_file)
        play_audio(temp_file)

    def export_mp3(self):
        if not self.text:
            messagebox.showerror("Error", "Convert a PDF first!")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 Files", "*.mp3")])
        if save_path:
            convert_to_mp3(self.text, save_path)
            messagebox.showinfo("Success", f"File saved as {save_path}")

# ------------------ Run App ------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = PDFToAudiobookApp(root)
    root.mainloop()
