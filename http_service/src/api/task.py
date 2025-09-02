import uuid
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
import json
from fastapi.responses import StreamingResponse
from typing import Annotated
import io
from http_service.src.schemas.exceptions import NotFoundError
from shared.schemas.schemas import FilterParameters
from http_service.src.usecases.abstract_task_service import AbstractTaskService
from http_service.src.dependencies.task_depend import get_task_service
from http_service.src.api.middleware import get_current_session

router = APIRouter(dependencies=[Depends(get_current_session)], )
router2 = APIRouter()


@router.post("/task", status_code=status.HTTP_201_CREATED)
async def create_task(service: Annotated[AbstractTaskService, Depends(get_task_service)],
                      file: UploadFile = File(...),
                      filter_json: str = Form(...)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail={"Error": f"Unsupported file type: '{file.content_type}'. "
                              f"Only image/jpeg, image/png are allowed."}
        )

    max_file_size = 10 * 1024 * 1024
    image_data = await file.read()
    if len(image_data) > max_file_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail={"Error": "File size exceeds 10 MB limit."}
        )

    try:
        filter_data = json.loads(filter_json)
        filter_obj = FilterParameters(**filter_data)
    except (json.JSONDecodeError, TypeError, ValueError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"Error": f"Invalid filter JSON: {str(e)}"}
        )

    try:
        task_id = await service.create_task(image_data, filter_obj)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"Error": f"Task creation failed: {str(e)}"}
        )
    return {"task_id": task_id}


@router.get("/status/{task_id}")
async def get_task_status(task_id: uuid.UUID, service: Annotated[AbstractTaskService, Depends(get_task_service)]):
    try:
        task_status = await service.get_task_status(task_id)
        return {"status": task_status}
    except NotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
            headers={"Error": "Task not found"}
        )


@router.get("/result/{task_id}")
async def get_task_result(task_id: uuid.UUID, service: Annotated[AbstractTaskService, Depends(get_task_service)]):
    try:
        result = await service.get_task_result(task_id)
        return StreamingResponse(
            io.BytesIO(result),
            media_type="image/jpeg"
        )
    except NotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
            headers={"Error": "Task not found"}
        )
