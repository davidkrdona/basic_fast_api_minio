from fastapi import FastAPI, File, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse

from minio.error import S3Error

import logging

from lib.helpers.minio import MinioHelper
from lib.models.models import FileOut

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post(
    "/upload",
    response_model=FileOut,
    status_code=status.HTTP_200_OK,
)
def upload_file(bucket_name: str, object_name: str, file: UploadFile = File(...)):
    """
    Uploads a file to the specified bucket and object in a MinIO server.

    Args:
    - bucket_name (str): The name of the bucket in the MinIO server.
    - object_name (str): The name of the object to be uploaded.
    - file (UploadFile): The file to be uploaded.

    Returns:
    - FileOut: A response model representing the uploaded file details.

    Raises:
    - HTTPException: If there's an error while uploading or processing the file.
    """
    try:
        minio_helper = MinioHelper(bucket_name=bucket_name)
        minio_helper.check_bucket()
    except Exception as err:
        logging.error(f"Something went wrong {err} while checking bucket {bucket_name}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from err

    logging.info(f"File {object_name} will be uploaded to bucket '{bucket_name}'")

    try:
        file_out = FileOut(
            file_name=minio_helper.upload_object(file=file, object_name=object_name)
        )
    except Exception as err:
        logging.error(
            f"Something went wrong {err} while uploading file {object_name} to bucket {bucket_name}"
        )
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from err

    return file_out


@app.get(
    "/file/{bucket_name}/{object_name}",
    status_code=status.HTTP_200_OK,
)
def get_file(bucket_name: str, object_name: str):
    """
       Download a file from MinIO given the bucket name and object name.

       Args:
       - bucket_name (str): The name of the bucket in the MinIO server.
       - object_name (str): The name of the object to be downloaded.

       Returns:
       - StreamingResponse: A streaming response containing the file data.

       If the file is not found or an error occurs during retrieval, an error response will be returned.
       """
    try:
        minio_helper = MinioHelper(bucket_name=bucket_name)
        minio_helper.check_bucket()
    except Exception as err:
        logging.error(f"Something went wrong {err} while checking bucket {bucket_name}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from err

    logging.info(f"File {object_name} will be downloaded from bucket '{bucket_name}'")
    try:
        # Get the object
        file_data = minio_helper.minio_client.get_object(bucket_name, object_name)

        # Set headers for the response
        return StreamingResponse(
            iter(file_data),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={object_name}"},
        )
    except S3Error:
        return {"error": f"There is no file named {object_name} in bucket {bucket_name}"}
    except Exception as err:
        logging.error(
            f"Something went wrong {err} while downloading file {object_name} to bucket {bucket_name}"
        )
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from err
