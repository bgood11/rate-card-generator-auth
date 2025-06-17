# Rate Card Generator - Supabase Authentication Version

This is the authentication-enhanced version of the Stax Rate Card Generator. This repository adds individual user accounts and role-based access control to replace the hardcoded password system.

## 🔐 Authentication Features

### User Roles
- **Admin**: Full access to all retailers
- **User**: Filtered access based on Salesforce company ownership

### Authentication Method
- **Supabase** email/password authentication
- Individual user accounts
- Session-based authentication
- Role-based access control

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

### Current Status
- **Phase 1**: ✅ Environment setup complete
- **Phase 2**: 🚀 Ready for Supabase project creation
- **Phase 3**: ⏳ Pending - Code implementation
- **Phase 4**: ⏳ Pending - Testing
- **Phase 5**: ⏳ Pending - Salesforce filtering
- **Phase 6**: ⏳ Pending - Deployment

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

## 🔄 Migration from Original

This version maintains 100% compatibility with the original Rate Card Generator while adding authentication:

### What's the Same
- All existing functionality (retailer search, rate card generation, Excel/PDF downloads)
- Same UI and branding
- Same Salesforce integration
- Same deployment process

### What's New
- Individual user accounts instead of single hardcoded password
- Role-based access control
- Supabase database integration
- User profile management (basic)

## 📚 Documentation

- `authbuild.md` - Step-by-step development checklist
- `README.md` - This file (project overview)

## 🛠 Technical Stack

- **Backend**: Flask (Python)
- **Authentication**: Supabase
- **Database**: PostgreSQL (via Supabase)
- **Frontend**: HTML/CSS/JavaScript (unchanged)
- **Deployment**: Vercel
- **External API**: Salesforce (simple-salesforce)

## 🔒 Security Features

- Secure password hashing
- Session management
- Role-based access control
- SQL injection prevention
- CSRF protection (planned)
- Rate limiting (planned)

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

**Original Project**: [Rate Card Generator](https://rate-card-generator-bgood11s-projects.vercel.app)  
**Development Branch**: Authentication Enhancement  
**Version**: Auth 1.0.0  
**Status**: Development in Progress