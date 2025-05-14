# CyberStore - Modern Gadget E-commerce Platform

![CyberStore Logo](static/images/logo.png)

A modern, feature-rich e-commerce platform built with Django for selling gadgets and electronics. CyberStore provides a seamless shopping experience with a beautiful UI and robust functionality.

## 🚀 Features

- **User Authentication & Authorization**
  - User registration and login
  - Profile management
  - Role-based access control

- **Product Management**
  - Category-based organization
  - Advanced product search
  - Real-time search suggestions
  - Wishlist functionality
  - Product ratings and reviews

- **Shopping Experience**
  - Intuitive shopping cart
  - Secure checkout process
  - Order tracking
  - Multiple payment options

- **UI/UX Features**
  - Responsive design
  - Modern animations
  - Quick view functionality
  - Advanced filtering and sorting
  - Real-time search suggestions

## 🛠️ Technology Stack

- **Backend**
  - Django 5.2
  - SQLite3 (default database)
  - Python 3.x

- **Frontend**
  - HTML5
  - CSS3
  - JavaScript
  - Bootstrap 5.3
  - Font Awesome 6.0

## 📋 Prerequisites

- Python 3.x
- pip (Python package manager)
- Virtual environment (recommended)

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cyberstore.git
cd cyberstore
```

2. Create and activate a virtual environment:
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
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the application.

## 🗂️ Project Structure

```
gadget_store/
├── cart/               # Shopping cart functionality
├── orders/            # Order processing and management
├── products/          # Product and category management
├── users/             # User authentication and profiles
├── static/
│   ├── css/          # Stylesheets
│   ├── js/           # JavaScript files
│   └── images/       # Static images
├── templates/         # HTML templates
├── gadget_store/      # Project settings
└── manage.py         # Django management script
```

## 💻 Usage

1. **Admin Interface**
   - Access the admin panel at `/admin`
   - Manage products, categories, orders, and users
   - Monitor site analytics

2. **User Features**
   - Browse products by category
   - Search for specific items
   - Add items to cart/wishlist
   - Complete purchases
   - Track orders

## 🔒 Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_database_url
EMAIL_HOST=your_email_host
EMAIL_PORT=your_email_port
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_email_password
```

## 🤝 Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

- Website: [cyberstore.com](https://cyberstore.com)
- Email: info@gadgetstore.com
- Phone: (123) 456-7890

## 🙏 Acknowledgments

- Bootstrap team for the amazing UI framework
- Django community for the robust backend framework
- All contributors who have helped to make this project better 