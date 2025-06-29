# Claude AI Assistant Context - Stax Staff Portal

This file provides essential context for Claude when working on the Stax Staff Portal (Rate Card Generator) project.

## 🎯 Project Overview

**Project Name**: Stax Staff Portal - Rate Card Generator  
**Repository**: rate-card-generator-auth  
**Production URL**: https://rate-card-generator-auth.vercel.app  
**Version**: 2.1.1 (Enhanced Retailer Search)  
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

## 🚀 DEPLOYMENT WORKFLOW - CRITICAL INSTRUCTIONS

**⚠️ IMPORTANT: NEVER push directly to `main` branch without explicit user approval!**

### Default Development Workflow (Unless Instructed Otherwise)
1. **Always create feature branches** for any changes
2. **Push to feature branch** to create preview deployments
3. **Share preview URL** with user for testing and approval
4. **Only merge to main** after explicit user approval
5. **Production deployment** happens automatically when merging to main

### Feature Branch Workflow
```bash
# 1. Create feature branch
git checkout -b feature/descriptive-name

# 2. Make changes and commit
git add .
git commit -m "Description of changes"

# 3. Push to feature branch (creates preview deployment)
git push origin feature/descriptive-name

# 4. Share preview URL for testing
# 5. Wait for user approval before merging to main

# 6. Only after approval - merge to production
git checkout main
git merge feature/descriptive-name
git push origin main  # Auto-deploys to production
```

### Preview vs Production
- **Feature branches** → Vercel preview deployments (for testing)
- **Main branch** → Production deployment (live site)
- **Never skip the preview step** unless explicitly told to deploy directly

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
- **Authentication**: Complete Supabase integration with modern card-based login
- **Role-Based Access**: Admin/User permissions
- **Rate Card Tool**: Full functionality with Excel/PDF export
- **Enhanced Retailer Search**: Comprehensive search including branch accounts with parent rate cards
- **Salesforce Integration**: Real-time data filtering with improved query logic
- **UI/UX**: Official Stax logo and clean design system implementation
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

## 🐛 Critical Bug Fix: Rate Card Duplicate Position Issue

### Problem Discovery
**Issue**: JN Bank was appearing as both Prime 1st AND Prime 2nd for the same product type (IFC), which is impossible.

**User Report**: "JN Bank dont have prime 1st IFC for taggas stafford AS Heat Pumps" - only Prime 2nd should appear for IFC products.

### Root Cause Investigation
Through systematic debugging with Salesforce MCP tools, discovered:

1. **Data Structure**: JN Bank has TWO separate Opportunities for ECO ENERGY LTD:
   - **006Nz00000R0TaMIAV**: IBC products (180 months) with Prime 1st position
   - **006Nz00000R8W3DIAV**: IFC products (12/24/36 months) with Prime 2nd position

2. **Pandas Merge Issue**: The merge logic in `process_rate_cards()` was joining on `['Lender_Name', 'Product_Vertical']` only, creating a many-to-many relationship:
   - IBC OpportunityLineItem records were getting merged with BOTH Prime 1st AND Prime 2nd positions
   - IFC OpportunityLineItem records were getting merged with BOTH Prime 1st AND Prime 2nd positions
   - This caused cross-contamination between different Opportunities

### Solutions Attempted

#### 1. **Active Assigned Rate Card Filtering** ❌ 
- Added pre-filtering to only include OpportunityLineItem records from Opportunities with active Assigned_Rate_Card__c records
- **Result**: Still showed duplicates because both IBC and IFC Opportunities had active assigned rate cards

#### 2. **Opportunity ID Merge** ❌
- Added Opportunity_Id to merge logic: `['Opportunity_Id', 'Lender_Name', 'Product_Vertical']`
- **Result**: Still failed - merge complexity remained problematic

#### 3. **Complete Rewrite: Single Query Approach** ✅
- **Solution**: Eliminated pandas merge entirely
- **Approach**: Start with Assigned_Rate_Card__c records, get OpportunityLineItem records for each specific Opportunity
- **Result**: Direct 1:1 relationship ensures each rate card line item gets correct position

### Final Implementation
**File**: `rate_card_generator.py`

**New Architecture**:
```python
def get_rate_card_items(self, retailer_name: str) -> pd.DataFrame:
    # 1. Query active Assigned_Rate_Card__c records for retailer
    # 2. For each unique Opportunity, get its OpportunityLineItem records  
    # 3. Attach position data directly from Assigned_Rate_Card__c
    # 4. Return combined data with embedded position information
    
def process_rate_cards(self, retailer_name: str) -> Dict[str, pd.DataFrame]:
    # No merge needed - position data already embedded
    # Process rate card items directly
```

**Key Benefits**:
- **No merge complexity**: Position data embedded at query time
- **Impossible cross-contamination**: Each OpportunityLineItem tied to specific Assigned_Rate_Card__c
- **Data integrity**: 1:1 relationship guarantees correct positions

### Expected Results
- **JN Bank AS Heat Pump IBC** (180 months) → Only Prime 1st position
- **JN Bank AS Heat Pump IFC** (12/24/36 months) → Only Prime 2nd position  
- **No duplicate positions** for any lender/product combination

---

## 🔧 Additional Fixes: Terminated Retailer Filtering

### Problem
After fixing the duplicate position issue, terminated retailers were still appearing in search results despite having no active rate cards.

### Solution Journey
1. **Initial Attempts (Failed)**:
   - `Name NOT LIKE '%TERMINATED%'` - SOQL syntax error
   - `NOT (Name LIKE '%TERMINATED%')` - SOQL syntax error  
   - `(NOT Name LIKE '%TERMINATED%')` - SOQL syntax error
   - `NOT Name LIKE '%TERMINATED%'` - Still SOQL syntax error

2. **Root Cause**: SOQL has specific syntax requirements that differ from standard SQL

3. **Final Solution**: Simplified approach - only show retailers with active assigned rate cards
   - Removed all name-based filtering
   - Enhanced Query 1 to check for active Assigned_Rate_Card__c records
   - Terminated retailers naturally excluded (they have no active rate cards)

### Technical Implementation
```sql
-- Query 1: Now checks for active assigned rate cards
AND Id IN (
    SELECT AccountId 
    FROM Opportunity 
    WHERE RecordType.DeveloperName = 'Retailer_Rate_Card' 
        AND StageName = 'Live'
        AND Id IN (
            SELECT Opportunity__c
            FROM Assigned_Rate_Card__c
            WHERE Active__c = true
        )
)
```

**Last Updated**: 2025-01-26  
**Version**: 2.3.0 (Terminated Retailer Filtering)  
**Latest Enhancement**: Simplified search to only show retailers with active assigned rate cards  
**Next Features**: Additional business tools (analytics, reporting, admin tools)