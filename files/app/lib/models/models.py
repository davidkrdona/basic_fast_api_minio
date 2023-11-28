import pydantic


class FileOut(pydantic.BaseModel):
    file_name: str
