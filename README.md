# ColorMe Bot – Chatbot Tematik Flask

Chatbot rule-based untuk mengenali undertone kulit (warm, cool, neutral) dan merekomendasikan warna baju, hijab, lipstik, serta perhiasan. Kode diambil dari `aplikasi-final` dosen; yang diganti hanya tema dan data ujinya.

## Menjalankan

```bash
python -m venv venv
venv\Scripts\activate            # Windows  (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
python app.py                    # buka http://127.0.0.1:5000
```

| Perintah | Fungsi |
| --- | --- |
| `python cli.py` | Chat di terminal |
| `pytest -v` | Jalankan 42 uji otomatis |
| `python evaluate.py` | Akurasi dari `evaluasi/colorme.csv` (100% pada ambang 0,45) |
| `python evaluate.py --sweep` | Bandingkan beberapa ambang |

## Yang diubah dari kode dosen

| File | Perubahan |
| --- | --- |
| `themes/colorme.json` | Tema baru: 28 intent, tiap intent minimal 5 patterns dan 2 responses, 4 suggestions, 2 fallback |
| `themes/kampus.json`, `kuliner.json`, `wisata.json` | Dihapus |
| `chatbot/engine.py` | `NORMALISASI` ditambah kata tema (kerudung/jilbab → hijab, ijo → hijau, lipcream → lipstik, gold → emas, gosong → cokelat, dll.) |
| `evaluasi/colorme.csv` | 38 kalimat uji, termasuk 5 pertanyaan di luar tema |
| `tests/` | Kasus uji disesuaikan dengan ColorMe |
| `cli.py`, `evaluate.py` | Tema bawaan diganti menjadi `colorme` |

## Screenshots

![Halaman awal](screenshots/01-halaman-awal.jpg)
![Tebak undertone](screenshots/03-tebak-undertone.jpg)
![Rekomendasi hijab](screenshots/04-rekomendasi-hijab.jpg)
![Fallback](screenshots/07-fallback.jpg)
