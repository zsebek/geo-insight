from fastapi import APIRouter
from services.plotting import plot_points_vs_time
import io
from fastapi.responses import StreamingResponse

router = APIRouter()

@router.get("/points_vs_time")
def get_points_vs_time(ncfa: str):
    """Generates and returns a Points vs. Time scatter plot."""
    fig = plot_points_vs_time(ncfa)

    img = io.BytesIO()
    fig.savefig(img, format="png")
    img.seek(0)

    return StreamingResponse(img, media_type="image/png")
