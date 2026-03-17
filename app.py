from fastapi import FastAPI, HTTPException, Request, Response, Depends, Header
from models import UserCreate, CommonHeaders, LoginRequest  # Добавлен LoginRequest
from typing import Optional
import uuid
import time
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

app = FastAPI()

# ===== Данные =====
sample_products = [
    {"product_id": 123, "name": "Smartphone", "category": "Electronics", "price": 599.99},
    {"product_id": 456, "name": "Phone Case", "category": "Accessories", "price": 19.99},
    {"product_id": 789, "name": "Iphone", "category": "Electronics", "price": 1299.99},
    {"product_id": 101, "name": "Headphones", "category": "Accessories", "price": 99.99},
    {"product_id": 202, "name": "Smartwatch", "category": "Electronics", "price": 299.99},
]

SECRET_KEY = "super-secret-key"
serializer = URLSafeTimedSerializer(SECRET_KEY)

fake_user = {
    "username": "user123",
    "password": "password123"
}

# ===== Задание 3.1 =====
@app.post("/create_user")
def create_user(user: UserCreate):
    return user


# ===== Задание 3.2 =====
@app.get("/product/{product_id}")
def get_product(product_id: int):
    for product in sample_products:
        if product["product_id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")


@app.get("/products/search")
def search_products(keyword: str, category: Optional[str] = None, limit: int = 10):
    result = []

    for product in sample_products:
        if keyword.lower() in product["name"].lower():
            if category and product["category"] != category:
                continue
            result.append(product)

    return result[:limit]


# ===== Задание 5.1–5.3 =====
@app.post("/login")
async def login(response: Response, credentials: LoginRequest):  # Используем Pydantic модель
    if credentials.username != fake_user["username"] or credentials.password != fake_user["password"]:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user_id = str(uuid.uuid4())
    timestamp = int(time.time())

    # Используем URLSafeTimedSerializer для подписи
    session_data = serializer.dumps({
        "user_id": user_id,
        "timestamp": timestamp
    })

    response.set_cookie(
        key="session_token",
        value=session_data,
        httponly=True,
        max_age=300,  # 5 минут
        secure=False,  # Для тестирования
        samesite="lax"
    )

    return {"message": "Logged in"}


def verify_session(request: Request, response: Response):
    cookie = request.cookies.get("session_token")
    if not cookie:
        raise HTTPException(status_code=401, detail="Session expired")

    try:
        # Автоматическая проверка срока действия
        data = serializer.loads(cookie, max_age=300)
        user_id = data["user_id"]
        timestamp = data["timestamp"]
    except (BadSignature, SignatureExpired):
        raise HTTPException(status_code=401, detail="Invalid session")

    now = int(time.time())
    diff = now - timestamp

    if diff > 300:
        raise HTTPException(status_code=401, detail="Session expired")

    # Задание 5.3: обновление только если прошло 3-5 минут
    if 180 <= diff < 300:
        new_timestamp = int(time.time())
        new_session_data = serializer.dumps({
            "user_id": user_id,
            "timestamp": new_timestamp
        })

        response.set_cookie(
            key="session_token",
            value=new_session_data,
            httponly=True,
            max_age=300,
            secure=False,
            samesite="lax"
        )

    return {"user_id": user_id, "last_activity": timestamp}


@app.get("/profile")
def profile(data=Depends(verify_session)):
    return {"message": "Authorized", "user": data}


# ===== Задание 5.4 =====
@app.get("/headers")
def get_headers(request: Request):
    user_agent = request.headers.get("user-agent")
    accept_language = request.headers.get("accept-language")

    if not user_agent or not accept_language:
        raise HTTPException(status_code=400, detail="Missing headers")

    return {
        "User-Agent": user_agent,
        "Accept-Language": accept_language
    }


# ===== Задание 5.5 =====
def get_common_headers(
    user_agent: str = Header(...),
    accept_language: str = Header(...)
):
    return CommonHeaders(user_agent=user_agent, accept_language=accept_language)


@app.get("/headers_pydantic")
def headers_pydantic(headers: CommonHeaders = Depends(get_common_headers)):
    return {
        "User-Agent": headers.user_agent,
        "Accept-Language": headers.accept_language
    }


@app.get("/info")
def info(response: Response, headers: CommonHeaders = Depends(get_common_headers)):
    response.headers["X-Server-Time"] = time.strftime("%Y-%m-%dT%H:%M:%S")

    return {
        "message": "Добро пожаловать! Ваши заголовки успешно обработаны.",
        "headers": {
            "User-Agent": headers.user_agent,
            "Accept-Language": headers.accept_language
        }
    }