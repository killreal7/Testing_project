from sqlalchemy import Column, Integer, FLOAT, TIMESTAMP
from src.main.api.db.base import Base


class Credit(Base):
    __tablename__ = 'credit'
    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, nullable=False)
    amount = Column(FLOAT, nullable=False)
    term_months = Column(Integer, nullable=False)
    balance = Column(FLOAT, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

    def __repr__(self):
        return f'<Credit(id={self.id}, account_id={self.account_id}, amount={self.amount}, term_months={self.term_months}, balance={self.balance}, created_at={self.created_at})>'