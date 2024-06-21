from sqlalchemy import Column, Integer, String, DateTime
from app.configs.database import Base, engine


class TaskModel(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(50))
    description = Column(String(250))
    status = Column(String(250))
    created_at = DateTime()


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
