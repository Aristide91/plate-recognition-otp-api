from fastapi import APIRouter
from app.database import create_connection, get_all_reservations

router = APIRouter()

@router.get("/reservations", summary="Get all reservations")
async def read_reservations():
    conn = create_connection()
    if conn:
        reservations = get_all_reservations(conn)
        conn.close()
        # Convert list of tuples to list of dicts for JSON response
        return [
            {
                "id": res[0],
                "plate": res[1],
                "vin": res[2],
                "phone": res[3],
                "status": res[4],
                "timestamp": res[5],
            }
            for res in reservations
        ]
    return []
