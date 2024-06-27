from fastapi import APIRouter, Body, HTTPException, status, Depends
from models import Product, Company, UserLogin, UserSignUp, CompanySignUp, Purchase
from database import (
    save_customer_user_to_db,
    save_company_user_to_db,
    get_user_from_db,
    get_company_user_from_db,
    get_all_companies_from_db,
    get_all_company_products_from_db,
    get_company_from_db,
    get_product_from_db,
    create_company_in_db,
    create_product_in_db,
    update_company_in_db,
    update_product_in_db,
    delete_company_from_db,
    delete_product_from_db,
    get_company_product_insights,
    create_purchase
)
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/api/companies")
async def get_all_companies():
    companies = await get_all_companies_from_db()
    return companies

@router.get("/api/{company_id}/products")
async def get_all_company_products(company_id: str):
    products = await get_all_company_products_from_db(company_id=company_id)
    return products

@router.get("/api/companies/{company_id}")
async def get_company(company_id: str):
    company = await get_company_from_db(company_id=company_id)
    if company:
        return company
    raise HTTPException(status_code=404, detail="Company not found")

@router.get("/api/products/{product_id}")
async def get_product(product_id: str):
    product = await get_product_from_db(product_id=product_id)
    if product:
        return product
    raise HTTPException(status_code=404, detail="Product not found")

@router.post("/api/products")
async def create_product(company_id: str, product: Product):
    await create_product_in_db(company_id=company_id, product=product)
    return {"message": "Product created successfully"}

@router.put("/api/companies/{company_id}")
async def update_company(company_id: str, company: Company):
    await update_company_in_db(company_id=company_id, company=company)
    return {"message": "Company updated successfully"}

@router.put("/api/products/{product_id}")
async def update_product(product_id: str, product: Product):
    await update_product_in_db(product_id=product_id, product=product)
    return {"message": "Product updated successfully"}

@router.delete("/api/companies/{company_id}")
async def delete_company(company_id: str):
    await delete_company_from_db(company_id=company_id)
    return {"message": "Company deleted successfully"}

@router.delete("/api/products/{product_id}")
async def delete_product(product_id: str):
    await delete_product_from_db(product_id=product_id)
    return {"message": "Product deleted successfully"}

@router.post("/api/purchases")
async def create_user_purchase(purchase: Purchase):
    await create_purchase(purchase)
    return {"message": "Purchase created successfully"}

@router.get("/api/companies/{company_id}/insights")
async def get_product_insights(company_id: str):
    insights = await get_company_product_insights(company_id)
    return insights

@router.post("/api/login")
async def login(user: UserLogin):
    user_in_db = await get_user_from_db(user.username)
    if user_in_db and pwd_context.verify(user.password, user_in_db['password']):
        return {"message": "Login successful"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
    )

@router.post("/api/companylogin")
async def company_login(user: UserLogin):
    company_user_in_db = await get_company_user_from_db(user.username)
    if company_user_in_db and pwd_context.verify(user.password, company_user_in_db['password']):
        return {"message": "Login successful"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
    )

@router.post("/api/signup")
async def sign_up(user: UserSignUp):
    user.password = pwd_context.hash(user.password)
    await save_customer_user_to_db(user)
    return {"message": "User signed up successfully"}

@router.post("/api/companysignup")
async def company_sign_up(company_user: CompanySignUp):
    company_user.password = pwd_context.hash(company_user.password)
    await save_company_user_to_db(company_user)
    return {"message": "Company user signed up successfully"}
