from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession


class SQLOrmRepository:
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict):
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def edit_one(self, invoked_id: int, data: dict):
        stmt = update(self.model).values(**data).filter_by(id=invoked_id).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def find_one(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.one().to_read_model()
        return res

    async def find_all(self):
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        res = [row[0].to_read_model() for row in res.all()]
        return res

    async def delete_one(self, data: dict):
        stmt = delete(self.model).where(self.model.id == data["id"])
        res = await self.session.execute(stmt)
        return res.rowcount
