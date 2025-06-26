# Stax Staff Portal - Rate Card Generator

A professional staff portal for Stax business development tools. Features a modern dashboard interface with role-based access control and seamless Salesforce integration for generating customer rate cards.

## 🎯 Key Features

### Dashboard Portal
- **Modern Dashboard**: Professional landing page showing available business tools
- **Tool Cards**: Easy-to-navigate interface for accessing different tools
- **User Profile Sidebar**: Shows user information and access level
- **Responsive Design**: Built with Stax brand colors and design principles

### Authentication & Security
- **Supabase Authentication**: Secure email/password login system
- **Role-Based Access**: Admin and User roles with different permissions
- **Session Management**: Secure session handling for user state
- **Salesforce Integration**: User profiles linked to Salesforce IDs for data filtering

### Rate Card Generator Tool
- **Enhanced Retailer Search**: Comprehensive search that finds both main retailers and their branch locations
- **Salesforce Data Integration**: Real-time data from Salesforce
- **Commission Control**: Admins can show/hide commission data
- **Multiple Export Formats**: Generate Excel and PDF rate cards
- **Role-Based Filtering**:
  - Admin users: Access to all retailer accounts
  - Regular users: Only see accounts they own in Salesforce

## 🏗️ Architecture

### Application Flow
```
Login → Dashboard Portal → Select Tool → Rate Card Generator
```

### Technology Stack
- **Backend**: Flask (Python) with Jinja2 templating
- **Frontend**: HTML/CSS/JavaScript with Stax design system
- **Authentication**: Supabase (PostgreSQL)
- **Data Source**: Salesforce API
- **Deployment**: Vercel (serverless)
- **File Generation**: Excel (openpyxl) and PDF (ReportLab)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Supabase account
- Salesforce credentials

### Environment Variables
Create a `.env` file with:
```env
# Salesforce Credentials
SF_USERNAME=your.email@sherminfinance.co.uk
SF_PASSWORD=your_password
SF_TOKEN=your_security_token
SF_DOMAIN=login

# Supabase Credentials
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here

# Flask Configuration
PORT=8080
```

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python web_app.py
```

## 📋 Development Process

This project follows a step-by-step development approach documented in `authbuild.md`.

### Project Status
- **Authentication**: ✅ Complete with Supabase integration and modern login page
- **Dashboard Portal**: ✅ Implemented with Stax branding
- **Rate Card Tool**: ✅ Fully functional with role-based filtering
- **Salesforce Integration**: ✅ Real-time data access
- **UI/UX**: ✅ Official Stax logo and clean interface design
- **Production Deployment**: ✅ Live on Vercel

### Development Commands
```bash
# Activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python web_app.py
```

## 📂 Project Structure

```
rate-card-generator-auth/
├── templates/               # Jinja2 templates
│   ├── base.html           # Base template with header/sidebar
│   ├── dashboard.html      # Dashboard page template
│   └── login.html          # Modern login page template
├── static/
│   ├── css/
│   │   └── dashboard.css   # Stax design system styles
│   └── stax-logo.png       # Company logo
├── 3628 Stax Logo Colour.svg # Official Stax logo
├── web_app.py              # Main Flask application
├── rate_card_generator.py  # Salesforce data processing
├── pdf_generator.py        # PDF generation logic
├── supabase_client.py      # Authentication handling
└── requirements.txt        # Python dependencies
```

## 👥 User Management

### Adding New Users

1. **Create user in Supabase**:
   - Go to Authentication > Users in your Supabase dashboard
   - Add user with email/password
   
2. **Update user profile**:
   - Go to Table Editor > profiles
   - Find the new user record
   - Set `role` to either `admin` or `user`
   - Set `salesforce_id` to the Salesforce User ID (e.g., `0058d0000058ya3AAA`)
   
3. **Get Salesforce User ID**:
   - Use the test script: `python test_ownership.py`
   - Find the user's 18-character Salesforce ID
   - Match by email or name from the Shermin Finance users list

### Example User Setup
```
Email: mike.jennings@sherminfinance.co.uk
Role: user
Salesforce ID: 0058d0000058yYvAAI
Result: User will see only retailers owned by Mike Jennings (218 accounts)
```

## 📚 Documentation

- `README.md` - Project overview and setup guide (this file)
- `CLAUDE.md` - AI assistant context and project details
- `authbuild.md` - Authentication implementation checklist
- `DASHBOARD_IMPLEMENTATION_TODO.md` - Dashboard development tracking
- `DESIGN_PRINCIPLES.md` - Stax design system and UI guidelines

## 🌐 Routes & Endpoints

### Public Routes
- `/login` - User login page
- `/logout` - Logout and session cleanup

### Protected Routes
- `/` - Redirects to dashboard
- `/dashboard` - Main portal dashboard
- `/tools/rate-card-generator` - Rate card generation tool

### API Endpoints
- `/search?q=<query>` - Search retailers (filtered by role)
- `/user-info` - Get current user information
- `/generate-data` - Generate rate card data (JSON)
- `/generate` - Generate Excel file download
- `/generate-pdf` - Generate PDF file download

## 🔒 Security Features

- **Supabase Authentication**: Secure password hashing and storage
- **Session Management**: Flask session cookies with secret key
- **Role-Based Access Control**: Admin/User permissions
- **Data Filtering**: Users only see their own Salesforce accounts
- **SQL Injection Prevention**: Parameterized queries via Supabase
- **Environment Variables**: Sensitive credentials stored securely

## 🌐 Deployment

This project is designed to deploy seamlessly on Vercel with automatic Supabase integration.

### Vercel Deployment
1. Import this repository to Vercel
2. Connect to Supabase (automatic via Vercel integration)
3. Set environment variables
4. Deploy

## 📞 Support

For issues or questions about this authentication version, refer to the development checklist in `authbuild.md`.

---

**Production URL**: [rate-card-generator-auth.vercel.app](https://rate-card-generator-auth.vercel.app)  
**Repository**: [github.com/bgood11/rate-card-generator-auth](https://github.com/bgood11/rate-card-generator-auth)  
**Version**: 2.1.1 (Enhanced Retailer Search)  
**Status**: ✅ Production Ready