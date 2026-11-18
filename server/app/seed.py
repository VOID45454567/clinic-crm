import asyncio
from sqlmodel import select
from app.db.connect import SessionLocal
from app.db.models import User
from app.security import hash_password


async def seed():
    async with SessionLocal() as db:
        existing = await db.scalar(
            select(User).where(User.email == "admin@clinic.local")
        )
        if existing:
            print("Админ уже существует.")
            return

        admin = User(
            email="admin@clinic.local",
            hashed_password=hash_password("admin123"),
            role="admin",
        )
        db.add(admin)
        await db.commit()
        print("Админ успешно создан: admin@clinic.local / admin123")


if __name__ == "__main__":
    asyncio.run(seed())
