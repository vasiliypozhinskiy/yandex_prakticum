from typing import Optional
from uuid import UUID

import orjson
from pydantic import BaseModel, validator

def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class CommonMixin(BaseModel):
    id: str

    @validator('id')
    def dash_in_id(self, my_id: str) -> str:
        if '-' not in id:
            raise ValueError('Проверьте id')
        return my_id

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
