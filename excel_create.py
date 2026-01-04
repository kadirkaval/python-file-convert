from fpdf import FPDF
import os

# PDF Sınıfı oluşturuyoruz
class PDF(FPDF):
    def header(self):
        # Header çalıştığında fontun yüklenmiş olduğundan emin olmalıyız.
        if 'ArialTR' in self.fonts:
            self.set_font('ArialTR', '', 8)
        else:
            self.set_font('Arial', 'I', 8)
            
        self.cell(0, 5, 'Otomatik Olusturulan Belge - Gemini & Python', 0, 1, 'R')
        self.line(10, 15, 200, 15)
        self.ln(10)

def create_pdf(data_json):
    pdf = PDF()
    
    # --- KRİTİK NOKTA (fpdf2 için) ---
    # Windows font yolu
    font_path = 'C:\\Windows\\Fonts\\arial.ttf'
    
    # Fontu ekliyoruz. NOT: fpdf2'de 'uni=True' parametresi kalktı, gerek yok.
    if os.path.exists(font_path):
        pdf.add_font('ArialTR', '', font_path) # uni=True SİLİNDİ
        print("✅ Arial fontu yüklendi.")
    else:
        print("UYARI: Arial fontu bulunamadı, standart font kullanılıyor.")

    pdf.add_page()

    # --- İÇERİK ---
    
    # Başlıklar
    if 'ArialTR' in pdf.fonts:
        pdf.set_font('ArialTR', '', 16)
    else:
        pdf.set_font('Arial', 'B', 16)
        
    pdf.cell(0, 10, data_json["baslik"], ln=1, align='C')
    
    # Alt Başlık
    pdf.set_font_size(12)
    pdf.cell(0, 10, f"Ders: {data_json['ders']} | Tarih: {data_json['tarih']}", ln=1, align='C')
    pdf.ln(5)

    # --- DÖNGÜ ---
    for bolum in data_json["bolumler"]:
        # Bölüm Başlığı
        pdf.set_font_size(14)
        pdf.set_text_color(0, 0, 128) # Lacivert
        
        pdf.cell(0, 10, bolum["bolum_adi"], ln=1)
        
        # İçerikler
        pdf.set_text_color(0, 0, 0) # Siyah
        pdf.set_font_size(11)
        
        for item in bolum["icerik"]:
            # fpdf2'de Türkçe karakterler için ekstra işleme gerek yok
            metin = f"Soru {item['soru']}: {item['cevap']}"
            pdf.multi_cell(0, 8, metin)
        
        pdf.ln(5)

    # --- KAYDET ---
    dosya_adi = f"{data_json['dosya_adi']}.pdf"
    pdf.output(dosya_adi)
    print(f"✅ PDF başarıyla oluşturuldu: {dosya_adi}")

# --- VERİ SETİ (İÇİNDE 'İ' HARFİ OLAN TEST VERİSİ) ---
veri_seti = {
    "baslik": "İNGİLİZCE - PERSONAL LIFE HOMEWORK-1", # Başlıkta 'İ' var
    "ders": "İngilizce",
    "tarih": "04.01.2026",
    "dosya_adi": "Ingilizce_Odev_PDF",
    "bolumler": [
        {
            "bolum_adi": "BÖLÜM 1: Boşluk Doldurma (İçerik)",
            "icerik": [
                {"soru": "1", "cevap": "about"},
                {"soru": "2", "cevap": "of"},
                {"soru": "11", "cevap": "isn't (İşaret zamiri)"}
            ]
        },
        {
            "bolum_adi": "BÖLÜM 2: Hata Düzeltme",
            "icerik": [
                {"soru": "a", "cevap": "Doğrusu: What does she look like?"},
                {"soru": "b", "cevap": "İstek kipi: She needs comfortable clothes."}
            ]
        }
    ]
}

# --- ÇALIŞTIR ---
if __name__ == "__main__":
    create_pdf(veri_seti)