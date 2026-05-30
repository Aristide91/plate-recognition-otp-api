import easyocr
import numpy as np
from PIL import Image
import io
import re

class OCRService:
    def __init__(self, languages: list[str] = ["en", "ar"]):
        self.reader = easyocr.Reader(languages)

    def _clean_ocr_result(self, text: str, pattern: str) -> str:
        """Cleans OCR results by correcting common misinterpretations."""
        text = text.upper().strip()
        if pattern == 'alpha':
            # Correct common OCR errors for letters
            text = text.replace('8', 'B').replace('0', 'O').replace('1', 'I').replace('5', 'S').replace('4', 'A')
            # Remove non-alphabetic characters if it should be strictly alpha
            text = re.sub(r'[^A-Z]', '', text)
        elif pattern == 'numeric':
            # Correct common OCR errors for numbers
            text = text.replace('B', '8').replace('O', '0').replace('I', '1').replace('S', '5').replace('A', '4').replace('G', '6')
            # Remove non-numeric characters
            text = re.sub(r'[^0-9]', '', text)
        return text

    async def analyze_registration_document(self, image_bytes: bytes) -> dict:
        raw_text = ""
        plate_number = None
        vin = None
        country = None

        try:
            image = Image.open(io.BytesIO(image_bytes))
            image_np = np.array(image)
            results = self.reader.readtext(image_np)

            if results:
                raw_text = " ".join([text for (bbox, text, prob) in results])
                
                # --- VIN (Châssis) ---
                # Search for 17 alphanumeric characters (standard VIN)
                vin_search_text = re.sub(r'[\s-]', '', raw_text).upper()
                # We look for a 17-char string that looks like a VIN (avoiding I, O, Q which are not allowed in modern VINs)
                vin_candidates = re.findall(r'[A-HJ-NPR-Z0-9]{17}', vin_search_text)
                if not vin_candidates:
                    # Fallback for slightly misread VINs
                    vin_candidates = re.findall(r'[A-Z0-9]{17}', vin_search_text)
                
                for candidate in vin_candidates:
                    # Check if it has a mix of letters and numbers typical of VINs
                    if any(c.isalpha() for c in candidate) and any(c.isdigit() for c in candidate):
                        vin = candidate
                        break

                # --- Plaque France/EU (Format AA-123-AA) ---
                plate_fr_eu_match = re.search(r'([A-Z]{2})[\s-]*(\d{3})[\s-]*([A-Z]{2})', raw_text, re.IGNORECASE)
                if plate_fr_eu_match:
                    g = plate_fr_eu_match.groups()
                    part1 = self._clean_ocr_result(g[0], 'alpha')
                    part2 = self._clean_ocr_result(g[1], 'numeric')
                    part3 = self._clean_ocr_result(g[2], 'alpha')
                    plate_number = f"{part1}-{part2}-{part3}"
                    country = "France/EU"
                
                # --- Plaque Tunisie (Format 123 تونس 4567 or 123 TUN 4567) ---
                # Improved regex to handle variations and potential misreads of "تونس" or "TUN"
                plate_tn_match = re.search(r'(\d{1,4})\s?(TUN|تونس|TUNISIE|TUNIS)\s?(\d{1,5})', raw_text, re.IGNORECASE)
                if not plate_number and plate_tn_match:
                    g = plate_tn_match.groups()
                    num1 = self._clean_ocr_result(g[0], 'numeric')
                    num2 = self._clean_ocr_result(g[2], 'numeric')
                    
                    # Map both versions to "TUN" as requested
                    indicator = "TUN"
                    
                    plate_number = f"{num1} {indicator} {num2}"
                    country = "Tunisia"
                
                # Fallback for Tunisian plate without the "TUN" word (just two numbers)
                if not plate_number:
                    # Look for two numeric blocks separated by space or noise, often seen on Tunisian plates
                    tn_blocks = re.findall(r'\b\d{2,4}\b', raw_text)
                    if len(tn_blocks) >= 2:
                        # This is speculative but might help if "TUN" is missing
                        # We'll only use this if we have high confidence or no other match
                        pass 

                # --- Plaque Maroc (Formats XXXXX A XX or XXXXX XX) ---
                plate_ma_pattern_letter = re.compile(r'(\d{1,5})\s*([A-Z])\s*(\d{1,2})', re.IGNORECASE)
                plate_ma_match_letter = plate_ma_pattern_letter.search(raw_text)

                if not plate_number and plate_ma_match_letter:
                    g = plate_ma_match_letter.groups()
                    num1 = self._clean_ocr_result(g[0], 'numeric')
                    letter = self._clean_ocr_result(g[1], 'alpha')
                    num2 = self._clean_ocr_result(g[2], 'numeric')
                    plate_number = f"{num1} {letter} {num2}"
                    country = "Morocco"
                
                if not plate_number:
                    plate_ma_pattern_numeric = re.compile(r'(\d{1,5})\s*(\d{1,2})', re.IGNORECASE)
                    plate_ma_match_numeric = plate_ma_pattern_numeric.search(raw_text)
                    if plate_ma_match_numeric:
                        g = plate_ma_match_numeric.groups()
                        num1 = self._clean_ocr_result(g[0], 'numeric')
                        num2 = self._clean_ocr_result(g[1], 'numeric')
                        plate_number = f"{num1} {num2}"
                        country = "Morocco"

        except Exception as e:
            print(f"Erreur lors de l'analyse OCR de la carte grise: {e}")
        
        return {"plate": plate_number, "vin": vin, "country": country, "raw_text": raw_text}

ocr_service = OCRService()
