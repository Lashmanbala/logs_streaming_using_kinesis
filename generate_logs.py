from faker import Faker
import random
from datetime import datetime
import os
import json
import dotenv
import time

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


def generate_logs(num_logs=10):
    """
    Generates and appends fake user log entries to a file.
    """

    log_directory = str(os.environ.get('LOG_DIR'))
    log_file = str(os.environ.get('LOG_FILE'))

    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    with open(log_file, 'a') as f:
        for _ in range(num_logs):
            log_entry = create_fake_log_entry()
            f.write(json.dumps(log_entry) + "\n")  # Write each log entry in JSON format
            print('a log entered')
            time.sleep(60)

if __name__ == "__main":
    dotenv.load_dotenv()
    generate_logs(10)
