# File Upload and Download with FastAPI and MinIO

This repository demonstrates how to implement file upload and file download functionalities using FastAPI, a modern web framework for building APIs with Python, integrated with MinIO, an object storage server compatible with Amazon S3.

## Prerequisites

* All of this is part of the requirements so no need to install them since its dockerized.
- Python (3.7 or later)
- FastAPI (`pip install fastapi`)
- MinIO client (`pip install minio`)
- Docker (Mandatory, for running MinIO locally using Docker)

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/davidkrdona/fastapi-minio-file-upload-download.git
   cd fastapi-minio-file-upload-download

2. Go to `files/` and run `docker-compose up -d`
3. Check dockers are running with `docker ps`
4. You should be able to check the api docs here http://localhost:8000/docs#/
### NOTE: Just in case it wont open in that url,  check the IP for the FastApi docker `files_files_app` with `docker inspect <docker-id> ` and use the value under `IPAddress` field.
Eg:
`"Gateway": "172.22.0.1, "IPAddress": "172.22.0.2", "IPPrefixLen": 16,`

You will open http://172.22.0.2:8000/docs#/

5. Update this line `app/lib/helpers/minio.py:11` with the new IP value extracted from the attached screenshot, copy the ip withih the characters "<>" and replace it in the code.

```
Status:         1 Online, 0 Offline. 
S3-API: => http:<//172.23.0.3:9000> <=  http://127.0.0.1:9000 
Console: http://172.23.0.2:9001 http://127.0.0.1:9001 
```
Then restart the python `files_files_app` docker with `docker restart <docker-id>`

### NOTE: To access the MinIO browser we could face the same problem as before so please access on `http://localhost:9001/browser` or `http://172.22.0.3:9001/browser` assuming this was the IP get by using `docker logs -f <docker-id>`   

![](files/assets/docker_minio.png)

6. Once this has been done you'll have the API up and running you can open the docs and test directly the API. Try upload and download files.

## License
This project is licensed under the MIT License.
