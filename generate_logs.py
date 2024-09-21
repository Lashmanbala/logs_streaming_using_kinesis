from faker import Faker
import random
from datetime import datetime

fake = Faker()
actions = ['login', 'logout', 'purchase', 'add_to_cart', 'view_item', 'search']

def create_fake_log_entry():
    """
    Creates a single fake user log entry.
    """
    return {
        'timestamp': datetime.now().isoformat(),  # Current timestamp in ISO format
        'username': fake.user_name(),
        'email': fake.email(),
        'action': random.choice(actions),  # Random user action
        'ip_address': fake.ipv4_public(),
        'location': {
            'city': fake.city(),
            'country': fake.country()
        }
    }

log = create_fake_log_entry()
print(log)