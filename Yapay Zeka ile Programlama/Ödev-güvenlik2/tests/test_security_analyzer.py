"""Çevrimdışı, API anahtarı gerektirmeyen doğrulama testleri.

Gerçek Gemini ile açık bulma başarısını sınamaz. Yanıtlar test doubles / mock veridir.
"""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import security_analyzer as analyzer


EXPECTED = {
    "sql_injection.py": ("SQL Injection", "Yüksek", 'conn.execute(sorgu)'),
    "hardcoded_password.py": ("Sabit Parola Kullanımı", "Orta", 'DB_PASSWORD = "ORNEK_GERCEK_OLMAYAN_PAROLA_123"'),
    "command_injection.py": ("Komut Enjeksiyonu", "Kritik", 'os.system("ls " + klasor_adi)'),
    "path_traversal.py": ("Path Traversal", "Yüksek", 'target = base_dir / filename'),
    "unsafe_deserialization.py": ("Güvensiz Serileştirme", "Kritik", "pickle.loads(request_body)"),
}


def mocked_response(filename: str) -> str:
    stem = Path(filename).name
    if stem == "safe_code.py":
        return '{"findings": []}'
    finding_type, severity, evidence = EXPECTED[stem]
    DETAILS = {
        "sql_injection.py": (
            "Kullanıcı adı parametreli sorgu yerine metin birleştirmeyle SQL'e katılıyor.",
            "Saldırgan sorgunun anlamını değiştirerek veri okuyabilir veya değiştirebilir.",
            'conn.execute("SELECT * FROM kullanicilar WHERE ad = ?", (kullanici_adi,))',
        ),
        "hardcoded_password.py": (
            "Parola kaynağa düz metin sabit olarak gömülmüş.",
            "Kaynak kod erişimiyle gizli bilgi ifşa olabilir.",
            'import os; DB_PASSWORD = os.environ["DB_PASSWORD"]  # gerçek sır çevre değişkeninden',
        ),
        "command_injection.py": (
            "Kullanıcı girdisi kabuğa verilen komutla birleştiriliyor.",
            "Ek kabuk komutlarının çalıştırılması mümkün olabilir.",
            'from pathlib import Path; entries = list(Path(klasor_adi).iterdir())  # shell kullanma',
        ),
        "path_traversal.py": (
            "Kullanıcıdan gelen dosya adıyla oluşturulan yol, izin verilen uploads dizininde kaldığı denetlenmeden açılıyor.",
            "../ gibi dizin geçişleri ile uploads dışındaki dosyalar okunabilir.",
            'root = Path("uploads").resolve()\ntarget = (root / filename).resolve()\nif not target.is_relative_to(root):\n    raise ValueError("Dizin dışına erişim engellendi")\nreturn target.read_text(encoding="utf-8")',
        ),
        "unsafe_deserialization.py": (
            "İstemciden gelen doğrulanmamış request_body baytları pickle.loads ile açılıyor.",
            "Kötü niyetli pickle nesnesi beklenmeyen kod çalıştırabilir.",
            'import json\ndata = json.loads(request_body.decode("utf-8"))  # veri şemasını da doğrula',
        ),
    }
    cause, impact, secure_code = DETAILS[stem]
    return json.dumps({"findings": [{
        "type": finding_type,
        "severity": severity,
        "evidence": evidence,
        "cause": cause,
        "impact": impact,
        "secure_code": secure_code,
    }]}, ensure_ascii=False)


class TestSecurityAnalyzer(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.output = self.root / "reports" / "analysis.json"

    def test_six_source_files_are_present(self):
        for name in analyzer.ALL_SAMPLES:
            path = analyzer.PROJECT_DIR / "samples" / name
            with self.subTest(name=name):
                self.assertTrue(path.is_file())
                self.assertTrue(analyzer.read_python_file(path))

    def test_six_scenarios_through_full_pipeline_with_mocked_gemini(self):
        for name in analyzer.ALL_SAMPLES:
            with self.subTest(name=name):
                path = analyzer.PROJECT_DIR / "samples" / name
                with patch.object(analyzer, "request_gemini", return_value=mocked_response(name)) as fake:
                    report = analyzer.analyze_one(path, report_path=self.output)
                    fake.assert_called_once()
                self.assertEqual(report["finding_count"], 0 if name == "safe_code.py" else 1)
                loaded = json.loads(self.output.read_text(encoding="utf-8"))
                self.assertEqual(loaded, report)
                self.assertEqual(sum(report["risk_summary"].values()), report["finding_count"])
                if name == "safe_code.py":
                    self.assertEqual(report["findings"], [])
                else:
                    self.assertEqual(report["findings"][0]["type"], EXPECTED[name][0])
                    self.assertEqual(report["findings"][0]["severity"], EXPECTED[name][1])
                    self.assertTrue(all(key in report["findings"][0] for key in analyzer.REQUIRED_FIELDS))

    def test_source_code_not_executed_while_reading_and_analyzing(self):
        marker = self.root / "unsafe_execution_marker.txt"
        test_file = self.root / "do_not_run.py"
        test_file.write_text(f"from pathlib import Path\nPath({str(marker)!r}).write_text('EXECUTED')\n", encoding="utf-8")
        with patch.object(analyzer, "request_gemini", return_value='{"findings": []}'):
            analyzer.analyze_one(test_file, report_path=self.output)
        self.assertFalse(marker.exists(), "Kaynak dosya yanlışlıkla çalıştırıldı!")

    def test_nonexistent_file_does_not_call_model(self):
        with patch.object(analyzer, "request_gemini") as fake:
            with self.assertRaisesRegex(analyzer.AnalyzerError, "Dosya bulunamadı"):
                analyzer.analyze_one(self.root / "missing.py", report_path=self.output)
            fake.assert_not_called()
        self.assertFalse(self.output.exists())

    def test_wrong_extension_does_not_call_model(self):
        wrong = self.root / "file.txt"
        wrong.write_text("print('hi')", encoding="utf-8")
        with patch.object(analyzer, "request_gemini") as fake:
            with self.assertRaisesRegex(analyzer.AnalyzerError, r"\.py"):
                analyzer.analyze_one(wrong, report_path=self.output)
            fake.assert_not_called()

    def test_directory_ending_py_does_not_call_model(self):
        folder = self.root / "folder.py"
        folder.mkdir()
        with patch.object(analyzer, "request_gemini") as fake:
            with self.assertRaisesRegex(analyzer.AnalyzerError, "bir dosya değil"):
                analyzer.analyze_one(folder, report_path=self.output)
            fake.assert_not_called()

    def test_blank_file_does_not_call_model(self):
        blank = self.root / "empty.py"
        blank.write_text("\n  \n", encoding="utf-8")
        with patch.object(analyzer, "request_gemini") as fake:
            with self.assertRaisesRegex(analyzer.AnalyzerError, "boş"):
                analyzer.analyze_one(blank, report_path=self.output)
            fake.assert_not_called()

    def test_invalid_utf8_does_not_call_model(self):
        bad = self.root / "bad.py"
        bad.write_bytes(b"\xff\xfe\xfd")
        with patch.object(analyzer, "request_gemini") as fake:
            with self.assertRaisesRegex(analyzer.AnalyzerError, "UTF-8"):
                analyzer.analyze_one(bad, report_path=self.output)
            fake.assert_not_called()

    def test_unreadable_file_does_not_call_model(self):
        path = self.root / "unreadable.py"
        path.write_text("x = 1", encoding="utf-8")
        with patch.object(Path, "read_text", side_effect=PermissionError("Permission denied")):
            with patch.object(analyzer, "request_gemini") as fake:
                with self.assertRaisesRegex(analyzer.AnalyzerError, "Dosya okunamadı"):
                    analyzer.analyze_one(path, report_path=self.output)
                fake.assert_not_called()

    def test_api_connection_error_does_not_save_report(self):
        path = analyzer.PROJECT_DIR / "samples" / "safe_code.py"
        with patch.object(analyzer, "request_gemini", side_effect=analyzer.AnalyzerError("API bağlantı hatası")):
            with self.assertRaisesRegex(analyzer.AnalyzerError, "API bağlantı"):
                analyzer.analyze_one(path, report_path=self.output)
        self.assertFalse(self.output.exists())

    def test_non_json_response_does_not_save_report(self):
        path = analyzer.PROJECT_DIR / "samples" / "safe_code.py"
        with patch.object(analyzer, "request_gemini", return_value="JSON değil <h1>Hata</h1>"):
            with self.assertRaisesRegex(analyzer.AnalyzerError, "geçerli JSON değil"):
                analyzer.analyze_one(path, report_path=self.output)
        self.assertFalse(self.output.exists())

    def test_missing_required_fields_do_not_save_report(self):
        path = analyzer.PROJECT_DIR / "samples" / "safe_code.py"
        with patch.object(analyzer, "request_gemini", return_value='{"findings": [{"type":"SQL Injection"}]}'):
            with self.assertRaisesRegex(analyzer.AnalyzerError, "severity"):
                analyzer.analyze_one(path, report_path=self.output)
        self.assertFalse(self.output.exists())

    def test_invalid_risk_does_not_save_report(self):
        response = mocked_response("path_traversal.py").replace('"Yüksek"', '"Devasa"')
        path = analyzer.PROJECT_DIR / "samples" / "path_traversal.py"
        with patch.object(analyzer, "request_gemini", return_value=response):
            with self.assertRaisesRegex(analyzer.AnalyzerError, "risk seviyesi geçersiz"):
                analyzer.analyze_one(path, report_path=self.output)
        self.assertFalse(self.output.exists())

    def test_missing_api_key_stops_before_gemini_import(self):
        from unittest.mock import patch as mock_patch
        with mock_patch.dict("os.environ", {"GEMINI_API_KEY": ""}):
            with self.assertRaisesRegex(analyzer.AnalyzerError, "GEMINI_API_KEY"):
                analyzer.request_gemini("x = 1", "safe_code.py")


if __name__ == "__main__":
    unittest.main()
