from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from datetime import date
from decimal import Decimal

class Subscription(SQLModel, table=True):
  id: int = Field(primary_key=True)   # O usuário não define o valor
  company: str
  url: Optional[str] = None  # Campo opcional
  subscription_date: date
  value: Decimal    # Recomendado em vez de float para valores monetários

class Payments(SQLModel, table=True):
  id: int = Field(primary_key=True)
  subscription_id: int = Field(foreign_key='subscription.id')
  subscription: Subscription = Relationship()
  date: date