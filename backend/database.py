from typing import List
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

from models import Product, Company, UserLogin, UserSignUp, CompanySignUp

client = AsyncIOMotorClient('mongodb://mongo:27017')
db = client.db
users_collection = db.users
company_users_collection = db.company_users
products_collection = db.products
companies_collection = db.companies

async def get_user_from_db(user_id: str):
    return await users_collection.find_one({"id": user_id})

async def get_company_user_from_db(company_user_id: str):
    return await company_users_collection.find_one({"id": company_user_id})

async def save_customer_user_to_db(user: UserSignUp):
    await users_collection.insert_one(user.dict())

async def save_company_user_to_db(company_user: CompanySignUp):
    await company_users_collection.insert_one(company_user.dict())

async def get_all_companies_from_db():
    cursor = companies_collection.find({})
    companies = await cursor.to_list(length=100)
    return [Company(**company) for company in companies]

async def get_all_company_products_from_db(company_id: int):
    company = await companies_collection.find_one({"id": company_id})
    if company:
        return [Product(**product) for product in company.get('products', [])]
    return []

async def get_company_from_db(company_id: int):
    return await companies_collection.find_one({"id": company_id})

async def get_product_from_db(product_id: int):
    return await products_collection.find_one({"id": product_id})

async def create_company_in_db(company: Company):
    await companies_collection.insert_one(company.dict())

async def create_product_in_db(product: Product):
    await products_collection.insert_one(product.dict())

async def update_company_in_db(company_id: int, company: Company):
    result = await companies_collection.update_one({"id": company_id}, {"$set": company.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Company not found")
    return result

async def update_product_in_db(product_id: int, product: Product):
    result = await products_collection.update_one({"id": product_id}, {"$set": product.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return result

async def delete_company_from_db(company_id: int):
    result = await companies_collection.delete_one({"id": company_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Company not found")
    return result

async def delete_product_from_db(product_id: int):
    result = await products_collection.delete_one({"id": product_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return result

async def update_product_purchase_count(product_id: int, increment: int):
    result = await products_collection.update_one(
        {"id": product_id},
        {"$inc": {"purchase_count": increment}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return result

async def create_purchase(purchase: Purchase):
    for product in purchase.products:
        await update_product_purchase_count(product.id, 1)
    await purchases_collection.insert_one(purchase.dict())

async def get_company_product_insights(company_id: int):
    company = await companies_collection.find_one({"id": company_id})
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    products = company.get('products', [])
    return [{"name": product['name'], "purchase_count": product['purchase_count']} for product in products]
