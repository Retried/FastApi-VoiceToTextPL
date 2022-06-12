import os
import math
from pydub import AudioSegment


class SplitAudio:
    def __init__(self, folder, filename, filetype):
        self.folder = folder
        self.filename = filename
        self.filepath = folder + '\\' + filename

        # Warunki sprawdzające format pliku audio
        if filetype == "audio/mpeg":
            self.audio = AudioSegment.from_mp3(self.filepath)
            self.filename = self.filename[:-4] + ".wav"
            self.filepath = folder + '\\' + filename
        elif filetype == "audio/wav":
            self.audio = AudioSegment.from_wav(self.filepath)
        else:
            pass

    # Funkcja pojedyńczego podzielenia pliku
    def single_split(self, from_min, to_min, split_filename):
        t1 = from_min * 30 * 1000  # Deklaracja odcinka 30 sekundowego
        t2 = to_min * 30 * 1000  # Deklaracja odcinka 30 sekundowego
        split_audio = self.audio[t1:t2]  # Podzielenie audio
        # W przypadku krótszych plików niż 1s nie są one zapisywane
        # Zrobione jest to ponieważ api Google nie obsługuje tak krótkich plików
        if split_audio.duration_seconds > 1:
            split_audio.export(self.folder + '\\' + split_filename, format="wav")

    # Funkcja podzielania na więcej niż 2 pliki
    def multiple_split(self):
        total_parts = math.ceil(self.audio.duration_seconds / 30)  # Zlicza części
        x = 0  # Zmienna odejmowana od ostatecznej ilości pliku w celu korekty licznika plików
        for i in range(0, total_parts, 1):
            split_fn = str(i) + '_' + self.filename
            self.single_split(i, i + 1, split_fn)  # Użycie funkcji podzielenia
            # Warunek sprawdzający istnienie pliku po podziale
            if os.path.isfile(f"files/{str(i) + '_' + self.filename}"):
                print(str(i) + ' Done')
            else:
                x += 1
            # Gdy wszystkie części się przetworzą, zwracana jest ich ilość i komunikat
            if i == total_parts - 1:
                opened = open(self.filepath[:-4] + ".txt", "wt")
                opened.write(str(i - x))
                opened.close()
                print('All splited successfully')
