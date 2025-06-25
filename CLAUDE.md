# Claude AI Assistant Context - Stax Staff Portal

This file provides essential context for Claude when working on the Stax Staff Portal (Rate Card Generator) project.

## 🎯 Project Overview

**Project Name**: Stax Staff Portal - Rate Card Generator  
**Repository**: rate-card-generator-auth  
**Production URL**: https://rate-card-generator-auth.vercel.app  
**Version**: 2.0.0 (Dashboard Portal Release)  
**Status**: ✅ Production Ready

## 🏗️ Architecture Overview

### Application Flow
```
User Login (Supabase) → Dashboard Portal → Select Tool → Rate Card Generator
```

### Technology Stack
- **Backend**: Flask (Python) with Jinja2 templating
- **Frontend**: HTML/CSS/JavaScript with Stax design system
- **Authentication**: Supabase (PostgreSQL)
- **Data Source**: Salesforce API
- **Deployment**: Vercel (serverless)
- **File Generation**: Excel (openpyxl) and PDF (ReportLab)

## 📁 Project Structure

```
rate-card-generator-auth/
├── templates/               # Jinja2 templates
│   ├── base.html           # Base template with header/sidebar
│   └── dashboard.html      # Dashboard page template
├── static/
│   ├── css/
│   │   └── dashboard.css   # Stax design system styles
│   └── stax-logo.png       # Company logo
├── web_app.py              # Main Flask application
├── rate_card_generator.py  # Salesforce data processing
├── pdf_generator.py        # PDF generation logic
├── supabase_client.py      # Authentication handling
└── requirements.txt        # Python dependencies
```

## 🌐 Routes & Endpoints

### Public Routes
- `/login` - User login page with Supabase authentication
- `/logout` - Logout and session cleanup

### Protected Routes
- `/` - Redirects authenticated users to dashboard
- `/dashboard` - Main portal dashboard (Jinja2 template)
- `/tools/rate-card-generator` - Rate card generation tool

### API Endpoints
- `/search?q=<query>` - Search retailers (filtered by user role)
- `/user-info` - Get current user information for client-side logic
- `/generate-data` - Generate rate card data as JSON for display
- `/generate` - Generate and download Excel file
- `/generate-pdf` - Generate and download PDF file

## 👤 User Roles & Authentication

### User Roles
- **Admin**: Full access to all retailers and rate cards
- **User**: Access restricted to retailers they own in Salesforce

### Authentication Flow
1. User enters email/password on `/login`
2. Supabase authentication validates credentials
3. User profile retrieved from `profiles` table
4. Session established with user data
5. Redirect to `/dashboard`

### Role-Based Filtering
- **Admin users**: See all retailer accounts (no filtering)
- **Regular users**: Only see Account records where `OwnerId` matches their `salesforce_id`

## 🎨 Design System

### Stax Brand Colors
```css
--stax-teal: #477085
--stax-pink: #d884b6
--stax-light-blue: #2ab7e3
--stax-gray: #9d9c9c
```

### Key Design Principles
- Professional business tool aesthetic
- Consistent Stax branding throughout
- Responsive design (desktop-first)
- Clean, modern interface
- Accessible typography and spacing

## 🔧 Development Commands

### Local Development
```bash
# Setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run development server
python web_app.py  # Runs on http://localhost:8080
```

### Git Workflow
```bash
# Feature development
git checkout -b feature/feature-name
git add .
git commit -m "Description of changes"
git push origin feature/feature-name

# Production deployment
git checkout main
git merge feature/feature-name
git push origin main  # Auto-deploys to Vercel
```

## 🗂️ Database Schema (Supabase)

### profiles table
```sql
CREATE TABLE profiles (
  id UUID REFERENCES auth.users(id) PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  role TEXT CHECK (role IN ('admin', 'user')) DEFAULT 'user',
  salesforce_id TEXT,
  full_name TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

## 🔐 Environment Variables

### Required Variables (.env)
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

## 📋 Current Implementation Status

### ✅ Completed Features
- **Dashboard Portal**: Professional landing page with tool cards
- **Template System**: Jinja2 templates with base.html inheritance
- **Authentication**: Complete Supabase integration
- **Role-Based Access**: Admin/User permissions
- **Rate Card Tool**: Full functionality with Excel/PDF export
- **Salesforce Integration**: Real-time data filtering
- **UI/UX**: Stax design system implementation
- **Production Deployment**: Live on Vercel

### 🎯 Tool Management System

The dashboard uses a dynamic tool structure in `web_app.py`:

```python
AVAILABLE_TOOLS = {
    'rate-card-generator': {
        'name': 'Rate Card Generator',
        'description': 'Generate rate cards with Salesforce data',
        'icon': '📊',
        'enabled': True,
        'access_level': ['admin', 'user']
    }
    # Future tools can be added here
}
```

### 🚀 Adding New Tools

To add new tools to the dashboard:

1. **Add tool definition** to `AVAILABLE_TOOLS` in `web_app.py`
2. **Create new route** (e.g., `/tools/new-tool`)
3. **Update access_level** array for role permissions
4. **Set enabled: true** when ready to go live

## 🧪 Testing

### Manual Testing Checklist
- [ ] Login with admin credentials
- [ ] Login with regular user credentials
- [ ] Dashboard loads with correct user profile
- [ ] Tool cards display based on role
- [ ] Rate Card Generator functions correctly
- [ ] Excel/PDF downloads work
- [ ] Back to Dashboard navigation works
- [ ] Logout clears session

### Test Users
Create test users in Supabase with different roles for testing:
- Admin user: Full access
- Regular user: Limited to owned accounts

## 🐛 Common Issues & Solutions

### Template Not Found
- Check template files exist in `templates/` directory
- Verify `render_template()` calls use correct file names

### Static Files Not Loading
- Use `url_for('static', filename='...')` in templates
- Check Vercel deployment includes static files

### Authentication Issues
- Verify Supabase environment variables
- Check user profile exists in `profiles` table
- Ensure `salesforce_id` is set for regular users

### Salesforce Connection
- Verify SF credentials in environment variables
- Check Salesforce security token is current
- Test connection with rate card generator

## 📞 Support & Maintenance

### Key Files to Monitor
- `web_app.py` - Main application logic
- `templates/` - UI templates
- `static/css/dashboard.css` - Styling
- `supabase_client.py` - Authentication
- `rate_card_generator.py` - Salesforce integration

### Deployment
- **Automatic**: Pushing to `main` branch auto-deploys to Vercel
- **Manual**: Use Vercel CLI or dashboard for manual deployments
- **Rollback**: Revert git commits and push to main

---

**Last Updated**: 2025-01-25  
**Version**: 2.0.0 Dashboard Release  
**Next Features**: Additional business tools (analytics, reporting, admin tools)