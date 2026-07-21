from app.database.session import SessionLocal

from app.seed.seed_admin import seed_admin


def run_seed():
    db = SessionLocal()

    try:
        print("=" * 50)
        print("🌱 Running Database Seeder")
        print("=" * 50)

        seed_admin(db)

        print("=" * 50)
        print("🎉 Database seeding completed!")
        print("=" * 50)

    finally:
        db.close()


if __name__ == "__main__":
    run_seed()