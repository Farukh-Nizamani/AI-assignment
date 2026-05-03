import streamlit as st
import json
import requests
from pathlib import Path
import streamlit.components.v1 as components

st.set_page_config(page_title="Autism Screening", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for black animated background, butterfly cursor, and white text
st.markdown("""
<style>
/* Dark Greyish Background with Depth */
header[data-testid="stHeader"] {
    background-color: transparent !important;
}

.stApp, [data-testid="stAppViewContainer"] {
    background-color: #000000 !important;
    background-image: radial-gradient(circle at center, #1e293b 0%, #020617 60%, #000000 100%) !important;
    color: #f8fafc;
}

/* Main title styling */
h1 {
    color: #38bdf8 !important;
    text-align: center;
    font-family: 'Inter', sans-serif;
    font-weight: 800 !important;
    text-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5);
    margin-bottom: 20px;
}

/* Typography for descriptions */
.stMarkdown p {
    font-size: 1.1rem;
    color: #cbd5e1;
    text-align: center;
}

/* Question Cards */
div[data-testid="stRadio"] > div {
    background: rgba(30, 41, 59, 0.7);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    margin-bottom: 10px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

div[data-testid="stRadio"] > div:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.3);
}

/* Choices Text Color */
div[data-testid="stRadio"] label p, div[data-testid="stRadio"] label {
    color: #ffffff !important;
    font-size: 1.1rem;
    font-weight: 500;
}

/* Question Subheaders */
h3 {
    color: #f8fafc !important;
    font-weight: 600 !important;
    padding-bottom: 10px;
}

/* Styled Submit Button */
div.stButton {
    display: flex;
    justify-content: center;
    margin-top: 30px;
    margin-bottom: 30px;
}

div.stButton > button {
    background: linear-gradient(90deg, #0ea5e9, #3b82f6);
    color: white;
    border: none;
    border-radius: 50px;
    padding: 10px 40px;
    font-size: 1.2rem;
    font-weight: 700;
    box-shadow: 0 4px 15px rgba(14, 165, 233, 0.4);
    transition: all 0.3s ease;
}

div.stButton > button:hover {
    transform: translateY(-3px) scale(1.05);
    box-shadow: 0 8px 25px rgba(14, 165, 233, 0.6);
    background: linear-gradient(90deg, #3b82f6, #0ea5e9);
}

div.stButton > button:active {
    transform: translateY(1px);
}
</style>
""", unsafe_allow_html=True)

# Injecting JavaScript for an animated butterfly cursor that follows the mouse
components.html(
    """
    <script>
    const parentDoc = window.parent.document;
    if (!parentDoc.getElementById('animated-cross-cursor')) {
        const style = parentDoc.createElement('style');
        style.innerHTML = `
            * { cursor: none !important; }
            .cross-cursor {
                position: fixed;
                pointer-events: none;
                z-index: 9999999;
                font-size: 35px;
                font-family: sans-serif;
                font-weight: 900;
                color: #ef4444;
                text-shadow: 0 0 15px #ef4444, 0 0 30px #ef4444;
                animation: pulse 0.8s infinite alternate ease-in-out;
            }
            @keyframes pulse {
                0% { transform: translate(-50%, -50%) scale(1); filter: brightness(1) drop-shadow(0 0 5px #ef4444); }
                100% { transform: translate(-50%, -50%) scale(1.3); filter: brightness(1.5) drop-shadow(0 0 20px #ef4444); }
            }
            .random-line {
                position: fixed;
                background-color: rgba(255, 255, 255, 0.6);
                box-shadow: 0 0 10px rgba(255, 255, 255, 0.9);
                pointer-events: none;
                z-index: 0;
                animation: lineFadeOut 2s ease-in-out forwards;
            }
            @keyframes lineFadeOut {
                0% { opacity: 0; }
                20% { opacity: 1; }
                80% { opacity: 1; }
                100% { opacity: 0; }
            }
        `;
        parentDoc.head.appendChild(style);

        const customCursor = parentDoc.createElement('div');
        customCursor.id = 'animated-cross-cursor';
        customCursor.className = 'cross-cursor';
        customCursor.innerHTML = '✚';
        parentDoc.body.appendChild(customCursor);

        parentDoc.addEventListener('mousemove', function(e) {
            customCursor.style.left = e.clientX + 'px';
            customCursor.style.top = e.clientY + 'px';
        });

        // Function to create a randomly placed perpendicular shape (intersecting lines)
        function createRandomPerpendicular() {
            const size = Math.random() * 60 + 20; // 20px to 80px total length
            const thickness = (Math.random() * 1.5 + 1) + 'px'; // 1-2.5px thick
            const cx = Math.random() * 100; // 0-100vw
            const cy = Math.random() * 100; // 0-100vh
            
            // Random depth effect
            const depth = Math.random();
            const opacity = 0.3 + (depth * 0.5); // 0.3 to 0.8 opacity
            const blur = (1 - depth) * 2; // 0 to 2px blur
            
            // Random vibrant color
            const hue = Math.floor(Math.random() * 360);
            const colorStr = `hsla(${hue}, 100%, 65%, ${opacity})`;
            const glowStr = `hsla(${hue}, 100%, 65%, ${opacity + 0.4})`;
            
            const createLine = (isHoriz) => {
                const line = parentDoc.createElement('div');
                line.className = 'random-line';
                
                // Apply dynamic color, opacity, and glow
                line.style.backgroundColor = colorStr;
                line.style.boxShadow = `0 0 10px ${glowStr}, 0 0 20px ${glowStr}`;
                line.style.filter = `blur(${blur}px)`;
                
                if (isHoriz) {
                    line.style.height = thickness;
                    line.style.width = size + 'px';
                    line.style.left = `calc(${cx}vw - ${size/2}px)`;
                    line.style.top = cy + 'vh';
                } else {
                    line.style.width = thickness;
                    line.style.height = size + 'px';
                    line.style.left = cx + 'vw';
                    line.style.top = `calc(${cy}vh - ${size/2}px)`;
                }
                
                parentDoc.body.appendChild(line);
                
                // Remove the line element after its 2s animation completes
                setTimeout(() => {
                    if (line.parentNode) {
                        line.parentNode.removeChild(line);
                    }
                }, 2000);
            };

            createLine(true);
            createLine(false);
        }

        // Spawn a new perpendicular shape randomly every 400ms
        setInterval(createRandomPerpendicular, 400);
    }
    </script>
    """,
    height=0,
    width=0,
)

# Load questions from the JSON file located two levels up
questions_path = Path(__file__).parent.parent / "questions.json"
with open(questions_path) as f:
    questions = json.load(f)

st.markdown("<h1>Autism Screening Questionnaire</h1>", unsafe_allow_html=True)
st.markdown("<p>Select the option that best describes you for each question. When finished, click <b>Submit</b> to see the probability.</p>", unsafe_allow_html=True)

answers = []
for q in questions:
    st.subheader(f"{q['id']}. {q['text']}")
    choice = st.radio(
        "Choose an option",
        options=q['choices'],
        key=f"q{q['id']}"
    )
    # Map choice index (0-3) as the answer value
    answers.append(q['choices'].index(choice))

if st.button("Submit"):
    try:
        response = requests.post(
            "http://127.0.0.1:8000/predict",
            json={"answers": answers},
            timeout=5,
        )
        response.raise_for_status()
        data = response.json()
        prob = data["probability"]
        interpretation = data["interpretation"]
        st.success(f"Probability of autism: {prob*100:.1f}%")
        st.info(interpretation)
        st.progress(prob)
    except Exception as e:
        st.error(f"Failed to get prediction: {e}")
