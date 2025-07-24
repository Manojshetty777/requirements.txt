import streamlit as st
import pandas as pd
import requests
from urllib.parse import urlparse
import random
import time
from datetime import datetime
import io
import base64

# Configure Streamlit page (set first)
st.set_page_config(page_title="LinkedIn HR Profile Extractor", page_icon="📄", layout="wide")

# ------------------------------ Enhanced Styling ------------------------------ #
def set_enhanced_styling():
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        font-family: 'Poppins', sans-serif;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Global white text styling */
    .stApp * {
        color: white !important;
    }
    
    .block-container {
        padding-top: 2rem;
        animation: slideInFromTop 1.2s ease-out;
        backdrop-filter: blur(10px);
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        margin: 20px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    }
    
    @keyframes slideInFromTop {
        from { 
            transform: translateY(-100px); 
            opacity: 0; 
        }
        to { 
            transform: translateY(0); 
            opacity: 1; 
        }
    }
    
    /* Title Animation */
    h1 {
        background: linear-gradient(45deg, #FFD700, #FFA500, #FF6B6B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: titleGlow 2s ease-in-out infinite alternate;
        text-align: center;
        font-weight: 700 !important;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.5);
    }
    
    @keyframes titleGlow {
        from { 
            filter: brightness(1); 
            transform: scale(1);
        }
        to { 
            filter: brightness(1.2); 
            transform: scale(1.02);
        }
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white !important;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        animation: buttonPulse 2s infinite;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        background: linear-gradient(45deg, #4ECDC4, #FF6B6B);
    }
    
    @keyframes buttonPulse {
        0%, 100% { 
            box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
        }
        50% { 
            box-shadow: 0 4px 25px rgba(78, 205, 196, 0.5);
        }
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        animation: slideInFromLeft 1s ease-out;
    }
    
    @keyframes slideInFromLeft {
        from { 
            transform: translateX(-100px); 
            opacity: 0; 
        }
        to { 
            transform: translateX(0); 
            opacity: 1; 
        }
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
        backdrop-filter: blur(5px);
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #4ECDC4 !important;
        box-shadow: 0 0 10px rgba(78, 205, 196, 0.5) !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1);
        border-radius: 10px;
        animation: progressGlow 1.5s ease-in-out infinite alternate;
    }
    
    @keyframes progressGlow {
        from { 
            box-shadow: 0 0 5px rgba(78, 205, 196, 0.5);
        }
        to { 
            box-shadow: 0 0 20px rgba(78, 205, 196, 0.8);
        }
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: rgba(76, 175, 80, 0.2) !important;
        color: #4CAF50 !important;
        border-left: 5px solid #4CAF50 !important;
        animation: successSlide 0.5s ease-out;
    }
    
    .stError {
        background: rgba(244, 67, 54, 0.2) !important;
        color: #F44336 !important;
        border-left: 5px solid #F44336 !important;
        animation: errorShake 0.5s ease-out;
    }
    
    @keyframes successSlide {
        from { 
            transform: translateX(-20px); 
            opacity: 0; 
        }
        to { 
            transform: translateX(0); 
            opacity: 1; 
        }
    }
    
    @keyframes errorShake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        color: white !important;
        font-weight: 600 !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 0 0 10px 10px !important;
        backdrop-filter: blur(5px);
    }
    
    /* DataFrames */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        backdrop-filter: blur(10px);
        animation: fadeInUp 0.8s ease-out;
    }
    
    @keyframes fadeInUp {
        from { 
            transform: translateY(30px); 
            opacity: 0; 
        }
        to { 
            transform: translateY(0); 
            opacity: 1; 
        }
    }
    
    /* Profile Card Styling */
    .profile-card {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 20px;
        padding: 20px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        transition: all 0.3s ease;
        animation: cardFloat 3s ease-in-out infinite alternate;
    }
    
    .profile-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 45px rgba(31, 38, 135, 0.5);
    }
    
    @keyframes cardFloat {
        from { transform: translateY(0px); }
        to { transform: translateY(-3px); }
    }
    
    .profile-photo {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        border: 3px solid #4ECDC4;
        box-shadow: 0 0 20px rgba(78, 205, 196, 0.5);
        animation: photoGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes photoGlow {
        from { 
            box-shadow: 0 0 20px rgba(78, 205, 196, 0.5);
        }
        to { 
            box-shadow: 0 0 30px rgba(78, 205, 196, 0.8);
        }
    }
    
    /* Floating particles background */
    .particle {
        position: fixed;
        top: -10px;
        animation: float 15s infinite linear;
        opacity: 0.6;
        z-index: -1;
    }
    
    @keyframes float {
        to {
            transform: translateY(calc(100vh + 10px));
        }
    }
    
    /* Modal/Popup Styling */
    .popup-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.7);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
        animation: fadeIn 0.3s ease-out;
    }
    
    .popup-content {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 30px;
        max-width: 500px;
        width: 90%;
        border: 1px solid rgba(255, 255, 255, 0.3);
        animation: popupSlide 0.4s ease-out;
    }
    
    @keyframes popupSlide {
        from { 
            transform: scale(0.8) translateY(-50px); 
            opacity: 0; 
        }
        to { 
            transform: scale(1) translateY(0); 
            opacity: 1; 
        }
    }
    
    /* Checkbox styling */
    .stCheckbox > label {
        color: white !important;
        font-weight: 500;
    }
    
    /* File uploader */
    .uploadedFile {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        color: white !important;
    }
    
    /* Metrics */
    .metric-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        animation: metricPulse 2s ease-in-out infinite;
    }
    
    @keyframes metricPulse {
        0%, 100% { 
            transform: scale(1);
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
        }
        50% { 
            transform: scale(1.02);
            box-shadow: 0 0 30px rgba(255, 255, 255, 0.2);
        }
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_enhanced_styling()

# Add floating particles
def add_floating_particles():
    particles_html = """
    <div id="particles-container"></div>
    <script>
    function createParticle() {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.innerHTML = ['💼', '👔', '📊', '🎯', '⭐', '💡'][Math.floor(Math.random() * 6)];
        particle.style.left = Math.random() * 100 + 'vw';
        particle.style.animationDuration = (Math.random() * 10 + 10) + 's';
        particle.style.opacity = Math.random() * 0.8 + 0.2;
        document.body.appendChild(particle);
        
        setTimeout(() => {
            particle.remove();
        }, 20000);
    }
    
    setInterval(createParticle, 3000);
    </script>
    """
    st.markdown(particles_html, unsafe_allow_html=True)

add_floating_particles()

# ------------------------------ Enhanced Helper Class ------------------------------ #
class EnhancedLinkedInScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.hr_certifications = {
            'SHRM-CP': ('SHRM', 'HR Management'),
            'PHR': ('HRCI', 'HR Professional'),
            'SPHR': ('HRCI', 'Senior HR Professional'),
            'CHRP': ('HRPA', 'Chartered HR Professional'),
            'GPHR': ('HRCI', 'Global Professional in HR'),
            'SHRM-SCP': ('SHRM', 'Senior Certified Professional'),
            'CCP': ('WorldatWork', 'Certified Compensation Professional'),
            'CEBS': ('IFEBP', 'Certified Employee Benefit Specialist')
        }
        self.hr_keywords = ['human resources', 'hr', 'talent', 'recruit', 'people', 'employee', 'organizational development', 'workforce']
        
        # Sample profile photos (placeholder URLs)
        self.sample_photos = [
            "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face",
            "https://images.unsplash.com/photo-1494790108755-2616b612b587?w=150&h=150&fit=crop&crop=face",
            "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face",
            "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop&crop=face",
            "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&h=150&fit=crop&crop=face",
            "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&h=150&fit=crop&crop=face"
        ]

    def is_valid_linkedin_url(self, url):
        parsed = urlparse(url)
        return 'linkedin.com' in parsed.netloc and '/in/' in parsed.path

    def generate_detailed_profile(self, url):
        """Generate comprehensive profile data with enhanced details"""
        profile_id = hash(url) % 10000
        
        # Enhanced profile data
        first_names = ['Sarah', 'Michael', 'Jennifer', 'David', 'Emily', 'Robert', 'Lisa', 'John', 'Jessica', 'Christopher']
        last_names = ['Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez']
        
        companies = [
            'Google', 'Microsoft', 'Amazon', 'Apple', 'Meta', 'Tesla', 'Netflix', 'Salesforce', 
            'Adobe', 'Oracle', 'IBM', 'Intel', 'Cisco', 'PayPal', 'Uber', 'Airbnb'
        ]
        
        hr_titles = [
            'Senior HR Manager', 'Talent Acquisition Specialist', 'People Operations Lead',
            'HR Business Partner', 'Recruitment Manager', 'Employee Experience Manager',
            'Organizational Development Specialist', 'HR Generalist', 'Talent Development Manager',
            'Workforce Analytics Manager', 'Compensation & Benefits Specialist', 'HR Director'
        ]
        
        locations = [
            'San Francisco, CA', 'New York, NY', 'Seattle, WA', 'Austin, TX', 'Chicago, IL',
            'Boston, MA', 'Los Angeles, CA', 'Denver, CO', 'Atlanta, GA', 'Miami, FL'
        ]
        
        # Generate profile
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        company = random.choice(companies)
        title = random.choice(hr_titles)
        location = random.choice(locations)
        photo = random.choice(self.sample_photos)
        
        # Experience years
        years_exp = random.randint(2, 15)
        
        # Skills
        hr_skills = [
            'Talent Acquisition', 'Employee Relations', 'Performance Management', 'HRIS',
            'Compensation & Benefits', 'Training & Development', 'Employment Law', 'Analytics',
            'Change Management', 'Diversity & Inclusion', 'Organizational Psychology', 'Leadership'
        ]
        selected_skills = random.sample(hr_skills, random.randint(4, 8))
        
        # Education
        universities = ['Stanford', 'Harvard', 'MIT', 'UC Berkeley', 'Northwestern', 'Penn State']
        degrees = ['MBA', 'MS in HR Management', 'BA in Psychology', 'MS in Organizational Psychology']
        
        return {
            'profile_name': name,
            'company_name': company,
            'job_title': title,
            'department': 'Human Resources',
            'location': location,
            'profile_photo': photo,
            'years_experience': years_exp,
            'skills': selected_skills,
            'education': f"{random.choice(degrees)} from {random.choice(universities)}",
            'employee_count': f"{random.randint(50, 500)}+ employees managed",
            'certifications': self.generate_sample_certs(),
            'summary': f"Experienced {title.lower()} with {years_exp}+ years in HR operations, specializing in talent management and organizational development.",
            'linkedin_url': url,
            'last_updated': datetime.now().strftime("%Y-%m-%d"),
            'profile_strength': random.choice(['Beginner', 'Intermediate', 'Advanced', 'Expert'])
        }

    def generate_sample_certs(self):
        certs = list(self.hr_certifications.keys())
        selected_certs = random.sample(certs, random.randint(0, 3))
        
        return [{
            'name': cert,
            'provider': self.hr_certifications[cert][0],
            'type': self.hr_certifications[cert][1],
            'issued_date': f"{random.randint(1,12):02d}/{random.randint(2020,2023)}",
            'renewal_date': f"{random.randint(1,12):02d}/{random.randint(2024,2026)}",
            'credential_id': f"CERT-{random.randint(100000, 999999)}"
        } for cert in selected_certs]

    def is_hr_related(self, title, dept):
        return any(k in f"{title} {dept}".lower() for k in self.hr_keywords)

    def process_urls(self, urls, update_cb=None):
        results = []
        detailed_profiles = []
        
        for i, url in enumerate(urls):
            if update_cb:
                update_cb(i + 1, len(urls))
            
            if not self.is_valid_linkedin_url(url):
                continue
                
            # Add realistic delay
            time.sleep(random.uniform(0.5, 1.5))
            
            profile_data = self.generate_detailed_profile(url)
            detailed_profiles.append(profile_data)
            
            # Create base record
            base = {
                'profile_url': url,
                'profile_name': profile_data['profile_name'],
                'company_name': profile_data['company_name'],
                'job_title': profile_data['job_title'],
                'department': profile_data['department'],
                'location': profile_data['location'],
                'years_experience': profile_data['years_experience'],
                'education': profile_data['education'],
                'skills_count': len(profile_data['skills']),
                'is_hr_related': self.is_hr_related(profile_data['job_title'], profile_data['department'])
            }
            
            # Handle certifications
            if not profile_data['certifications']:
                results.append({
                    **base, 
                    'certification': '', 
                    'provider': '', 
                    'type': '', 
                    'issued': '', 
                    'renewal': '',
                    'credential_id': ''
                })
            else:
                for cert in profile_data['certifications']:
                    results.append({
                        **base, 
                        'certification': cert['name'], 
                        'provider': cert['provider'], 
                        'type': cert['type'], 
                        'issued': cert['issued_date'], 
                        'renewal': cert['renewal_date'],
                        'credential_id': cert['credential_id']
                    })
        
        return results, detailed_profiles

# ------------------------------ Profile Card Component ------------------------------ #
def create_profile_card(profile_data):
    """Create an enhanced profile card with detailed information"""
    
    skills_html = "".join([f'<span style="background: rgba(78, 205, 196, 0.3); padding: 4px 8px; border-radius: 15px; margin: 2px; font-size: 12px; display: inline-block;">{skill}</span>' for skill in profile_data['skills'][:6]])
    
    certs_html = ""
    if profile_data['certifications']:
        certs_html = "<br>".join([f"🏆 <strong>{cert['name']}</strong> ({cert['provider']})" for cert in profile_data['certifications']])
    else:
        certs_html = "No certifications listed"
    
    card_html = f"""
    <div class="profile-card" onclick="showProfilePopup('{profile_data['profile_name']}')">
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <img src="{profile_data['profile_photo']}" class="profile-photo" style="margin-right: 15px;">
            <div>
                <h3 style="margin: 0; color: #4ECDC4; font-weight: 600;">{profile_data['profile_name']}</h3>
                <p style="margin: 5px 0; color: #FFD700; font-weight: 500;">{profile_data['job_title']}</p>
                <p style="margin: 0; opacity: 0.8; font-size: 14px;">📍 {profile_data['location']}</p>
            </div>
        </div>
        
        <div style="margin-bottom: 10px;">
            <strong>🏢 Company:</strong> {profile_data['company_name']}<br>
            <strong>⏱️ Experience:</strong> {profile_data['years_experience']} years<br>
            <strong>🎓 Education:</strong> {profile_data['education']}<br>
            <strong>👥 Team Size:</strong> {profile_data['employee_count']}
        </div>
        
        <div style="margin-bottom: 10px;">
            <strong>💪 Top Skills:</strong><br>
            <div style="margin-top: 5px;">{skills_html}</div>
        </div>
        
        <div style="margin-bottom: 10px;">
            <strong>🏆 Certifications:</strong><br>
            <div style="margin-top: 5px; font-size: 14px;">{certs_html}</div>
        </div>
        
        <div style="border-top: 1px solid rgba(255,255,255,0.2); padding-top: 10px; margin-top: 10px;">
            <p style="font-style: italic; opacity: 0.9; font-size: 14px;">"{profile_data['summary']}"</p>
            <div style="display: flex; justify-content: space-between; font-size: 12px; opacity: 0.7;">
                <span>Profile Strength: {profile_data['profile_strength']}</span>
                <span>Updated: {profile_data['last_updated']}</span>
            </div>
        </div>
    </div>
    """
    
    return card_html

# ------------------------------ Main UI ------------------------------ #
st.markdown("""
<h1>🚀 LinkedIn HR Profile Extractor Pro</h1>
<div style="text-align: center; margin-bottom: 30px; animation: fadeIn 1s ease-in;">
    <p style="font-size: 18px; opacity: 0.9;">
        🔍 Extract comprehensive HR professional data with enhanced analytics and beautiful visualizations
    </p>
    <p style="font-size: 14px; opacity: 0.7;">
        ⚡ This is a demo application with simulated data for demonstration purposes
    </p>
</div>
""", unsafe_allow_html=True)

# Initialize scraper
scraper = EnhancedLinkedInScraper()

# Sidebar with enhanced styling
st.sidebar.markdown("### 🎛️ Filter Settings")
filter_hr = st.sidebar.checkbox("🎯 Only HR-related profiles", False)
filter_cert = st.sidebar.checkbox("🏆 Only certified profiles", False)
min_experience = st.sidebar.slider("📈 Minimum years of experience", 0, 15, 0)

st.sidebar.markdown("### 📊 Export Options")
export_format = st.sidebar.selectbox("Choose export format", ["CSV", "Excel", "JSON"])
include_photos = st.sidebar.checkbox("📸 Include profile photos in export", True)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    with st.expander("📤 Upload LinkedIn URLs", expanded=True):
        uploaded_file = st.file_uploader(
            "Upload CSV/Excel file with LinkedIn URLs", 
            type=['csv', 'xlsx'],
            help="Upload a file containing LinkedIn profile URLs"
        )
        
        manual_input = st.text_area(
            "Or paste LinkedIn URLs (one per line):",
            height=150,
            placeholder="https://linkedin.com/in/example-profile-1\nhttps://linkedin.com/in/example-profile-2"
        )

with col2:
    st.markdown("""
    <div class="metric-container">
        <h4>📈 Quick Stats</h4>
        <div id="stats-content">Ready to process profiles...</div>
    </div>
    """, unsafe_allow_html=True)

# Process URLs
urls = []
df = None

if uploaded_file:
    try:
        if uploaded_file.name.endswith("csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        url_col = st.selectbox("🔗 Select the column with LinkedIn URLs", df.columns)
        urls = df[url_col].dropna().tolist()
        
        st.success(f"✅ Successfully loaded {len(urls)} URLs from file!")
        
    except Exception as e:
        st.error(f"❌ Failed to process file: {str(e)}")

elif manual_input:
    urls = [line.strip() for line in manual_input.strip().split('\n') if line.strip()]
    if urls:
        st.success(f"✅ Loaded {len(urls)} URLs from manual input!")

# Main processing button
if st.button("🚀 Extract Profiles", disabled=not urls) and urls:
    # Show processing animation
    st.markdown("""
    <div style="text-align: center; margin: 20px 0;">
        <div style="display: inline-block; animation: spin 1s linear infinite;">🔄</div>
        <h3 style="color: #4ECDC4;">Processing profiles... Please wait</h3>
    </div>
    <style>
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
    """, unsafe_allow_html=True)
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    def update_progress(current, total):
        progress = current / total
        progress_bar.progress(progress)
        status_text.markdown(f"<div style='text-align: center; color: #4ECDC4;'>Processing profile {current} of {total} ({progress:.1%} complete)</div>", unsafe_allow_html=True)
    
    # Process profiles
    try:
        data, detailed_profiles = scraper.process_urls(urls, update_progress)
        df_result = pd.DataFrame(data)
        
        # Apply filters
        if filter_hr:
            df_result = df_result[df_result['is_hr_related']]
            detailed_profiles = [p for p in detailed_profiles if scraper.is_hr_related(p['job_title'], p['department'])]
        
        if filter_cert:
            df_result = df_result[df_result['certification']