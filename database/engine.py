from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from common.settings import settings

engine = create_async_engine(settings.DATABASE_URI_WITH_DRIVER)

AsyncSession = async_sessionmaker(bind=engine, autoflush=False)
