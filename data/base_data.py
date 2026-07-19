
# --- Site under test ---
BASE_URL = "https://v2.demo.sylius.com/en_US/"

# --- Existing registered user (used for "duplicate email" negative tests) ---
first_name = "shalev"
last_name = "shapiro"
email = "shalev@gmail.com"
password = "123456789"

# --- Valid demo-shop credentials (used across login / e2e / security tests) ---
VALID_USER_EMAIL = "shop@example.com"
VALID_USER_PASSWORD = "sylius"

# --- Default product used across catalog / cart / checkout tests ---
DEFAULT_PRODUCT_NAME = "Sunshine Strappy Delight"

# --- Default valid checkout address, reused and overridden per test case ---
CHECKOUT_ADDRESS = {
    "email": "shalev6005@gmail.com",
    "first_name": "shalev",
    "last_name": "shapiro",
    "company": "shapiro",
    "street": "200 George Street",
    "country": "AU",
    "city": "Sydney",
    "postcode": "2000",
    "phone": "123456789",
}

# --- Security test payloads ---
XSS_PAYLOAD = "<script>alert('XSS')</script>"
