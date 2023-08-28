from typing import Optional, Union, Any
from enum import Enum
from uuid import uuid4

# from redis_om import HashModel, VectorFieldOptions, Field
from pydantic import BaseModel, ValidationError, field_validator, constr, Field

from models.db.addressModels import Address

class AddAddress(BaseModel):
    data: Address

class UpdateAddress(BaseModel):
    key: str    
    data: Address