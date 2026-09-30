import os
import random
import string
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from faker import Faker

from utils.logger import get_logger

logger = get_logger(__name__)


class Helpers:
    @staticmethod
    def generate_random_string(length=6):
        """Generate a random alphabetic string."""
        if length <= 0:
            raise ValueError("length must be a positive integer")
        logger.debug("Generating random string of length %s", length)
        return "".join(random.choices(string.ascii_letters, k=length))

    @staticmethod
    def generate_random_number(length=6):
        """Generate a random numeric string (digits only)."""
        if length <= 0:
            raise ValueError("length must be a positive integer")
        logger.debug("Generating random number of length %s", length)
        return "".join(random.choices(string.digits, k=length))

    @staticmethod
    def generate_random_email(prefix="user", domain="example.com"):
        """Generate a random email address."""
        logger.debug(
            "Generating random email with prefix %s and domain %s", prefix, domain
        )
        username = f"{prefix}_{Helpers.generate_random_string(6).lower()}"
        return f"{username}@{domain}"

    @staticmethod
    def generate_random_phone(country_code="+91", length=8):
        """Generate a random phone number string."""
        if length <= 0:
            raise ValueError("length must be a positive integer")
        number = "".join(random.choices(string.digits, k=length))
        logger.debug("Generated phone number with country code %s", country_code)
        return f"97{number}"

    @staticmethod
    def get_timestamp(fmt="%Y%m%d%H%M%S"):
        """Return current timestamp string in given format."""
        logger.debug("Generating timestamp with format %s", fmt)
        return datetime.now().strftime(fmt)

    @staticmethod
    def get_future_date(years_to_add=2, fmt="%Y-%m-%d"):
        """Return a future date string by adding years to the current date."""
        future_datetime = datetime.now() + relativedelta(years=years_to_add)
        logger.debug(
            "Generating future date (current + %d years) with format %s",
            years_to_add,
            fmt,
        )
        return future_datetime.strftime(fmt)

    @staticmethod
    def sleep(seconds=1):
        """Pause execution for the given number of seconds."""
        if seconds < 0:
            raise ValueError("seconds must be non-negative")
        logger.debug("Sleeping for %s seconds", seconds)
        time.sleep(seconds)

    @staticmethod
    def ensure_dir(path):
        """Create directory if it does not exist."""
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        logger.debug("Ensured directory exists: %s", path)
        return path

    @staticmethod
    def maximize_browser(page):
        """Maximize the browser viewport in a stable, predictable way."""
        if page is None:
            raise ValueError("page cannot be None")
        logger.debug("Maximizing browser viewport")
        page.set_viewport_size({"width": 1920, "height": 1080})

    @staticmethod
    def generate_random_indian_state_data():
        """
        Generate a matched random Indian state name and its state code.
        Returns:
            tuple: (state_name, state_code) e.g., ("Maharashtra", "MH")
        """
        indian_states = {
            "Andhra Pradesh": "AP",
            "Arunachal Pradesh": "AR",
            "Assam": "AS",
            "Bihar": "BR",
            "Chhattisgarh": "CG",
            "Goa": "GA",
            "Gujarat": "GJ",
            "Haryana": "HR",
            "Himachal Pradesh": "HP",
            "Jharkhand": "JH",
            "Karnataka": "KA",
            "Kerala": "KL",
            "Madhya Pradesh": "MP",
            "Maharashtra": "MH",
            "Manipur": "MN",
            "Meghalaya": "ML",
            "Mizoram": "MZ",
            "Nagaland": "NL",
            "Odisha": "OD",
            "Punjab": "PB",
            "Rajasthan": "RJ",
            "Sikkim": "SK",
            "Tamil Nadu": "TN",
            "Telangana": "TG",
            "Tripura": "TR",
            "Uttar Pradesh": "UP",
            "Uttarakhand": "UK",
            "West Bengal": "WB",
            "Andaman and Nicobar Islands": "AN",
            "Chandigarh": "CH",
            "Dadra and Nagar Haveli": "DN",
            "Daman and Diu": "DD",
            "Delhi": "DL",
            "Jammu & Kashmir": "JK",
            "Ladakh": "LA",
            "Lakshadweep": "LD",
            "Puducherry": "PY",
        }
        state_name = random.choice(list(indian_states.keys()))
        state_code = indian_states[state_name]

        logger.debug(
            "Generated matched Indian state data -> Name: %s, Code: %s",
            state_name,
            state_code,
        )
        return state_name, state_code

    @staticmethod
    def generate_random_state_name():
        """Generate a random Indian state name."""
        state_name, _ = Helpers.generate_random_indian_state_data()
        return state_name

    @staticmethod
    def generate_random_state_abbreviation():
        """Generate a random Indian state abbreviation matching the generated flow."""
        _, state_code = Helpers.generate_random_indian_state_data()
        return state_code

    @staticmethod
    def generate_random_ip():
        """Generate a random IPv4 address using Faker."""
        fake = Faker()
        ip_address = fake.ipv4()
        logger.debug("Generated random IP address: %s", ip_address)
        return ip_address

    @staticmethod
    def generate_random_port():
        """Generate a random port number between 1024 and 65535."""
        port = random.randint(1024, 65535)
        logger.debug("Generated random port number: %s", port)
        return str(port)
