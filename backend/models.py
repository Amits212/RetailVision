from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

class Product(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image: Optional[str] = None
    purchase_count: int = 0

class Company(BaseModel):
    name: str
    description: Optional[str] = None
    image: Optional[str] = None
    products: Optional[List[Product]] = []

class UserLogin(BaseModel):
    username: str
    password: str

class UserSignUp(UserLogin):
    first_name: str
    last_name: str
    address: str
    email: EmailStr

class CompanySignUp(UserLogin):
    company: Company

class Purchase(BaseModel):
    products: List[Product]
    date: datetime = Field(default_factory=datetime.utcnow)

    @property
    def quantity(self):
        return len(self.products)

    @property
    def total_price(self):
        return sum([p.price for p in self.products])
