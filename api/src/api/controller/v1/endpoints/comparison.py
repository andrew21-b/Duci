from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session
from src.api.db.connection import get_session
from src.api.models.comparison import Comparison
from src.api.services.comparisson_service import compare_images, generate_image_paths, get_comparison_by_id, initialize_comparison_resources

router = APIRouter()


@router.post("/")
async def create_comparison(
    before: UploadFile = File(...),
    after: UploadFile = File(...),
    threshold: int = Form(30),
    db: Session = Depends(get_session)
):
    comp_id, comp_dir = initialize_comparison_resources()

    before_path, after_path, diff_path = generate_image_paths(comp_dir)

    with open(before_path, "wb") as f:
        f.write(await before.read())
    with open(after_path, "wb") as f:
        f.write(await after.read())

    diff_score = compare_images(before_path, after_path, diff_path, threshold)

    comparison = Comparison(
        id = comp_id,
        before_image = before_path,
        after_image = after_path,
        diff_image = diff_path,
        pixel_difference = diff_score
    )
    db.add(comparison)
    db.commit()
    db.refresh(comparison)

    return {
        "id": comp_id,
        "difference_score": diff_score,
        "diff_image_url": f"/comparison/{comp_id}/diff.png"
    }

@router.get("/{comp_id}")
def get_comparison(comp_id: str, db: Session = Depends(get_session)):
    comparison = get_comparison_by_id(comp_id, db)

    return {
        "id": comparison.id,
        "difference_score": comparison.pixel_difference,
        "diff_image_url": f"/comparison/{comp_id}/diff.png",
        "created_at": comparison.created_at
    }




