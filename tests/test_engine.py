"""Uji unit untuk mesin chatbot ColorMe (tanpa Flask)."""
from pathlib import Path

import pytest

from chatbot.engine import ChatbotEngine, load_themes, preprocess, similarity, validate_theme

THEMES = load_themes(Path(__file__).resolve().parent.parent / "themes")


def test_preprocess_normalisasi_dan_stopword():
    assert preprocess("Gimana cara cek undertone, kak?") == ["bagaimana", "cara", "cek", "undertone"]


def test_normalisasi_istilah_tema():
    assert preprocess("kerudung") == ["hijab"]
    assert preprocess("jilbab") == ["hijab"]
    assert preprocess("lipcream") == ["lipstik"]
    assert preprocess("ijo") == ["hijau"]
    assert preprocess("gold") == ["emas"]


def test_similarity_kalimat_sama_bernilai_satu():
    t = ["hijab", "warm", "undertone"]
    assert similarity(t, t) == 1.0


def test_similarity_kalimat_berbeda_rendah():
    assert similarity(["urat", "hijau"], ["lipstik", "cool"]) < 0.3


def test_tema_colorme_termuat():
    assert "colorme" in THEMES


def test_tema_memenuhi_syarat_tugas():
    t = THEMES["colorme"]
    assert len(t["intents"]) >= 10
    assert len(t["suggestions"]) >= 4
    for intent in t["intents"]:
        assert len(intent["patterns"]) >= 5, intent["tag"]
        assert len(intent["responses"]) >= 2, intent["tag"]


@pytest.mark.parametrize("pesan, intent", [
    ("halo kak", "salam"),
    ("kamu siapa?", "identitas"),
    ("apa itu undertone", "pengertian_undertone"),
    ("gmn cara tau undertone aku", "cara_cek_undertone"),
    ("urat nadiku hijau, undertone aku apa?", "ciri_urat_hijau"),
    ("kalo uratku biru ungu?", "ciri_urat_biru"),
    ("aku lebih cocok pakai perhiasan emas", "ciri_emas"),
    ("kulitku gampang gosong", "ciri_matahari_cokelat"),
    ("warna hijab buat warm undertone apa?", "hijab_warm"),
    ("kerudung untuk cool undertone", "hijab_cool"),
    ("lipstik yang cocok buat cool undertone?", "lipstik_cool"),
    ("outfit buat neutral undertone", "baju_neutral"),
    ("makasih ya", "terima_kasih"),
])
def test_klasifikasi_intent(pesan, intent):
    engine = ChatbotEngine(THEMES["colorme"])
    tag, _ = engine.classify(pesan)
    assert tag == intent


def test_salah_ketik_masih_dikenali():
    engine = ChatbotEngine(THEMES["colorme"])
    tag, _ = engine.classify("warna hijb warm undertne")
    assert tag == "hijab_warm"


@pytest.mark.parametrize("pesan", ["harga emas hari ini berapa", "siapa presiden indonesia", "apa kabar"])
def test_pertanyaan_di_luar_tema_memberi_fallback(pesan):
    engine = ChatbotEngine(THEMES["colorme"])
    hasil = engine.reply(pesan)
    assert hasil["intent"] is None
    assert hasil["reply"] in THEMES["colorme"]["fallback"]


def test_placeholder_nama_bot_diganti():
    engine = ChatbotEngine(THEMES["colorme"])
    hasil = engine.reply("kamu siapa")
    assert "{nama_bot}" not in hasil["reply"]
    assert "ColorMe" in hasil["reply"]


def test_explain_mengurutkan_kandidat_dari_skor_tertinggi():
    engine = ChatbotEngine(THEMES["colorme"])
    kandidat = engine.explain("lipstik untuk warm undertone")
    assert kandidat[0]["intent"] == "lipstik_warm"
    skor = [k["score"] for k in kandidat]
    assert skor == sorted(skor, reverse=True)


def test_validate_theme_menemukan_kesalahan():
    rusak = {"id": "x", "name": "X", "bot_name": "B", "avatar": "*", "color": "#000",
             "description": "d", "greeting": "g", "suggestions": [], "fallback": ["f"],
             "intents": [{"tag": "a", "patterns": ["halo"], "responses": ["hai"]},
                         {"tag": "b", "patterns": ["halo"], "responses": []}]}
    masalah = validate_theme(rusak)
    assert any("responses kosong" in m for m in masalah)
    assert any("'a' dan 'b'" in m for m in masalah)


def test_tema_colorme_valid():
    assert validate_theme(THEMES["colorme"]) == []


def test_akurasi_data_uji_colorme_minimal_90_persen():
    from evaluate import baca_data, evaluasi
    akurasi, _ = evaluasi(THEMES["colorme"], baca_data("colorme"), 0.45)
    assert akurasi >= 0.9
