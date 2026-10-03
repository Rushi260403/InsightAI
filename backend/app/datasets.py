import os
import shutil

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Dataset
from app.dependencies import get_current_user


router = APIRouter(
    prefix="/datasets",
    tags=["Datasets"]
)


UPLOAD_FOLDER = r"D:\InsightAI\datasets\uploads"


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/upload")
def upload_dataset(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    allowed_extensions = [".csv", ".xlsx", ".xls"]

    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only CSV and Excel files are allowed"
        )

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    user_id = current_user["user_id"]

    file_path = os.path.join(
        UPLOAD_FOLDER,
        f"user_{user_id}_{file.filename}"
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_dataset = Dataset(
        user_id=user_id,
        dataset_name=os.path.splitext(file.filename)[0],
        file_name=file.filename,
        file_type=file_extension,
        file_path=file_path
    )

    db.add(new_dataset)
    db.commit()
    db.refresh(new_dataset)

    return {
        "message": "Dataset uploaded successfully",
        "dataset_id": new_dataset.id,
        "user_id": new_dataset.user_id,
        "dataset_name": new_dataset.dataset_name,
        "file_name": new_dataset.file_name,
        "file_type": new_dataset.file_type
    }

@router.get("/my")
def get_my_datasets(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user["user_id"]

    datasets = db.query(Dataset).filter(
        Dataset.user_id == user_id
    ).all()

    return {
        "user_id": user_id,
        "total_datasets": len(datasets),
        "datasets": [
            {
                "dataset_id": dataset.id,
                "dataset_name": dataset.dataset_name,
                "file_name": dataset.file_name,
                "file_type": dataset.file_type,
                "uploaded_at": dataset.uploaded_at
            }
            for dataset in datasets
        ]
    }

@router.get("/{dataset_id}")
def get_dataset(
    dataset_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user["user_id"]

    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id,
        Dataset.user_id == user_id
    ).first()

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    return {
        "dataset_id": dataset.id,
        "user_id": dataset.user_id,
        "dataset_name": dataset.dataset_name,
        "file_name": dataset.file_name,
        "file_type": dataset.file_type,
        "file_path": dataset.file_path,
        "uploaded_at": dataset.uploaded_at
    }

@router.get("/{dataset_id}/file")
def download_dataset(
    dataset_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user["user_id"]

    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id,
        Dataset.user_id == user_id
    ).first()

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    if not os.path.exists(dataset.file_path):
        raise HTTPException(
            status_code=404,
            detail="Dataset file not found"
        )

    return FileResponse(
        path=dataset.file_path,
        filename=dataset.file_name,
        media_type="application/octet-stream"
    )

@router.delete("/{dataset_id}")
def delete_dataset(
    dataset_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user["user_id"]

    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id,
        Dataset.user_id == user_id
    ).first()

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    # Delete the physical file
    if os.path.exists(dataset.file_path):
        os.remove(dataset.file_path)

    # Delete database record
    db.delete(dataset)
    db.commit()

    return {
        "message": "Dataset deleted successfully",
        "dataset_id": dataset_id
    }