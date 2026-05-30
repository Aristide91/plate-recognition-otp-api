from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.services.ocr_service import ocr_service
from app.core.security import get_current_user

router = APIRouter()

@router.post("/analyze-registration-doc", summary="Analyze vehicle registration document for plate and VIN", response_model=dict)
async def analyze_registration_document(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Upload an image file of a vehicle registration document.
    The image will be processed by the OCR service to extract the license plate number,
    the VIN (Vehicle Identification Number), and the full raw text.
    Requires authentication.
    """
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Invalid file type. Only images are allowed.")

    try:
        image_bytes = await file.read()
        analysis_results = await ocr_service.analyze_registration_document(image_bytes)

        if analysis_results["plate"] or analysis_results["vin"] or analysis_results["raw_text"]:
            return analysis_results
        else:
            raise HTTPException(status_code=404, detail="No recognizable information found in the document.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process registration document: {e}")
