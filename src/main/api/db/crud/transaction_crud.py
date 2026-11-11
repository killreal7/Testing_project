from src.main.api.db.models.transaction_table import Transaction
from sqlalchemy.orm import Session


class TransactionCrudDB:
    @staticmethod
    def get_transaction_by_credit_id(db: Session, credit_id: int) -> Transaction | None:
        return db.query(Transaction).filter_by(credit_id=credit_id).first()