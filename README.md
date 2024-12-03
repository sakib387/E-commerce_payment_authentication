# TestHub

TestHub is a full-featured e-commerce web application built with Django. The platform allows users to browse and purchase various food products categorized as drinks, lunch, breakfast, and dinner. The application provides a seamless experience for account management, product selection, and checkout.

## Features

### User Account Management
- **Sign Up & Authentication:**
  - Users can create accounts by signing up.
  - Email verification is implemented; users receive an activation link via email to activate their accounts.
- **Login & Logout:**
  - Users can securely log in and log out.

### Product Browsing & Management
- **Categories:**
  - Products are categorized into drinks, lunch, breakfast, and dinner for easy navigation.
- **Cart Management:**
  - Users can add items to their cart and view the cart contents.

### Payment Options
- **Payment Methods:**
  - Supports multiple payment methods including credit/debit cards, mobile banking, and bank transfers.

## Installation & Setup

### Prerequisites
- Python (3.x)
- Django (4.x)
- A mail server for email verification
- A payment gateway integration (e.g., SSLCommerz, Stripe, or others)

### Steps to Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/testhub.git
   cd testhub
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Configure email settings in `settings.py`:
   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'your-mail-server'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'your-email@example.com'
   EMAIL_HOST_PASSWORD = 'your-email-password'
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the application at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Technologies Used
- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite (default), can be configured for PostgreSQL/MySQL
- **Payment Gateway:** Supports integration with multiple providers

## Project Structure
```
|-- testhub/
    |-- manage.py
    |-- testhub/        # Project settings
    |-- products/       # App for managing product listings
    |-- accounts/       # App for user authentication
    |-- cart/           # App for cart and checkout functionality
    |-- templates/      # HTML templates
    |-- static/         # Static files (CSS, JS, Images)
```

## Future Enhancements
- Adding product reviews and ratings.
- Implementing coupon codes and discounts.
- Enhancing UI/UX for a better shopping experience.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing
Contributions are welcome! Please feel free to fork the repository and submit pull requests.

## Contact
If you have any questions or suggestions, please feel free to contact us at [sakibmollah28.387@gmail.com](mailto:sakibmollah28.387@gmail.com).
