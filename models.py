# This is forf the databaasse, the schema is the serilzaer
from database import Base
from sqlalchemy import Column, String, Integer, Boolean, Text


class Item(Base):
    __tablename__ = 'Items'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer)
    on_offer = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Item name={self.name}>"
