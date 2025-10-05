from fastapi import APIRouter, Query, Path,status,HTTPException
import json

router = APIRouter(
    tags=['products']
)

def load_products_file():
    try:
        with open('src/data/db.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Products file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Products file is invalid")

@router.get('/444/products', status_code=status.HTTP_200_OK)
async def get_all_products(name_like: str = Query(None)):
    all_products = load_products_file()
    products = all_products.get("products", [])
    if name_like:
        products = [p for p in products if name_like.lower() in p["name"].lower()]
    return products

@router.get("/444/products/{id}", status_code=status.HTTP_200_OK)
async def get_product(id: int = Path(..., description="ID of the product")):
    all_products = load_products_file()
    products = all_products.get("products", [])
    product = next((p for p in products if p["id"] == id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get('/444/featured_products', status_code=status.HTTP_200_OK)
async def get_featured_products():
    all_products = load_products_file()
    featured = all_products.get("featured_products", [])
    if not featured:
        raise HTTPException(status_code=404, detail="No featured products found")
    return featured