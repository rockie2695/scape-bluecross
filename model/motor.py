from motor.motor_asyncio import AsyncIOMotorDatabase


async def update_plans(
    db: AsyncIOMotorDatabase, where: dict[str], plan: dict[str, list]
):
    return await db["plans"].update_one(where, {"$set": plan}, upsert=True)
    # await db["plans"].insert_one(plan)


async def update_prices(
    db: AsyncIOMotorDatabase, where: dict[str], plan: dict[str, list]
):
    return await db["prices"].update_one(where, {"$set": plan}, upsert=True)
