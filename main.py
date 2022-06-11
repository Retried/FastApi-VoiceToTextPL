import speech_recognition as sr
import uvicorn
from fastapi import FastAPI, UploadFile

r = sr.Recognizer()

app = FastAPI(
    title="FastAPI VoiceToTextPL",
    description="Voice recognition app",
    version="0.0.1"
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/test/")
def create_upload_file(file: UploadFile):
    with sr.AudioFile('example_audio_files/'+file.filename) as source:
        audio_text = r.listen(source)
        text = r.recognize_google(audio_text, language='pl-PL')
        return {'Konwertowanie transkryptu audio na tekst ... '+text}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8848, log_level="info", debug=True)
