from fpdf import FPDF
from fpdf.enums import XPos, YPos  # Yeni hizalama sistemi için gerekli
import os

class PDF(FPDF):
    def header(self):
        # Header her sayfada çalıştığı için fontun tanımlı olduğundan emin olmalıyız
        # Burada doğrudan ArialTR kullanıyoruz, çünkü aşağıda kesin yükleyeceğiz.
        self.set_font('ArialTR', '', 8)
        
        # new_x ve new_y parametreleri fpdf2'nin yeni standardıdır (ln=1 yerine)
        self.cell(0, 5, 'Otomatik Olusturulan Belge - Gemini & Python', 
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='R')
        
        self.line(10, 15, 200, 15)
        self.ln(5)

def create_pdf(data_json):
    pdf = PDF()
    
    # --- 1. ADIM: FONTU KESİN OLARAK YÜKLE ---
    # Windows font klasöründeki Arial dosyasını hedefliyoruz.
    font_path = r'C:\Windows\Fonts\arial.ttf'
    
    if not os.path.exists(font_path):
        print(f"HATA: Font dosyası bulunamadı: {font_path}")
        return

    # Fontu sisteme 'ArialTR' adıyla tanıtıyoruz.
    pdf.add_font('ArialTR', style='', fname=font_path)
    
    # --- 2. ADIM: SAYFAYI EKLE ---
    pdf.add_page()
    
    # Artık tüm belgede SADECE 'ArialTR' kullanacağız.
    # Asla set_font('Arial') demeyeceğiz çünkü o Helvetica'ya döner.

    # --- BAŞLIK ---
    pdf.set_font('ArialTR', size=16) # Başlık büyük
    pdf.cell(0, 10, data_json["baslik"], new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    
    # --- ALT BAŞLIK ---
    pdf.set_font('ArialTR', size=12) 
    pdf.cell(0, 10, f"Ders: {data_json['ders']} | Tarih: {data_json['tarih']}", 
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    
    pdf.ln(5) # Boşluk

    # --- İÇERİK DÖNGÜSÜ ---
    for bolum in data_json["bolumler"]:
        # Bölüm Başlığı
        pdf.set_font('ArialTR', size=14)
        pdf.set_text_color(0, 0, 128) # Lacivert
        
        pdf.cell(0, 10, bolum["bolum_adi"], new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        # İçerikler
        pdf.set_text_color(0, 0, 0) # Siyah
        pdf.set_font('ArialTR', size=11)
        
        for item in bolum["icerik"]:
            metin = f"Soru {item['soru']}: {item['cevap']}"
            # Multi_cell kullanımı da değişti
            pdf.multi_cell(0, 8, metin, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        pdf.ln(5)

    # --- KAYDET ---
    dosya_adi = f"{data_json['dosya_adi']}.pdf"
    pdf.output(dosya_adi)
    print(f"✅ PDF başarıyla oluşturuldu: {dosya_adi}")

# --- VERİ SETİ ---
veri_seti = {}

# --- ÇALIŞTIR ---
if __name__ == "__main__":
    create_pdf(veri_seti)