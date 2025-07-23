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

# ------------------------------ Set Background ------------------------------ #
def set_background(image_file):
    with open(image_file, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_string}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_background("background.png")

# ------------------------------ Helper Class ------------------------------ #
class LinkedInScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.hr_certifications = {
            'SHRM-CP': ('SHRM', 'HR Management'),
            'PHR': ('HRCI', 'HR Professional'),
            'SPHR': ('HRCI', 'Senior HR Professional'),
            'CHRP': ('HRPA', 'Chartered HR Professional')
        }
        self.hr_keywords = ['human resources', 'hr', 'talent', 'recruit', 'people', 'employee']

    def is_valid_linkedin_url(self, url):
        parsed = urlparse(url)
        return 'linkedin.com' in parsed.netloc and '/in/' in parsed.path

    def extract_profile_data(self, url):
        time.sleep(0.5)
        return {
            'profile_name': f"User {hash(url) % 1000}",
            'company_name': f"Company {hash(url) % 100}",
            'job_title': random.choice(['HR Manager', 'Recruiter', 'People Ops Lead']),
            'department': 'HR',
            'location': 'USA',
            'certifications': self.generate_sample_certs()
        }

    def generate_sample_certs(self):
        certs = list(self.hr_certifications.keys())
        return [{
            'name': c,
            'provider': self.hr_certifications[c][0],
            'type': self.hr_certifications[c][1],
            'issued_date': f"{random.randint(1,12):02d}/{random.randint(2020,2023)}",
            'renewal_date': f"{random.randint(1,12):02d}/{random.randint(2024,2026)}"
        } for c in random.sample(certs, random.randint(0, len(certs)))]

    def is_hr_related(self, title, dept):
        return any(k in f"{title} {dept}".lower() for k in self.hr_keywords)

    def process_urls(self, urls, update_cb=None):
        results = []
        for i, url in enumerate(urls):
            if update_cb:
                update_cb(i + 1, len(urls))
            if not self.is_valid_linkedin_url(url):
                continue
            data = self.extract_profile_data(url)
            base = {
                'profile_url': url,
                'profile_name': data['profile_name'],
                'company_name': data['company_name'],
                'job_title': data['job_title'],
                'department': data['department'],
                'location': data['location'],
                'is_hr_related': self.is_hr_related(data['job_title'], data['department'])
            }
            if not data['certifications']:
                results.append({**base, 'certification': '', 'provider': '', 'type': '', 'issued': '', 'renewal': ''})
            else:
                for cert in data['certifications']:
                    results.append({**base, 'certification': cert['name'], 'provider': cert['provider'], 'type': cert['type'], 'issued': cert['issued_date'], 'renewal': cert['renewal_date']})
        return results

# ------------------------------ UI Layout ------------------------------ #
st.title("📄 LinkedIn HR Profile Extractor")
st.markdown("""
Upload LinkedIn profile URLs to extract simulated HR-related data such as job titles and certifications.
This is a demo and does not scrape real LinkedIn content.
""")

scraper = LinkedInScraper()
st.sidebar.title("Settings")
filter_hr = st.sidebar.checkbox("Only show HR-related profiles", False)
filter_cert = st.sidebar.checkbox("Only show certified profiles", False)

uploaded_file = st.file_uploader("Upload CSV/Excel with LinkedIn URLs", type=['csv', 'xlsx'])
manual_input = st.text_area("Or paste LinkedIn URLs (one per line):")

urls = []
df = None
if uploaded_file:
    try:
        if uploaded_file.name.endswith("csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        url_col = st.selectbox("Select the column with LinkedIn URLs", df.columns)
        urls = df[url_col].dropna().tolist()
        st.success(f"Loaded {len(urls)} URLs from file.")
    except Exception as e:
        st.error(f"Failed to process file: {e}")
elif manual_input:
    urls = [line.strip() for line in manual_input.strip().split('\n') if line.strip()]
    st.success(f"Loaded {len(urls)} URLs from manual input.")

if st.button("🚀 Extract Profiles") and urls:
    st.info("Processing profiles... Please wait.")
    bar = st.progress(0)
    status = st.empty()

    def update_progress(current, total):
        bar.progress(current / total)
        status.text(f"Processing {current} of {total}")

    data = scraper.process_urls(urls, update_progress)
    df_result = pd.DataFrame(data)

    if filter_hr:
        df_result = df_result[df_result['is_hr_related']]
    if filter_cert:
        df_result = df_result[df_result['certification'] != '']

    st.success(f"Processed {len(df_result)} entries.")
    st.dataframe(df_result, use_container_width=True)

    csv = df_result.to_csv(index=False)
    st.download_button("📥 Download CSV", csv, "linkedin_results.csv", "text/csv")
