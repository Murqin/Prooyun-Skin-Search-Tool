import json
import os
import tkinter as tk
from tkinter import ttk
import unicodedata
import re

# Metni temizleme fonksiyonu
def normalize_text(text):
    if not text:
        return ""
    text = unicodedata.normalize("NFKD", text)  # Türkçe karakterleri normalleştir
    text = text.lower().strip()  # Küçük harfe çevir ve baştaki/sondaki boşlukları kaldır
    text = re.sub(r'\s+', ' ', text)  # Fazla boşlukları tek boşluk yap
    text = text.replace(" ", "")  # Tüm boşlukları kaldır
    text = text.replace("-", "")  # Çizgileri kaldır
    return text

# JSON dosyasını yükleme fonksiyonu
def load_json_data(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "files", file_name)
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    print(f"{json_path} dosyası bulunamadı.")
    return {}

data = load_json_data('skins.json')

def search():
    query = normalize_text(search_var.get())
    result_list.delete(*result_list.get_children())  # Önceden eklenen sonuçları sil

    for weapon, details in data.items():
        item_type, weapon_code = "", ""
        for detail in details:
            if "türü" in detail:
                item_type = detail.get("türü", "")
            if "kodadi" in detail:
                weapon_code = detail.get("kodadi", "")

        for detail in details:
            skin_name, skin_no = detail.get("isim", ""), detail.get("numara", "")
            if skin_name == "bilinmiyor" or not skin_name:
                continue
            if query in normalize_text(weapon) or query in normalize_text(skin_name):
                result_list.insert("", "end", values=(weapon, skin_name, skin_no, item_type, weapon_code))

def on_result_click(event):
    selected_items = result_list.selection()
    if not selected_items:
        return
    item = selected_items[0]
    weapon_name, skin_name, skin_no, item_type, weapon_code = result_list.item(item, "values")
    
    if item_type.lower() == "silah" or item_type.lower() == "bıçak":
        code_name = f"sm_ws {weapon_code} {skin_no}"
    elif item_type.lower() == "eldiven":
        code_name = f"sm_glove {skin_no}"
    else:
        return
    
    current_text = text_box.get("1.0", tk.END).strip()
    text_box.config(state=tk.NORMAL)
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, f"{current_text}; {code_name}" if current_text else code_name)
    text_box.config(state=tk.DISABLED)

def undo_last_entry():
    current_text = text_box.get("1.0", tk.END).strip()
    if ";" in current_text:
        current_text = current_text.rsplit(";", 1)[0]
    else:
        current_text = ""
    text_box.config(state=tk.NORMAL)
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, current_text)
    text_box.config(state=tk.DISABLED)

def clear_all_entries():
    text_box.config(state=tk.NORMAL)
    text_box.delete("1.0", tk.END)
    text_box.config(state=tk.DISABLED)

def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(text_box.get("1.0", tk.END).strip())
    root.update()

# Arayüz oluşturma
root = tk.Tk()
root.title("Prooyun Skin Kodu Arama Aracı")
root.geometry("800x800")
root.configure(bg="#e0f4fe")  # Açık mavi arka plan rengi

# İkonu ayarlama
current_dir = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(current_dir, "files", "icon.ico")
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)  # İkonu yükleme

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", background="#91caf8", foreground="black", font=("Arial", 10), padding=5, relief="flat")
style.map("TButton", background=[("active", "#66A1AE")])  # Hover rengi
style.configure("TEntry", fieldbackground="#ffffff", foreground="black", font=("Arial", 10))
style.configure("Treeview", background="#ffffff", fieldbackground="#ffffff", foreground="black", font=("Arial", 10))
style.configure("Treeview.Heading", background="#91caf8", foreground="black", font=("Arial", 10, "bold"))
style.map("Treeview.Heading", background=[("active", "#66A1AE")])
style.configure("TLabel", background="#e0f4fe", foreground="black", font=("Arial", 12))

search_var = tk.StringVar()
search_label = ttk.Label(root, text="Skin Ara")
search_label.pack(pady=10)
search_entry = ttk.Entry(root, textvariable=search_var, width=50)
search_entry.pack(pady=10)
search_button = ttk.Button(root, text="Ara", command=search)
search_button.pack(pady=10)

# Treeview ve Scrollbar'ı düzgün hizala
tree_frame = tk.Frame(root)
tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)  # Frame genişleyebilir hale getirildi

# Treeview
columns = ("Eşya Adı", "Skin Adı", "Skin No", "Eşya Türü", "Eşya Kod Adı")
result_list = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
result_list.pack(side="left", fill=tk.BOTH, expand=True)  # Expand ekleyerek genişleme sağlandı

# Scrollbar
scrollbar = tk.Scrollbar(tree_frame, orient="vertical", command=result_list.yview)
scrollbar.pack(side="right", fill="y")
result_list.configure(yscrollcommand=scrollbar.set)

for col in columns:
    result_list.heading(col, text=col)
    result_list.column(col, width=150)

# Textbox
text_box = tk.Text(root, height=5, width=70, wrap=tk.WORD, state=tk.DISABLED, bg="white", fg="black", font=("Arial", 10))
text_box.pack(pady=10, padx=10, fill=tk.NONE)

# Butonlar
button_frame = tk.Frame(root, bg="#e0f4fe")
button_frame.pack(pady=10)

undo_button = ttk.Button(button_frame, text="Geri Al", command=undo_last_entry, style="TButton")
clear_button = ttk.Button(button_frame, text="Hepsini Sil", command=clear_all_entries, style="TButton")
copy_button = ttk.Button(button_frame, text="Hepsini Kopyala", command=copy_to_clipboard, style="TButton")

undo_button.pack(side=tk.LEFT, padx=5)
clear_button.pack(side=tk.LEFT, padx=5)
copy_button.pack(side=tk.LEFT, padx=5)

# Footer
footer_label = ttk.Label(root, text="Bu programın prooyun ile bağlantısı yoktur, sadece prooyun sunucularında oynarken kolaylık sağlaması amacıyla yapılmıştır.", font=("Arial", 8), background="#e0f4fe")
footer_label.pack(side="bottom", pady=10)

search_entry.focus()
result_list.bind("<Double-1>", on_result_click)
root.mainloop()
