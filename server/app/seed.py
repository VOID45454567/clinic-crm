import asyncio

from sqlmodel import select

from app.db.connect import SessionLocal
from app.db.models.user import User
from app.security import hash_password

SEED_USERS = [
    {
        "email": "admin@clinic.local",
        "password": "admin123",
        "role": "admin",
    },
    {
        "email": "doctor@clinic.local",
        "password": "doctor123",
        "role": "doctor",
    },
    {
        "email": "registrar@clinic.local",
        "password": "registrar123",
        "role": "registrar",
    },
]


async def seed():
    async with SessionLocal() as db:
        created_count = 0
        skipped_count = 0

        for user_data in SEED_USERS:
            existing = await db.scalar(
                select(User).where(User.email == user_data["email"])
            )
            if existing:
                print(f"⏭  Пользователь {user_data['email']} уже существует")
                skipped_count += 1
                continue

            user = User(
                email=user_data["email"],
                hashed_password=hash_password(user_data["password"]),
                role=user_data["role"],
                is_active=True,
            )
            db.add(user)
            created_count += 1
            print(
                f"✓ Создан {user_data['role']}: {user_data['email']} / {user_data['password']}"
            )

        await db.commit()
        print(f"\n✓ Создано пользователей: {created_count}, пропущено: {skipped_count}")


if __name__ == "__main__":
    asyncio.run(seed())
