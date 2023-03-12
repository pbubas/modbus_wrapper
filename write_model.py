from pydantic import BaseModel, validator
from typing import Union, List
from fatek_address import FatekAddress


class WriteModel(BaseModel):
    fatek_address: str
    value: Union[List[bool], List[int], bool, int]

    @validator("fatek_address")
    def validate_fatek_address(cls, fatek_address):
        return FatekAddress(fatek_address)

