import os
import speech_recognition as sr
import uvicorn

from fastapi import FastAPI, UploadFile, File, Query, Request
from fastapi.responses import RedirectResponse
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates

from Cleanup import Cleanup
from Splitter import SplitAudio

r = sr.Recognizer()

app = FastAPI(
    title="FastAPI VoiceToTextPL",
    description="Voice recognition app",
    version="0.1"
)

# templates = Jinja2Templates(directory="templates")  # Przygotowania pod formularz


# @app.get("/", response_class=HTMLResponse)  # Przygotowania pod formularz
# def index(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

@app.get("/")
def index():
    return RedirectResponse("http://127.0.0.1:8848/docs")


@app.post("/uploaded/")
def create_upload_file(find: list | None = Query(default=None), uploaded_file: UploadFile = File(...)):
    file_location = f"files/{uploaded_file.filename}"  # Zadeklarowanie lokalizacji pliku
    opened = open(file_location, "wb+")
    opened.write(uploaded_file.file.read())  # Zapisanie przesłanego pliku na dysk
    opened.close()

    # Warunek sprawdzający rozszerzenie pliku
    if uploaded_file.content_type == "audio/mpeg" or uploaded_file.content_type == "audio/wav":
        # Funkcja rozdzielająca plik na kawałki
        SplitAudio("files", uploaded_file.filename, uploaded_file.content_type).multiple_split()
    else:
        # Usunięcie niekompatybilnego pliku
        os.remove(file_location)
        return "Format pliku nie jest wspierany"

    newname = uploaded_file.filename[:-4]  # Zdefiniowanie nazwy pliku bez rozszerzenia
    # Warunek sprawdzający istnienie pliku z ilością podzielonych plików
    if os.path.isfile("files/" + newname + ".txt"):
        text = 'Wynik transkrypcji: '
        # Wczytanie ilości plików
        with open("files/" + newname + ".txt", "rt") as f:
            value = f.readlines()

        # Pętla wrzucająca każdy plik do api firmy Google
        for i in range(int(value[0]) + 1):
            with sr.AudioFile(f"files/{str(i) + '_' + newname + '.wav'}") as source:
                audio_text = r.listen(source)
                text += r.recognize_google(audio_text, language='pl-PL') + " "

        # Warunek sprawdzający istnienie szukanego elementu
        if find is not None:
            return_list = [""] * len(find)  # Deklaracja pustej listy
            # Pętla tworząca wiersze wyników wyszukiwania
            for i, val in enumerate(find):
                return_list[i] = "Występowanie '" + val + "' : " + str(text.lower().count(val.lower()))
            return {'   '.join(return_list)}
        return {text}  # Jeżeli nie ma szukanego elementu wypisuje całą transkrypcję

    else:
        return "There is no file"


if __name__ == "__main__":
    Cleanup("files/")
    uvicorn.run(app, host="127.0.0.1", port=8848, log_level="info", debug=True)
