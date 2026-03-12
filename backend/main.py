from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from groq import Groq
import pdfplumber
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="LegalBot API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY bulunamadi. .env dosyasina ekle.")

client = Groq(api_key=GROQ_API_KEY)

PDF_PATH = os.path.join(os.path.dirname(__file__), "miras_kanunu.pdf")


def load_pdf_text(path: str) -> str:
    """PDF'i okuyup tum metni tek string olarak dondur."""
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n\n"
    return text.strip()


# Uygulama baslarken PDF'i bir kere yukle, bellekte tut
print("PDF yukleniyor...")
LAW_TEXT = load_pdf_text(PDF_PATH)
print(f"PDF yuklendi. Toplam karakter: {len(LAW_TEXT)}")

SYSTEM_PROMPT = f"""Sen deneyimli bir Turk hukuk asistanisin. Gorev alani yalnizca asagida verilen kanun maddelerine dayanarak avukatlara yardimci olmaktir.

KANUN METNI:
{LAW_TEXT}

KURALLARIN:
1. Yalnizca yukaridaki kanun metnine dayanarak cevap ver.
2. Soruyla ilgili kanun maddesini acikca belirt (ornek: "Madde 5 uyarinca...").
3. Kanun metninde yer almayan konularda "Bu konu mevcut kanun metninde yer almamaktadir." de.
4. Hukuki terminolojiyi dogru kullan ama anlasilir bir dil kullan.
5. Avukata pratik bir ozet sun, ardindan ilgili madde numarasini ve aciklamasini ver.
6. Kesinlikle tahmin veya yorumdan kacinarak yalnizca metnin icerigi ile sinirli kal.
"""


class ChatRequest(BaseModel):
    messages: list  # [{"role": "user"|"assistant", "content": "..."}]


class ChatResponse(BaseModel):
    reply: str


app.mount("/static", StaticFiles(directory="../frontend"), name="static")


@app.get("/")
def serve_frontend():
    return FileResponse("../frontend/index.html")


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not req.messages:
        raise HTTPException(status_code=400, detail="Mesaj listesi bos olamaz.")

    # Son 10 mesaji gonder (context penceresi yonetimi)
    recent = req.messages[-10:]

    groq_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + recent

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=groq_messages,
            temperature=0.1,   # Hukuki hassasiyet icin dusuk sicaklik
            max_tokens=1024,
        )
        reply = response.choices[0].message.content.strip()
        return ChatResponse(reply=reply)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI hatasi: {str(e)}")