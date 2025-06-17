# Auth Build Checklist - Simple Supabase Authentication

## Overview
This document tracks the implementation of simple Supabase authentication to replace the hardcoded password system. We're taking a minimal, step-by-step approach to avoid complexity.

**Repository**: https://github.com/bgood11/rate-card-generator-auth  
**Production URL**: https://rate-card-generator-bgood11s-projects.vercel.app (PROTECTED - no changes)  
**Goal**: Replace hardcoded password with individual user accounts + basic role filtering

---

## ✅ Phase 1: Environment Setup

### Git & Branch Setup
- [x] Create new branch `simple-auth`
- [x] Verify virtual environment is active
- [ ] Test current functionality works
- [x] Commit baseline state

### Documentation
- [x] Create authbuild.md checklist
- [x] Update CLAUDE.md with auth project status
- [ ] Document current hardcoded auth system

---

## 📋 Phase 2: Supabase Project Creation (Manual Setup)

### Step 2.1: Create New Supabase Project
- [ ] **Go to Supabase Dashboard**: https://supabase.com/dashboard
- [ ] **Click "New Project"**
- [ ] **Project Details**:
  - Organization: (Select your organization)
  - Project Name: `rate-card-auth`
  - Database Password: (Generate strong password - save it!)
  - Region: (Choose closest to you)
- [ ] **Click "Create new project"** (takes ~2 minutes)
- [ ] **Save project details**:
  - Project URL: `https://[project-id].supabase.co`
  - Anon Key: (from Settings > API)
  - Service Role Key: (from Settings > API)

### Step 2.2: Configure Authentication Settings
- [ ] **Go to Authentication > Settings**
- [ ] **Confirm Email**: Turn OFF for testing (can enable later)
- [ ] **Sign up enabled**: Turn ON
- [ ] **Email auth**: Turn ON
- [ ] **Save settings**

### Step 2.3: Create User Profile Table
- [ ] **Go to SQL Editor**
- [ ] **Run this SQL** (copy/paste):
```sql
-- Create profiles table extending auth.users
CREATE TABLE public.profiles (
    id UUID REFERENCES auth.users(id) PRIMARY KEY,
    email TEXT NOT NULL,
    full_name TEXT,
    role TEXT NOT NULL DEFAULT 'user' CHECK (role IN ('admin', 'user')),
    salesforce_id TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Create policy for users to read their own profile
CREATE POLICY "Users can view own profile" 
ON public.profiles FOR SELECT 
USING (auth.uid() = id);

-- Create policy for service role to manage all profiles
CREATE POLICY "Service role can manage all profiles" 
ON public.profiles FOR ALL 
USING (auth.role() = 'service_role');

-- Create function to handle user creation
CREATE OR REPLACE FUNCTION public.handle_new_user() 
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (id, email, full_name)
    VALUES (NEW.id, NEW.email, NEW.raw_user_meta_data->>'full_name');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create trigger for new user creation
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
```
- [ ] **Verify table created**: Check Tables tab shows `profiles`

### Step 2.4: Create Test Users
**First User (Admin)**:
- [ ] **Go to Authentication > Users**
- [ ] **Click "Add user"**
- [ ] **Email**: `admin@sherminfinance.co.uk`
- [ ] **Password**: (Choose strong password - save it!)
- [ ] **Auto Confirm User**: ON
- [ ] **Click "Create user"**
- [ ] **Go to Table Editor > profiles**
- [ ] **Find the admin user row**
- [ ] **Edit the row**:
  - role: `admin`
  - full_name: `Admin User`
  - salesforce_id: `leave blank for now`
- [ ] **Save changes**

**Second User (Test BDM)**:
- [ ] **Go to Authentication > Users**
- [ ] **Click "Add user"**
- [ ] **Email**: `test@sherminfinance.co.uk`
- [ ] **Password**: (Choose strong password - save it!)
- [ ] **Auto Confirm User**: ON
- [ ] **Click "Create user"**
- [ ] **Go to Table Editor > profiles**
- [ ] **Find the test user row**
- [ ] **Edit the row**:
  - role: `user`
  - full_name: `Test BDM`
  - salesforce_id: `0051t00000ABC123` (example ID - we'll update later)
- [ ] **Save changes**

### Step 2.5: Get Environment Variables
- [ ] **Go to Settings > API**
- [ ] **Copy these values**:
  - Project URL: `SUPABASE_URL`
  - anon public key: `SUPABASE_ANON_KEY`
- [ ] **Add to .env file** (next phase)

---

## 🔧 Phase 3: Code Implementation

### Step 3.1: Install Dependencies
- [ ] **Activate virtual environment**: `source venv/bin/activate`
- [ ] **Install Supabase**: `pip install supabase`
- [ ] **Update requirements.txt**: Add `supabase>=2.0.0`

### Step 3.2: Update Environment Variables
- [ ] **Add to .env file**:
```
# Existing Salesforce variables (keep these)
SF_USERNAME=your.email@sherminfinance.co.uk
SF_PASSWORD=your_password
SF_TOKEN=your_security_token
SF_DOMAIN=login

# New Supabase variables
SUPABASE_URL=https://[your-project-id].supabase.co
SUPABASE_ANON_KEY=your-anon-key-here

# Flask config (keep existing)
PORT=8080
```

### Step 3.3: Create Supabase Client
- [ ] **Create new file**: `supabase_client.py`
- [ ] **Add Supabase initialization code**
- [ ] **Test connection to Supabase**

### Step 3.4: Update Authentication Functions
- [ ] **Backup current web_app.py**: `cp web_app.py web_app.py.backup`
- [ ] **Update login route**: Replace hardcoded password with Supabase auth
- [ ] **Update session management**: Store user info in session
- [ ] **Keep all existing routes unchanged**

### Step 3.5: Update Login Page HTML
- [ ] **Modify login form**: Add proper email field
- [ ] **Update form validation**: Email + password instead of just password
- [ ] **Keep existing styling and branding**
- [ ] **Add basic error messages**

---

## 🧪 Phase 4: Testing Basic Auth

### Step 4.1: Local Testing
- [ ] **Start Flask app**: `python web_app.py`
- [ ] **Go to**: `http://localhost:8080`
- [ ] **Test admin login**:
  - Email: `admin@sherminfinance.co.uk`
  - Password: (the one you set)
  - Should redirect to main page
- [ ] **Test BDM login**:
  - Email: `test@sherminfinance.co.uk`
  - Password: (the one you set)
  - Should redirect to main page
- [ ] **Test invalid login**: Should show error
- [ ] **Test logout**: Should redirect to login page

### Step 4.2: Functionality Testing
- [ ] **Test retailer search**: Should work for both users
- [ ] **Test rate card generation**: Should work for both users
- [ ] **Test Excel download**: Should work
- [ ] **Test PDF download**: Should work
- [ ] **All users see ALL retailers** (no filtering yet)

### Step 4.3: Session Testing
- [ ] **Test session persistence**: Refresh page, should stay logged in
- [ ] **Test logout**: Should clear session
- [ ] **Test direct URL access**: Should redirect to login if not authenticated

---

## 🎯 Phase 5: Add Salesforce Filtering (Optional for later)

### Step 5.1: Research Salesforce Owner Field
- [ ] **Test Salesforce query**: Find the field that contains owner ID
- [ ] **Map test user to real Salesforce ID**
- [ ] **Update test user profile with real Salesforce ID**

### Step 5.2: Add Filtering Logic
- [ ] **Modify retailer search**: Add WHERE clause for user role filtering
- [ ] **Test admin sees all**: No filtering applied
- [ ] **Test user sees filtered**: Only retailers they own

---

## 🚀 Phase 6: Deployment

### Step 6.1: Environment Setup
- [ ] **Add Supabase env vars to Vercel**:
  - `SUPABASE_URL`
  - `SUPABASE_ANON_KEY`
- [ ] **Update requirements.txt in repo**

### Step 6.2: Staging Deployment
- [ ] **Deploy to preview URL first**
- [ ] **Test login on staging**
- [ ] **Test all functionality**

### Step 6.3: Production Deployment
- [ ] **Merge to main branch** (only when ready)
- [ ] **Deploy to production**
- [ ] **Update documentation**

---

## 📝 Notes & Troubleshooting

### Current Hardcoded System
- Password: `Sh3rminRat3Ch3ck`
- Session key: `shermin_rate_card_secret_key_2025`
- All routes protected with `is_authenticated()` function

### Common Issues
- **Supabase connection**: Check URL and keys
- **Virtual environment**: Ensure `supabase` package installed
- **Session management**: Check Flask secret key
- **Authentication errors**: Check Supabase user exists and confirmed

### Test Credentials (save these!)
- **Admin**: `admin@sherminfinance.co.uk` / [password you set]
- **Test User**: `test@sherminfinance.co.uk` / [password you set]

### Rollback Plan
If anything goes wrong:
```bash
git checkout main
# Production is unaffected
```

---

## 🎉 Success Criteria

### Phase 3 Success
- [ ] Can login with email/password
- [ ] Invalid credentials show error
- [ ] All existing functionality works
- [ ] Both users can access everything (no filtering yet)

### Phase 5 Success (if implemented)
- [ ] Admin user sees all retailers
- [ ] Regular user sees only their retailers
- [ ] All other functionality unchanged

### Final Success
- [ ] Production deployment works
- [ ] Old hardcoded password system completely replaced
- [ ] Individual user accounts working
- [ ] Documentation updated

---

**Current Status**: 🚀 Ready to start Phase 2 - Supabase Project Creation