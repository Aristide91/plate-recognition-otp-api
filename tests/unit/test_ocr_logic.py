import unittest
from unittest.mock import MagicMock
from app.services.ocr_service import OCRService

class TestOCRService(unittest.TestCase):
    def setUp(self):
        # On évite d'initialiser EasyOCR pour les tests unitaires de logique
        self.service = OCRService.__new__(OCRService)
    
    def test_clean_ocr_result_alpha(self):
        self.assertEqual(self.service._clean_ocr_result("8O1", "alpha"), "BOI")

    def test_clean_ocr_result_numeric(self):
        self.assertEqual(self.service._clean_ocr_result("BOIS", "numeric"), "8015")

    def test_plate_extraction_fr(self):
        # Simuler un résultat d'OCR pour une plaque française
        raw_text = "CARTE GRISE AA-123-AA NOM DU TITULAIRE"
        # On va tester la logique d'extraction manuellement car analyze_registration_document
        # utilise readtext qui est une méthode de l'objet reader.
        import re
        plate_fr_eu_match = re.search(r'([A-Z]{2})[\s-]*(\d{3})[\s-]*([A-Z]{2})', raw_text, re.IGNORECASE)
        self.assertIsNotNone(plate_fr_eu_match)
        g = plate_fr_eu_match.groups()
        plate = f"{g[0]}-{g[1]}-{g[2]}"
        self.assertEqual(plate, "AA-123-AA")

if __name__ == '__main__':
    unittest.main()
