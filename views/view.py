from models.model import Subscription, Payments
from sqlmodel import Session, select
from datetime import date, datetime

# Assuming you've defined get_session somewhere in your code
def get_session(engine):
    """Return a session object for interacting with the database."""
    return Session(engine)

class SubscriptionService:
  def __init__(self, engine):
    self.engine = engine
  
  def create(self, subscription: Subscription):
    with get_session(self.engine) as session:
      session.add(subscription)
      session.commit()
      return subscription
    
  def list_all(self):
    with get_session(self.engine) as session:
      statement = select(Subscription)
      results = session.exec(statement).all()
    return results

  def delete(self, id):
    with get_session(self.engine) as session:
      statement = select(Subscription).where(Subscription.id == id)
      result = session.exec(statement).one()
      print(result)
      session.delete(result)
      session.commit()

  def _has_pay(self, results):
    return any(result.date.month == date.today().month for result in results)

  def pay(self, subscription: Subscription):
    with get_session(self.engine) as session:
      statement = select(Payments).join(Subscription).where(Subscription.company == subscription.company)
      results = session.exec(statement).all()

      if self._has_pay(results):
        question = input('This subscription has already been paid this month. Do you want to pay again? [Y/n]')
        if not question.upper() == 'Y':
          return
      
      pay = Payments(subscription_id=subscription.id, date=date.today())
      session.add(pay)
      session.commit()
    
  def total_value(self):
    with get_session(self.engine) as session:
      statement = select(Subscription)
      results = session.exec(statement).all()
    
    total = 0

    for result in results:
      total += result.value
    
    return float(total)
  
  def _get_last_n_months_native(self, n: int = 12):
    today = datetime.now()
    year, month = today.year, today.month

    # Generate the last 'n' months
    last_n_months = [
        ((month - i - 1) % 12 + 1, year - ((12 - (month - i)) // 12))
        for i in range(n)
    ]
    return last_n_months[::-1]

  def _get_values_for_months(self, last_n_months):
      with get_session(self.engine) as session:
          statement = select(Payments)
          results = session.exec(statement).all()

          values_for_months = []
          for i in last_n_months:
              value = 0
              for result in results:
                  if result.date.month == i[0] and result.date.year == i[1]:
                      value += float(result.subscription.value)
              values_for_months.append(value)
      return values_for_months  # Ensure values are returned!

  def gen_chart(self):
      last_12_months = self._get_last_n_months_native()
      last_12_months_strings = [f"{month:02d}/{str(year)[-2:]}" for month, year in last_12_months]
      values_for_months = self._get_values_for_months(last_12_months)

      import matplotlib.pyplot as plt
      plt.plot(last_12_months_strings, values_for_months)
      plt.show()
