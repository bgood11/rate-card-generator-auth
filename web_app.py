# web_app.py
from flask import Flask, render_template, request, send_file, jsonify, send_from_directory, session, redirect, url_for
import os
from rate_card_generator import RateCardGenerator
from pdf_generator import PDFGenerator
from supabase_client import authenticate_user, get_user_profile
from dotenv import load_dotenv
import tempfile
import json

load_dotenv()

app = Flask(__name__, static_folder='static')
app.secret_key = 'shermin_rate_card_secret_key_2025'  # For session management

def get_current_user():
    """Get current user profile from session"""
    return session.get('user_profile')

# Initialize Salesforce connection
generator = None

def get_generator():
    global generator
    if generator is None:
        generator = RateCardGenerator(
            os.getenv('SF_USERNAME'),
            os.getenv('SF_PASSWORD'),
            os.getenv('SF_TOKEN'),
            os.getenv('SF_DOMAIN', 'login')
        )
    return generator

def is_authenticated():
    return session.get('authenticated', False)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        
        # Authenticate with Supabase
        auth_response = authenticate_user(email, password)
        
        if auth_response and auth_response.user:
            # Get user profile from database
            user_profile = get_user_profile(auth_response.user.id)
            
            if user_profile:
                # Store authentication and user info in session
                session['authenticated'] = True
                session['user_profile'] = user_profile
                session['user_email'] = email
                return redirect(url_for('index'))
            else:
                return render_login_page(error="User profile not found. Please contact administrator.")
        else:
            return render_login_page(error="Invalid email or password. Please try again.")
    
    return render_login_page()

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    session.pop('user_profile', None)
    session.pop('user_email', None)
    return redirect(url_for('login'))

def render_login_page(error=None):
    error_html = f'<div style="color: red; text-align: center; margin: 10px;">{error}</div>' if error else ''
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Stax Rate Card Generator - Login</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 500px; margin: 0 auto; padding: 20px; background: #f9f9f9; }}
            .logo-container {{ text-align: center; margin-bottom: 30px; }}
            .logo {{ max-width: 200px; height: auto; }}
            h1 {{ color: #477085; text-align: center; margin-top: 20px; }}
            .login-form {{ background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }}
            input {{ padding: 12px; font-size: 16px; border-radius: 4px; border: 1px solid #ddd; width: 250px; margin: 10px; }}
            button {{ 
                background-color: #2ab7e3; 
                color: white; 
                border: none; 
                cursor: pointer; 
                padding: 12px 30px;
                font-size: 16px;
                border-radius: 4px;
                margin: 20px;
                transition: background-color 0.3s;
            }}
            button:hover {{ background-color: #1a97c3; }}
            .beta-notice {{ 
                background: #fff3cd; 
                border: 1px solid #ffeaa7; 
                color: #856404; 
                padding: 15px; 
                border-radius: 4px; 
                margin-bottom: 20px; 
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="logo-container">
            <img src="/static/stax-logo.png" alt="Stax Logo" class="logo">
        </div>
        
        <h1>Rate Card Generator</h1>
        
        <div class="beta-notice">
            <strong>Staff Login Required</strong><br>
            Please login with your Shermin Finance email and password to access the Rate Card Generator.
        </div>
        
        <div class="login-form">
            <form method="POST">
                <div>
                    <input type="email" name="email" placeholder="Email address" required>
                </div>
                <div>
                    <input type="password" name="password" placeholder="Password" required>
                </div>
                <div>
                    <button type="submit">Login</button>
                </div>
            </form>
            {error_html}
        </div>
    </body>
    </html>
    '''

@app.route('/dashboard-test')
def dashboard_test():
    if not is_authenticated():
        return redirect(url_for('login'))
    user_profile = get_current_user()
    return render_template('dashboard.html', user=user_profile)

@app.route('/')
def index():
    if not is_authenticated():
        return redirect(url_for('login'))
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Stax Rate Card Generator</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; background: #f9f9f9; }
            .header-container { position: relative; }
            .logout-btn { 
                position: absolute; 
                top: 10px; 
                right: 10px; 
                background-color: #666; 
                color: white; 
                padding: 8px 15px; 
                font-size: 14px; 
                text-decoration: none; 
                border-radius: 4px;
                transition: background-color 0.3s;
            }
            .logout-btn:hover { background-color: #555; }
            .logo-container { text-align: center; margin-bottom: 30px; }
            .logo { max-width: 300px; height: auto; }
            h1 { color: #477085; text-align: center; margin-top: 20px; }
            h2 { color: #477085; margin-top: 30px; margin-bottom: 15px; }
            .form-group { margin-bottom: 20px; text-align: center; }
            input, button { padding: 10px; font-size: 16px; border-radius: 4px; }
            input { width: 300px; border: 1px solid #ddd; }
            button { 
                background-color: #2ab7e3; 
                color: white; 
                border: none; 
                cursor: pointer; 
                margin: 0 5px;
                transition: background-color 0.3s;
            }
            button:hover { background-color: #1a97c3; }
            button:disabled { 
                background-color: #ccc; 
                cursor: not-allowed; 
            }
            .download-button {
                background-color: #477085;
                padding: 12px 24px;
                font-size: 18px;
                margin: 10px;
            }
            .download-button:hover { background-color: #365566; }
            #results { margin-top: 20px; }
            .retailer-option { 
                padding: 10px; 
                cursor: pointer; 
                border: 1px solid #ddd; 
                margin: 5px 0; 
                background: white;
                border-radius: 4px;
                transition: all 0.2s;
            }
            .retailer-option:hover { 
                background-color: #e8f4f8; 
                border-color: #2ab7e3;
                transform: translateX(5px);
            }
            #status { margin-top: 20px; color: #666; text-align: center; }
            
            /* Rate card display styles */
            #rateCardDisplay {
                display: none;
                margin-top: 30px;
                background: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .rate-card-header {
                border-bottom: 2px solid #477085;
                padding-bottom: 20px;
                margin-bottom: 30px;
            }
            .rate-card-header h2 {
                margin: 0;
                color: #477085;
            }
            .generation-date {
                color: #666;
                font-size: 14px;
                margin-top: 5px;
            }
            .download-section {
                text-align: center;
                margin: 30px 0;
                padding: 20px;
                background: #f5f5f5;
                border-radius: 8px;
            }
            .rate-table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 30px;
            }
            .rate-table th {
                background-color: #477085;
                color: white;
                padding: 12px;
                text-align: left;
                font-weight: bold;
            }
            .rate-table td {
                padding: 10px;
                border-bottom: 1px solid #ddd;
            }
            .rate-table tr:nth-child(even) {
                background-color: #f5f5f5;
            }
            .rate-table tr:hover {
                background-color: #e8f4f8;
            }
            .product-vertical-section {
                margin-bottom: 40px;
            }
            .product-vertical-title {
                color: #477085;
                font-size: 20px;
                margin-bottom: 15px;
                padding-bottom: 10px;
                border-bottom: 1px solid #ddd;
            }
            .loading-spinner {
                display: inline-block;
                width: 20px;
                height: 20px;
                border: 3px solid #f3f3f3;
                border-top: 3px solid #2ab7e3;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin-left: 10px;
                vertical-align: middle;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <div class="header-container">
            <a href="/logout" class="logout-btn">Logout</a>
            <div class="logo-container">
                <img src="/static/stax-logo.png" alt="Stax - Simply. Payments." class="logo" style="max-width: 200px; height: auto;">
            </div>
            <h1>Rate Card Generator</h1>
        </div>
        <div class="form-group">
            <input type="text" id="retailerSearch" placeholder="Enter retailer name..." />
            <button onclick="searchRetailers()">Search</button>
        </div>
        <!-- Commission checkbox only shown for admin users -->
        <div class="form-group" id="commissionGroup" style="display: none;">
            <label style="display: flex; align-items: center; justify-content: center; gap: 8px; font-size: 14px; color: #666;">
                <input type="checkbox" id="hideSherminCommissions" style="margin: 0;">
                Hide Shermin Commissions?
            </label>
        </div>
        <div id="results"></div>
        <div id="status"></div>
        
        <div id="rateCardDisplay">
            <div class="rate-card-header">
                <h2 id="retailerTitle"></h2>
                <div class="generation-date" id="generationDate"></div>
            </div>
            
            <div class="download-section">
                <h3>Download Rate Card</h3>
                <button class="download-button" onclick="downloadExcel()">📊 Download as Excel</button>
                <button class="download-button" onclick="downloadPDF()">📄 Download as PDF</button>
            </div>
            
            <div id="rateCardContent"></div>
        </div>
        
        <script>
            let currentRetailer = null;
            let currentRateCardData = null;
            let userRole = null;
            
            // Get user info and show commission checkbox for admin users
            async function initializeUserInterface() {
                try {
                    const response = await fetch('/user-info');
                    const userInfo = await response.json();
                    userRole = userInfo.role;
                    
                    // Show commission checkbox only for admin users
                    if (userRole === 'admin') {
                        document.getElementById('commissionGroup').style.display = 'block';
                    }
                } catch (error) {
                    console.error('Failed to get user info:', error);
                }
            }
            
            // Initialize on page load
            document.addEventListener('DOMContentLoaded', initializeUserInterface);
            async function searchRetailers() {
                const search = document.getElementById('retailerSearch').value;
                if (!search) return;
                
                document.getElementById('status').textContent = 'Searching...';
                document.getElementById('results').innerHTML = '';
                
                try {
                    const response = await fetch('/search?q=' + encodeURIComponent(search));
                    const data = await response.json();
                    
                    // Check if the response is an error
                    if (data.error) {
                        document.getElementById('status').textContent = 'Error: ' + data.error;
                        document.getElementById('results').innerHTML = '';
                        return;
                    }
                    
                    // Handle successful response (array of retailers)
                    if (data.length === 0) {
                        document.getElementById('results').innerHTML = '<p>No retailers found</p>';
                    } else {
                        const html = data.map(r => 
                            `<div class="retailer-option" onclick="generateRateCard('${r.name}')">${r.name}</div>`
                        ).join('');
                        document.getElementById('results').innerHTML = html;
                    }
                    document.getElementById('status').textContent = '';
                } catch (error) {
                    document.getElementById('status').textContent = 'Error: ' + error.message;
                    document.getElementById('results').innerHTML = '';
                }
            }
            
            async function generateRateCard(retailerName) {
                document.getElementById('status').innerHTML = 'Generating rate card for ' + retailerName + '...<span class="loading-spinner"></span>';
                document.getElementById('results').innerHTML = '';
                currentRetailer = retailerName;
                
                // Get commission setting - always true for BDMs, checkbox value for admins
                const commissionCheckbox = document.getElementById('hideSherminCommissions');
                const hideCommissions = userRole === 'admin' ? (commissionCheckbox ? commissionCheckbox.checked : false) : true;
                
                try {
                    const response = await fetch('/generate-data', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({retailer: retailerName, hide_commissions: hideCommissions})
                    });
                    
                    if (response.ok) {
                        const data = await response.json();
                        currentRateCardData = data;
                        displayRateCard(data);
                        document.getElementById('status').textContent = '';
                    } else {
                        throw new Error('Failed to generate rate card');
                    }
                } catch (error) {
                    document.getElementById('status').textContent = 'Error: ' + error.message;
                }
            }
            
            function displayRateCard(data) {
                // Update header
                document.getElementById('retailerTitle').textContent = currentRetailer + ' - Rate Card Analysis';
                document.getElementById('generationDate').textContent = 'Generated: ' + new Date().toLocaleDateString('en-GB', { 
                    day: 'numeric', 
                    month: 'long', 
                    year: 'numeric' 
                });
                
                // Clear and populate content
                const contentDiv = document.getElementById('rateCardContent');
                contentDiv.innerHTML = '';
                
                // Process each product vertical
                for (const [vertical, rows] of Object.entries(data)) {
                    if (rows.length === 0) continue;
                    
                    const section = document.createElement('div');
                    section.className = 'product-vertical-section';
                    
                    const title = document.createElement('h3');
                    title.className = 'product-vertical-title';
                    title.textContent = vertical + ' Waterfall';
                    section.appendChild(title);
                    
                    const table = document.createElement('table');
                    table.className = 'rate-table';
                    
                    // Check if we should hide commissions
                    // Get commission setting - always true for BDMs, checkbox value for admins
                const commissionCheckbox = document.getElementById('hideSherminCommissions');
                const hideCommissions = userRole === 'admin' ? (commissionCheckbox ? commissionCheckbox.checked : false) : true;
                    
                    // Header
                    const thead = document.createElement('thead');
                    const headerRow = document.createElement('tr');
                    const headers = hideCommissions 
                        ? ['Lender', 'Position', 'Term', 'Product Type', 'Deferred Period', 'APR Range', 'Subsidy']
                        : ['Lender', 'Position', 'Shermin Commission', 'Term', 'Product Type', 'Deferred Period', 'APR Range', 'Subsidy'];
                    
                    headers.forEach(header => {
                        const th = document.createElement('th');
                        th.textContent = header;
                        headerRow.appendChild(th);
                    });
                    thead.appendChild(headerRow);
                    table.appendChild(thead);
                    
                    // Body
                    const tbody = document.createElement('tbody');
                    rows.forEach(row => {
                        const tr = document.createElement('tr');
                        const dataKeys = hideCommissions 
                            ? ['Lender_Name', 'Position', 'Term', 'Product_Type', 'Deferred_Period', 'APR_Range', 'Subsidy']
                            : ['Lender_Name', 'Position', 'Shermin_Commission', 'Term', 'Product_Type', 'Deferred_Period', 'APR_Range', 'Subsidy'];
                        
                        dataKeys.forEach(key => {
                            const td = document.createElement('td');
                            td.textContent = row[key] || '';
                            tr.appendChild(td);
                        });
                        tbody.appendChild(tr);
                    });
                    table.appendChild(tbody);
                    
                    section.appendChild(table);
                    contentDiv.appendChild(section);
                }
                
                // Show the rate card display
                document.getElementById('rateCardDisplay').style.display = 'block';
            }
            
            async function downloadExcel() {
                if (!currentRetailer) return;
                
                document.getElementById('status').innerHTML = 'Generating Excel file...<span class="loading-spinner"></span>';
                
                // Get commission setting - always true for BDMs, checkbox value for admins
                const commissionCheckbox = document.getElementById('hideSherminCommissions');
                const hideCommissions = userRole === 'admin' ? (commissionCheckbox ? commissionCheckbox.checked : false) : true;
                
                try {
                    const response = await fetch('/generate', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({retailer: currentRetailer, hide_commissions: hideCommissions})
                    });
                    
                    if (response.ok) {
                        const blob = await response.blob();
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = currentRetailer.replace(/[^a-z0-9]/gi, '_') + '_Rate_Card.xlsx';
                        document.body.appendChild(a);
                        a.click();
                        window.URL.revokeObjectURL(url);
                        document.getElementById('status').textContent = '✅ Excel downloaded!';
                        setTimeout(() => { document.getElementById('status').textContent = ''; }, 3000);
                    } else {
                        throw new Error('Failed to generate Excel');
                    }
                } catch (error) {
                    document.getElementById('status').textContent = 'Error: ' + error.message;
                }
            }
            
            async function downloadPDF() {
                if (!currentRetailer) return;
                
                document.getElementById('status').innerHTML = 'Generating PDF file...<span class="loading-spinner"></span>';
                
                // Get commission setting - always true for BDMs, checkbox value for admins
                const commissionCheckbox = document.getElementById('hideSherminCommissions');
                const hideCommissions = userRole === 'admin' ? (commissionCheckbox ? commissionCheckbox.checked : false) : true;
                
                try {
                    const response = await fetch('/generate-pdf', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({retailer: currentRetailer, hide_commissions: hideCommissions})
                    });
                    
                    if (response.ok) {
                        const blob = await response.blob();
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = currentRetailer.replace(/[^a-z0-9]/gi, '_') + '_Rate_Card.pdf';
                        document.body.appendChild(a);
                        a.click();
                        window.URL.revokeObjectURL(url);
                        document.getElementById('status').textContent = '✅ PDF downloaded!';
                        setTimeout(() => { document.getElementById('status').textContent = ''; }, 3000);
                    } else {
                        throw new Error('Failed to generate PDF');
                    }
                } catch (error) {
                    document.getElementById('status').textContent = 'Error: ' + error.message;
                }
            }
        </script>
    </body>
    </html>
    '''

@app.route('/search')
def search_retailers():
    if not is_authenticated():
        return jsonify({'error': 'Authentication required'}), 401
    
    query = request.args.get('q', '')
    user_profile = get_current_user()
    
    try:
        gen = get_generator()
        
        # Apply user-based filtering
        if user_profile['role'] == 'admin':
            # Admin users see all retailers
            retailers = gen.find_retailer(query)
        else:
            # Regular users only see retailers they own
            salesforce_id = user_profile.get('salesforce_id')
            if not salesforce_id:
                return jsonify({'error': 'User profile missing Salesforce ID. Please contact administrator.'}), 400
            retailers = gen.find_retailer(query, salesforce_id)
        
        return jsonify([{'name': r['Name'], 'id': r['Id']} for r in retailers[:20]])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/user-info')
def user_info():
    """Get current user info for client-side logic"""
    if not is_authenticated():
        return jsonify({'error': 'Authentication required'}), 401
    
    user_profile = get_current_user()
    return jsonify({
        'role': user_profile['role'],
        'email': user_profile['email'],
        'name': user_profile['full_name']
    })

@app.route('/generate-data', methods=['POST'])
def generate_data():
    """Generate rate card data and return as JSON for display"""
    if not is_authenticated():
        return jsonify({'error': 'Authentication required'}), 401
    retailer_name = request.json.get('retailer')
    hide_commissions = request.json.get('hide_commissions', False)
    
    # For BDM users, always hide commissions regardless of checkbox
    user_profile = get_current_user()
    if user_profile['role'] != 'admin':
        hide_commissions = True
    try:
        gen = get_generator()
        rate_card_data = gen.process_rate_cards(retailer_name)
        
        # Convert DataFrames to JSON-serializable format
        json_data = {}
        for vertical, df in rate_card_data.items():
            json_data[vertical] = df.to_dict('records')
        
        return jsonify(json_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate', methods=['POST'])
def generate():
    """Generate Excel file"""
    if not is_authenticated():
        return jsonify({'error': 'Authentication required'}), 401
    
    retailer_name = request.json.get('retailer')
    hide_commissions = request.json.get('hide_commissions', False)
    
    # For BDM users, always hide commissions regardless of checkbox
    user_profile = get_current_user()
    if user_profile['role'] != 'admin':
        hide_commissions = True
        
    try:
        gen = get_generator()
        rate_card_data = gen.process_rate_cards(retailer_name)
        
        # Generate Excel in temp file
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            output_path = tmp.name
        
        gen.generate_excel(retailer_name, rate_card_data, output_path, hide_commissions)
        
        return send_file(output_path, as_attachment=True,
                        download_name=f"{retailer_name}_Rate_Card.xlsx",
                        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    """Generate PDF file"""
    if not is_authenticated():
        return jsonify({'error': 'Authentication required'}), 401
    
    retailer_name = request.json.get('retailer')
    hide_commissions = request.json.get('hide_commissions', False)
    
    # For BDM users, always hide commissions regardless of checkbox
    user_profile = get_current_user()
    if user_profile['role'] != 'admin':
        hide_commissions = True
        
    try:
        gen = get_generator()
        rate_card_data = gen.process_rate_cards(retailer_name)
        
        # Generate PDF in temp file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            output_path = tmp.name
        
        pdf_gen = PDFGenerator()
        pdf_gen.generate_pdf(retailer_name, rate_card_data, output_path, hide_commissions)
        
        return send_file(output_path, as_attachment=True,
                        download_name=f"{retailer_name}_Rate_Card.pdf",
                        mimetype='application/pdf')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    print(f"Starting Rate Card Generator on port {port}")
    print(f"Open http://localhost:{port} in your browser")
    app.run(debug=False, host='0.0.0.0', port=port)
