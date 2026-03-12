# LegalBot — Miras Hukuku Asistani

Avukatlara yonelik PDF tabanli hukuki chatbot. Yuklu kanun belgesini okuyup belleğe atar; avukat soru sorduğunda ilgili maddeleri bulup aciklar.

---


https://github.com/user-attachments/assets/5e361ae2-0b8f-40f5-8f8a-40e6fdf170a7


## Nasil Calisir

Uygulama baslarken `miras_kanunu.pdf` dosyasini okur ve tumunu bellekte tutar. Avukat bir soru yazdiginda bu metin, sistem promptu olarak Groq API'ye iletilir. Model yalnizca bu metne dayanarak yanit uretir ve her yanita ilgili madde numarasini ekler.

---

## Ozellikler

Sohbet gecmisini konusmadan konusmaya tasir, yani avukat onceki sorulara atifta bulunabilir. Her yanit "Madde X uyarinca..." bicimiyle basar; arayuz bu madde referanslarini otomatik olarak vurgular. Sol panelde ornek sorular bulunur, bunlara tiklandiginda soru alanina otomatik yazilir.

---

## Kullanilan Teknolojiler

Frontend tamamen Vanilla HTML, CSS ve JavaScript ile yazildi. Backend FastAPI ile Python uzerinde calisiyor. PDF okuma icin `pdfplumber` kullanildi. Dil modeli olarak Groq uzerindeki Llama 3.3 70B secildi.

---

## Groq API Key

[console.groq.com](https://console.groq.com) adresine girerek ucretsiz hesap ac ve API anahtari olustur. Kredi karti bilgisi istenmez.

`backend/.env` dosyasi olustur:

```
GROQ_API_KEY=buraya_kendi_anahtarini_yaz
```

---

## Kurulum

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Tarayicida `http://localhost:8000` adresini ac. Chrome veya Edge onerilir.

---

## Kendi PDF'ini Kullanmak

`backend/miras_kanunu.pdf` dosyasini kendi kanun belgeni ile degistir, sunucuyu yeniden baslatmak yeterli. Baska herhangi bir degisiklik gerekmez.

---

## Lisans

MIT
