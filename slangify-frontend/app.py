import streamlit as st
import requests
import os
st.set_page_config(page_title="Slangify: Translate Like a Gen Z Pro", page_icon="🎮", layout="centered")

# Custom CSS for Authentic Y2K Arcade Interface
st.markdown("""
<style>
/* Import pixelated arcade font */
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

/* Global styles */
body {
    background: #000000;
    color: #FFD700;  /* Gold text */
    font-family: 'Press Start 2P', cursive;
    font-size: 12px;
    line-height: 1.5;
    overflow-x: hidden;
    image-rendering: pixelated;
}

/* Arcade cabinet style container */
.game-cabinet {
    background: #1a1a1a;
    border: 12px solid #8B0000;  /* Dark red */
    border-radius: 8px;
    padding: 15px;
    margin: 0 auto;
    max-width: 600px;
    position: relative;
    box-shadow: 
        0 0 0 4px #FF0000,  /* Red inner border */
        0 0 20px rgba(255, 0, 0, 0.7),  /* Red glow */
        inset 0 0 10px rgba(0, 0, 0, 0.8);
}

/* CRT scanlines effect */
.crt::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(
        rgba(0, 0, 0, 0) 50%, 
        rgba(0, 0, 0, 0.25) 50%
    );
    background-size: 100% 4px;
    pointer-events: none;
    z-index: 100;
}

/* Title style with pixelated text-shadow */
h1 {
    color: #FF0000;  /* Red */
    text-shadow: 
        3px 3px 0 #FFD700,  /* Gold shadow */
        6px 6px 0 #0000FF;   /* Blue shadow */
    font-size: 24px;
    text-align: center;
    margin-bottom: 20px;
    letter-spacing: 2px;
}

/* Subheaders */
h2 {
    color: #00FF00;  /* Neon green */
    font-size: 16px;
    margin: 15px 0 10px 0;
    text-shadow: 2px 2px 0 #000000;
    border-bottom: 2px dotted #FFD700;
    padding-bottom: 5px;
}

/* Input fields */
.stTextInput>div>input, .stTextArea textarea {
    background-color: #000000;
    color: #00FF00;
    border: 3px solid #FFD700;
    border-radius: 0;
    padding: 8px;
    font-family: 'Press Start 2P', cursive;
    font-size: 10px;
    image-rendering: pixelated;
}
.stTextInput>div>input:focus, .stTextArea textarea:focus {
    outline: none;
    border-color: #FF0000;
    box-shadow: 0 0 5px #FF0000;
}

/* Buttons - Arcade style */
.stButton>button {
    background: #FF0000;
    color: #FFD700;
    border: 3px solid #FFD700;
    border-radius: 0;
    padding: 8px 15px;
    font-family: 'Press Start 2P', cursive;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1px;
    box-shadow: 3px 3px 0 #000000;
    transition: all 0.1s;
}
.stButton>button:hover {
    background: #8B0000;
    color: #FFFFFF;
    box-shadow: 1px 1px 0 #000000;
    transform: translate(2px, 2px);
}

/* Selectbox */
.stSelectbox>div>div {
    background-color: #000000;
    color: #00FF00;
    border: 3px solid #FFD700;
    border-radius: 0;
    font-family: 'Press Start 2P', cursive;
    font-size: 10px;
    padding: 5px;
}

/* Slang cards - like arcade high score displays */
.slang-card {
    background-color: #000000;
    border: 3px solid #00FF00;
    border-radius: 0;
    padding: 10px;
    margin: 10px 0;
    color: #FFD700;
    font-size: 10px;
    box-shadow: 3px 3px 0 #0000FF;
    position: relative;
    overflow: hidden;
}
.slang-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(to right, #FF0000, #00FF00, #0000FF, #FF0000);
}

/* Expander - like arcade cabinet controls */
.stExpander {
    border: 2px solid #FFD700;
    border-radius: 0;
    background: #000000;
}
.stExpander summary {
    color: #FF0000;
    font-family: 'Press Start 2P', cursive;
    font-size: 12px;
}

/* Alerts - like arcade error messages */
.stAlert {
    background-color: #000000;
    color: #FF0000;
    border: 2px solid #FFD700;
    border-radius: 0;
    font-family: 'Press Start 2P', cursive;
    font-size: 10px;
    text-shadow: 1px 1px 0 #000000;
}

/* Columns spacing */
.stColumn {
    padding: 5px;
}

/* Pixelated divider */
.pixel-divider {
    height: 4px;
    background: repeating-linear-gradient(
        to right,
        #FF0000,
        #FF0000 4px,
        #FFD700 4px,
        #FFD700 8px
    );
    margin: 15px 0;
    border: none;
}

/* Blinking text for important elements */
.blink {
    animation: blink 1s step-end infinite;
}
@keyframes blink {
    50% { opacity: 0; }
}

/* Scoreboard-like elements */
.scoreboard {
    background: #000000;
    border: 3px solid #00FF00;
    padding: 10px;
    margin: 10px 0;
    color: #FFD700;
    text-align: center;
}
.scoreboard-title {
    color: #FF0000;
    margin-bottom: 5px;
}

/* Pixelated loading animation */
.loading-pixel {
    display: inline-block;
    width: 8px;
    height: 8px;
    background-color: #00FF00;
    margin: 0 2px;
    animation: loading 1.4s infinite ease-in-out;
}
.loading-pixel:nth-child(1) { animation-delay: 0s; }
.loading-pixel:nth-child(2) { animation-delay: 0.2s; }
.loading-pixel:nth-child(3) { animation-delay: 0.4s; }
@keyframes loading {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(0.5); opacity: 0.5; }
}
</style>
""", unsafe_allow_html=True)

# API endpoint
BACKEND_URL = "https://slangify.onrender.com"  # Your live backend URL
API_URL = f"{BACKEND_URL}/api/"

def fetch_slang_of_the_day():
    try:
        response = requests.get(f"{API_URL}slangs/slang_of_the_day/", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"ERROR {response.status_code}: FAILED TO FETCH SLANG OF THE DAY")
            return {}
    except requests.exceptions.ConnectionError as e:
        st.error(f"CONNECTION ERROR: CANNOT CONNECT TO BACKEND API")
        return {}
    except requests.exceptions.Timeout:
        st.error(f"TIMEOUT: SERVER NOT RESPONDING")
        return {}
    except requests.exceptions.RequestException as e:
        st.error(f"API ERROR: {str(e)}")
        return {}

def fetch_categories():
    try:
        response = requests.get(f"{API_URL}categories/", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"ERROR {response.status_code}: FAILED TO FETCH CATEGORIES")
            return []
    except requests.exceptions.ConnectionError as e:
        st.error(f"CONNECTION ERROR: CANNOT CONNECT TO BACKEND API")
        return {}
    except requests.exceptions.Timeout:
        st.error(f"TIMEOUT: SERVER NOT RESPONDING")
        return {}
    except requests.exceptions.RequestException as e:
        st.error(f"API ERROR: {str(e)}")
        return {}

def translate_slang(slang_term):
    slang_term = slang_term.strip().lower()
    if not slang_term:
        return {}

    try:
        response = requests.get(f"{API_URL}slangs/{slang_term}/", timeout=5)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            st.warning(f"TERM '{slang_term.upper()}' NOT FOUND IN DATABASE")
            return {}
        else:
            st.error(f"ERROR {response.status_code}: TRANSLATION FAILED")
            return {}
    except requests.exceptions.ConnectionError as e:
        st.error(f"CONNECTION ERROR: CANNOT CONNECT TO BACKEND API")
        return {}
    except requests.exceptions.Timeout:
        st.error(f"TIMEOUT: SERVER NOT RESPONDING")
        return {}
    except requests.exceptions.RequestException as e:
        st.error(f"API ERROR: {str(e)}")
        return {}

def add_slang(term, meaning, category_id, origin):
    data = {
        "term": term.strip().lower(),
        "meaning": meaning.strip(),
        "category_id": category_id,
        "origin": origin.strip() if origin else "",
        "popularity": 5  # Default popularity
    }
    try:
        response = requests.post(f"{API_URL}slangs/", json=data, timeout=5)
        if response.status_code == 201:
            return response.json()
        elif response.status_code == 409:
            st.error(f"TERM '{term.upper()}' ALREADY EXISTS")
            return {}
        elif response.status_code == 400:
            st.error(f"INVALID DATA: {response.text}")
            return {}
        else:
            st.error(f"ERROR {response.status_code}: ADD SLANG FAILED")
            return {}
    except requests.exceptions.ConnectionError as e:
        st.error(f"CONNECTION ERROR: CANNOT CONNECT TO BACKEND API")
        return {}
    except requests.exceptions.Timeout:
        st.error(f"TIMEOUT: SERVER NOT RESPONDING")
        return {}
    except requests.exceptions.RequestException as e:
        st.error(f"API ERROR: {str(e)}")
        return {}

# Main App - Arcade Cabinet Interface
st.markdown('<div class="game-cabinet crt">', unsafe_allow_html=True)

# Title with arcade style
st.markdown("""
<h1>SLANGIFY<span class="blink">_</span></h1>
<p style="text-align: center; color: #FFD700; font-size: 10px;">TRANSLATE GEN-Z SLANG • HIGH SCORE: 25000</p>
<div class="pixel-divider"></div>
""", unsafe_allow_html=True)

# Slang of the Day - Like a high score display
st.markdown("""
<div class="scoreboard">
    <div class="scoreboard-title">SLANG OF THE DAY</div>
</div>
""", unsafe_allow_html=True)

slang_day = fetch_slang_of_the_day()
if slang_day:
    st.markdown(f"""
    <div class="slang-card">
        <div style="color: #FF0000; margin-bottom: 5px;">{slang_day.get('term', 'N/A').upper()}</div>
        <div><span style="color: #00FF00;">MEANING:</span> {slang_day.get('meaning', 'N/A')}</div>
        <div><span style="color: #00FF00;">CATEGORY:</span> {slang_day.get('category', {}).get('name', 'N/A').upper()}</div>
        <div><span style="color: #00FF00;">ORIGIN:</span> {slang_day.get('origin', 'N/A')}</div>
    </div>
    """, unsafe_allow_html=True)

# Translation Section - Like an arcade game input
st.markdown("""
<div class="pixel-divider"></div>
<h2>TRANSLATE SLANG</h2>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    user_input = st.text_input("ENTER SLANG TERM:", placeholder="E.G. 'YEET'", key="slang_input")
with col2:
    st.markdown("<div style='height: 27px; display: flex; align-items: flex-end;'>", unsafe_allow_html=True)
    translate_button = st.button("TRANSLATE")
    st.markdown("</div>", unsafe_allow_html=True)

if translate_button:
    if user_input:
        with st.spinner("".join([f'<span class="loading-pixel"></span>' for _ in range(3)])):
            slang_data = translate_slang(user_input)
        if slang_data:
            st.markdown(f"""
            <div class="slang-card">
                <div style="color: #FF0000; margin-bottom: 5px;">{slang_data.get('term', 'N/A').upper()}</div>
                <div><span style="color: #00FF00;">MEANING:</span> {slang_data.get('meaning', 'N/A')}</div>
                <div><span style="color: #00FF00;">CATEGORY:</span> {slang_data.get('category', {}).get('name', 'N/A').upper()}</div>
                <div><span style="color: #00FF00;">ORIGIN:</span> {slang_data.get('origin', 'N/A')}</div>
                <div><span style="color: #00FF00;">EXAMPLE:</span> {slang_data.get('usage_example', 'N/A')}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="stAlert">NO TRANSLATION FOUND</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="stAlert">PLEASE ENTER A TERM</div>', unsafe_allow_html=True)

# Add New Slang - Like a high score entry
with st.expander("++ ADD NEW SLANG ++"):
    categories = fetch_categories()
    category_options = {cat["name"]: cat["id"] for cat in categories}
    new_term = st.text_input("SLANG TERM:", key="new_term")
    new_meaning = st.text_area("MEANING:", key="new_meaning")
    new_category = st.selectbox("CATEGORY:", options=list(category_options.keys()), key="new_category")
    new_origin = st.text_input("ORIGIN (OPTIONAL):", key="new_origin")
    if st.button("SUBMIT SLANG"):
        if new_term and new_meaning and new_category:
            category_id = category_options[new_category]
            result = add_slang(new_term, new_meaning, category_id, new_origin)
            if result:
                st.markdown('<div class="stAlert" style="color: #00FF00;">SLANG ADDED SUCCESSFULLY!</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="stAlert">FAILED TO ADD SLANG</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="stAlert">FILL ALL REQUIRED FIELDS</div>', unsafe_allow_html=True)

# Browse Categories - Like an arcade game menu
st.markdown("""
<div class="pixel-divider"></div>
<h2>BROWSE CATEGORIES</h2>
""", unsafe_allow_html=True)

categories = fetch_categories()
for cat in categories:
    with st.expander(f">> {cat['name'].upper()} <<"):
        try:
            response = requests.get(f"{API_URL}slangs/", params={"category": cat['id']}, timeout=5)
            if response.status_code == 200:
                slangs = response.json()
                if slangs:
                    for slang in slangs:
                        st.markdown(f"""
                        <div class="slang-card" style="margin-bottom: 10px;">
                            <div style="color: #FF0000;">{slang.get('term', 'N/A').upper()}</div>
                            <div>{slang.get('meaning', 'N/A')}</div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown('<div class="stAlert">NO SLANGS IN THIS CATEGORY</div>', unsafe_allow_html=True)
            else:
                st.error(f"ERROR {response.status_code}: FAILED TO LOAD CATEGORY")
        except requests.exceptions.ConnectionError as e:
            st.error(f"CONNECTION ERROR: CANNOT CONNECT TO BACKEND API")
        except requests.exceptions.Timeout:
            st.error(f"TIMEOUT: SERVER NOT RESPONDING")
        except requests.exceptions.RequestException as e:
            st.error(f"API ERROR: {str(e)}")

# Arcade cabinet footer
st.markdown("""
<div class="pixel-divider"></div>
<div style="text-align: center; color: #FFD700; font-size: 8px; margin-top: 20px;">
    CREDIT 00 • © 2023 SLANGIFY ARCADE • 1UP 25000 • HIGH SCORE 25000 • 2UP 00322
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close game-cabinet div
