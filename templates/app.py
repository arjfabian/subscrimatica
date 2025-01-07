from datetime import datetime
from decimal import Decimal
from models.database import engine
from views.view import SubscriptionService
from models.model import Subscription

class UI:
  def __init__(self):
    self.subscription_service = SubscriptionService(engine)

  def start(self):
    while True:
      menu_options = {
        1: ('Add a subscription', self.add_subscription),
        2: ('Delete a subscription', self.delete_subscription),
        3: ('Pay for subscription', self.pay_subscription),
        4: ('Total value', self.total_value),
        5: ('Payments of last 12 months', self.subscription_service.gen_chart)
      }

      for key, (desc, _) in menu_options.items():
        print(f'{key}. {desc}')
        
      choice = int(input('Choose an option: '))
      if choice in menu_options:
        menu_options[choice][1]()  # Call the corresponding function
      else:
        print("Invalid choice. Exiting...")
        break

  def add_subscription(self):
    company = input('Company: ')
    url = input('Website URL: ')
    subscription_date = datetime.strptime(input('Subscription Date (dd/mm/yyyy): '), '%d/%m/%Y')
    value = Decimal(input('Value: '))
    subscription = Subscription(company=company, url=url, subscription_date=subscription_date, value=value)
    self.subscription_service.create(subscription)
    print('Subscription added successfully.')

  def delete_subscription(self):
    subscriptions = self.subscription_service.list_all()
    print('Choose a subscription to delete:')
    for subscription in subscriptions:
      print(f'[{subscription.id}] -> {subscription.company}')
    choice = int(input('Choose the subscription: '))
    self.subscription_service.delete(choice)
    print('Subscription deleted successfully.')

  def pay_subscription(self):
    print("Payment functionality coming soon...")  # Placeholder for the future implementation

  def total_value(self):
    total = self.subscription_service.total_value()
    print(f'Total value for all subscriptions: {total}')

if __name__ == '__main__':
  UI().start()
