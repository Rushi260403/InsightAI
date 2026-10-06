import os
import shutil

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Dataset
from app.dependencies import get_current_user
from app.services.dataset_service import (
    load_user_dataset,
    generate_dataset_profile,
    clean_user_dataset
)


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

@router.get("/{dataset_id}/load")
def load_dataset(
    dataset_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user["user_id"]

    try:
        dataset, dataframe = load_user_dataset(
            dataset_id,
            user_id,
            db
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    return {
        "message": "Dataset loaded successfully",
        "dataset_id": dataset.id,
        "dataset_name": dataset.dataset_name,
        "rows": len(dataframe),
        "columns": len(dataframe.columns),
        "column_names": list(dataframe.columns)
    }

@router.get("/{dataset_id}/profile")
def profile_dataset(
    dataset_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user["user_id"]

    try:
        result = generate_dataset_profile(
            dataset_id,
            user_id,
            db
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    return result

@router.get("/{dataset_id}/clean")
def clean_dataset(
    dataset_id: int,
    missing_value_strategy: str = "median",
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_id = current_user["user_id"]

    # Check strategy
    if missing_value_strategy not in [
        "mean",
        "median",
        "mode"
    ]:
        raise HTTPException(
            status_code=400,
            detail="Strategy must be mean, median, or mode"
        )

    try:
        result = clean_user_dataset(
            dataset_id,
            user_id,
            db,
            missing_value_strategy
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    dataframe = result["data"]

    dataframe = dataframe.astype(object).where(
    dataframe.notna(),
    None
    )

    return {
        "message": "Dataset cleaned successfully",
        "dataset_id": result["dataset_id"],
        "dataset_name": result["dataset_name"],
        "original_rows": result["original_rows"],
        "cleaned_rows": result["cleaned_rows"],
        "original_columns": result["original_columns"],
        "cleaned_columns": result["cleaned_columns"],
        "duplicates_removed": result["duplicates_removed"],
        "missing_value_strategy": result[
            "missing_value_strategy"
        ],
        "columns": list(dataframe.columns),
        "data": dataframe.where(
            dataframe.notna(),
            None
            ).to_dict(
                orient="records"
            )
    }