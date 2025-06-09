import tkinter as tk
from tkinter import ttk
import threading
import pyautogui
import time

class OtomatikTiklayici:
    def __init__(self, root):
        self.root = root
        self.root.title("YiğitDev Otomatik Tıklayıcı")
        self.root.geometry("400x300")
        self.calismiyor = False 

        aralik_kutusu = ttk.LabelFrame(root, text="Tıklama Aralığı")
        aralik_kutusu.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.saat = tk.IntVar(value=0)
        self.dakika = tk.IntVar(value=0)
        self.saniye = tk.IntVar(value=0)
        self.milisaniye = tk.IntVar(value=100)

        ttk.Entry(aralik_kutusu, textvariable=self.saat, width=5).grid(row=0, column=0)
        ttk.Label(aralik_kutusu, text="saat").grid(row=0, column=1)
        ttk.Entry(aralik_kutusu, textvariable=self.dakika, width=5).grid(row=0, column=2)
        ttk.Label(aralik_kutusu, text="dakika").grid(row=0, column=3)
        ttk.Entry(aralik_kutusu, textvariable=self.saniye, width=5).grid(row=0, column=4)
        ttk.Label(aralik_kutusu, text="saniye").grid(row=0, column=5)
        ttk.Entry(aralik_kutusu, textvariable=self.milisaniye, width=7).grid(row=0, column=6)
        ttk.Label(aralik_kutusu, text="milisaniye").grid(row=0, column=7)

        secenekler_kutusu = ttk.LabelFrame(root, text="Tıklama Seçenekleri")
        secenekler_kutusu.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.fare_tusu = tk.StringVar(value="left")
        self.tiklama_turu = tk.StringVar(value="single")

        ttk.Label(secenekler_kutusu, text="Fare tuşu:").grid(row=0, column=0)
        ttk.Combobox(secenekler_kutusu, textvariable=self.fare_tusu, values=["left", "right", "middle"], width=10).grid(row=0, column=1)

        ttk.Label(secenekler_kutusu, text="Tıklama türü:").grid(row=1, column=0)
        ttk.Combobox(secenekler_kutusu, textvariable=self.tiklama_turu, values=["single", "double"], width=10).grid(row=1, column=1)

        tekrar_kutusu = ttk.LabelFrame(root, text="Tıklama Tekrarı")
        tekrar_kutusu.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.tekrar_tipi = tk.StringVar(value="until_stopped")
        self.tekrar_sayisi = tk.IntVar(value=1)

        ttk.Radiobutton(tekrar_kutusu, text="Tekrarla", variable=self.tekrar_tipi, value="repeat").grid(row=0, column=0)
        ttk.Entry(tekrar_kutusu, textvariable=self.tekrar_sayisi, width=5).grid(row=0, column=1)
        ttk.Label(tekrar_kutusu, text="kez").grid(row=0, column=2)

        ttk.Radiobutton(tekrar_kutusu, text="Durdurulana kadar tekrarla", variable=self.tekrar_tipi, value="until_stopped").grid(row=1, column=0, columnspan=3)

        imlec_kutusu = ttk.LabelFrame(root, text="İmleç Pozisyonu")
        imlec_kutusu.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.imlec_konumu = tk.StringVar(value="current")
        self.pos_x = tk.IntVar(value=0)
        self.pos_y = tk.IntVar(value=0)

        ttk.Radiobutton(imlec_kutusu, text="Şu anki konum", variable=self.imlec_konumu, value="current").grid(row=0, column=0)
        ttk.Radiobutton(imlec_kutusu, text="Konumu seç", variable=self.imlec_konumu, value="pick").grid(row=0, column=1)
        ttk.Label(imlec_kutusu, text="X").grid(row=0, column=2)
        ttk.Entry(imlec_kutusu, textvariable=self.pos_x, width=5).grid(row=0, column=3)
        ttk.Label(imlec_kutusu, text="Y").grid(row=0, column=4)
        ttk.Entry(imlec_kutusu, textvariable=self.pos_y, width=5).grid(row=0, column=5)

        self.baslat_butonu = ttk.Button(root, text="Başlat (B)", command=self.baslat)
        self.baslat_butonu.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        self.durdur_butonu = ttk.Button(root, text="Durdur (B)", command=self.durdur, state="disabled")
        self.durdur_butonu.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

    def aralik_ms(self):
        return (self.saat.get() * 3600000 +
                self.dakika.get() * 60000 +
                self.saniye.get() * 1000 +
                self.milisaniye.get())

    def tiklama_islemi(self):
        tus = self.fare_tusu.get()
        tur = self.tiklama_turu.get()
        pozisyon = (self.pos_x.get(), self.pos_y.get()) if self.imlec_konumu.get() == "pick" else None

        while self.calismiyor:
            if pozisyon:
                pyautogui.moveTo(pozisyon[0], pozisyon[1])
            if tur == "single":
                pyautogui.click(button=tus)
            else:
                pyautogui.click(button=tus, clicks=2, interval=0.1)

            if self.tekrar_tipi.get() == "repeat":
                self.tekrar_sayisi.set(self.tekrar_sayisi.get() - 1)
                if self.tekrar_sayisi.get() <= 0:
                    break

            time.sleep(self.aralik_ms() / 1000.0)

        self.calismiyor = False
        self.baslat_butonu.config(state="normal")
        self.durdur_butonu.config(state="disabled")

    def baslat(self):
        if self.aralik_ms() <= 0:
            tk.messagebox.showerror("Geçersiz Aralık", "Lütfen geçerli bir aralık giriniz.")
            return

        self.calismiyor = True
        self.baslat_butonu.config(state="disabled")
        self.durdur_butonu.config(state="normal")

        threading.Thread(target=self.tiklama_islemi, daemon=True).start()

    def durdur(self):
        self.calismiyor = False

root = tk.Tk()
app = OtomatikTiklayici(root)
root.mainloop()
