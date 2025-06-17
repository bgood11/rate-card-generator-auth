# Rate Card Generator - Supabase Authentication Version

This is the authentication-enhanced version of the Stax Rate Card Generator. This repository adds individual user accounts and role-based access control to replace the hardcoded password system.

## 🔐 Authentication Features

### User Roles
- **Admin**: Full access to all retailers and rate cards
- **User**: Access restricted to retailers they own in Salesforce (based on Account.OwnerId)

### Authentication Method
- **Supabase** email/password authentication
- Individual user accounts with profiles
- Session-based authentication
- **Salesforce-integrated role-based filtering**

### Filtering Implementation
- **Admin users**: See all retailer accounts (no filtering applied)
- **Regular users**: Only see Account records where `OwnerId` matches their `salesforce_id`
- User profiles link Supabase authentication to Salesforce User IDs
- Seamless integration with existing rate card generation functionality

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

### Current Status
- **Phase 1**: ✅ Environment setup complete
- **Phase 2**: ✅ Supabase project created and configured
- **Phase 3**: ✅ Code implementation complete
- **Phase 4**: ✅ Authentication testing complete
- **Phase 5**: ✅ **Salesforce filtering implemented**
- **Phase 6**: ✅ Deployment ready

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
- **Salesforce-integrated role-based filtering**
- Supabase database integration
- User profile management linked to Salesforce User IDs

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