import flet as ft
import tkinter as tk
from yt_dlp import YoutubeDL

import threading
from tkinter import filedialog, messagebox


def main(page: ft.Page):
    page.title = "YouTube Downloader by abd"
    page.icon = "icon.ico"  # تأكد من وجود ملف الأيقونة في نفس مسار الكود
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.scroll = 'auto'
    page.window.top = 150
    page.window.left = 350
    page.window.width = 900
    page.window.height = 535
    page.bgcolor = 'white'
    
    # جعل النصوص متجاوبة مع الشاشات المختلفة
    youtube_icon = ft.Image(src="youtube.png", width=125, height=100)  # تأكد من وجود ملف الأيقونة في نفس مسار الكود
    credit1_text = ft.Text("برنامج تنزيل الفيديوهات من اليوتيوب", size=22.7, weight="bold", color='blue')
    credit01_text = ft.Text("")

    url_input = ft.TextField(label="YouTube URL - رابط الفيديو")
    path_input = ft.TextField(label="Save Path - مكان الحفظ", width=810)
    browse_button = ft.IconButton(icon=ft.icons.FOLDER_OPEN, icon_color="white", bgcolor="blue", on_click=lambda _: browse_path(path_input))
    credit03_text = ft.Text("")

    path_row = ft.Row([path_input, browse_button], alignment=ft.MainAxisAlignment.CENTER)

    progress_bar = ft.ProgressBar()
    progress_text = ft.Text("0%", size=16)
    download_button = ft.ElevatedButton(text="Download", color="white", bgcolor="orange", on_click=lambda _: start_download(url_input.value, path_input.value, progress_bar, progress_text))
    credit2_text = ft.Text("تصميم وبرمجة التطبيق عبدالخالق © 2025", size=14, color='black')
    credit_text = ft.Text("Desinged and Coded by Abdalkaliq Basheer © 2025", size=14, color='black')

    # إضافة جميع العناصر إلى الصفحة مع توسيطها
    page.add(
        ft.Column(
            [
                youtube_icon,  # إضافة أيقونة اليوتيوب
                credit1_text, credit01_text,  
                url_input, path_row, progress_bar, 
                progress_text, credit03_text, download_button, 
                credit2_text, credit_text
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

def browse_path(path_input):
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askdirectory()
    path_input.value = path
    path_input.update()

def start_download(url, path, progress_bar, progress_text):
    def download():
        try:
            ydl_opts = {
                'outtmpl': f'{path}/%(title)s.%(ext)s',
                'progress_hooks': [lambda d: update_progress(d, progress_bar, progress_text)]
            }
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            show_error(str(e))

    threading.Thread(target=download).start()

def update_progress(d, progress_bar, progress_text):
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded_bytes = d.get('downloaded_bytes')
        progress = downloaded_bytes / total_bytes
        progress_bar.value = progress
        progress_text.value = f"{int(progress * 100)}%"
        progress_bar.update()
        progress_text.update()
    elif d['status'] == 'finished':
        progress_bar.value = 1
        progress_text.value = "اكتمل التنزيل"
        progress_bar.update()
        progress_text.update()

def show_error(message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Error", message)

ft.app(target=main)
