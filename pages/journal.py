import streamlit as st
import torch
from transformers import BertTokenizer, BertForSequenceClassification
from safetensors.torch import load_file
import datetime
import pandas as pd
from firebase_setup import db, save_journal_entry, get_user_journal_entries, delete_journal_entry
import altair as alt
import random
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Custom CSS styling
def inject_custom_css():
    st.markdown("""
    <style>
        /* Main container styling */
        .stApp {
            background-color: #f5f7fa;
            background-image: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        
        /* Title styling */
        .css-10trblm {
            color: #2c3e50;
            text-align: center;
            font-family: 'Arial', sans-serif;
            font-weight: 700;
            margin-bottom: 30px;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.1);
        }
        
        /* Tab styling - make sure headings are visible */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #2c3e50;
            padding: 8px;
            border-radius: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            color: white !important;
            padding: 8px 16px;
            margin: 0 4px;
            border-radius: 4px;
            transition: all 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #34495e !important;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #3498db !important;
            color: white !important;
        }
        
        /* Card-like containers */
        .stContainer {
            background-color: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        
        /* Custom divider */
        .divider {
            height: 1px;
            background: linear-gradient(to right, transparent, #bdc3c7, transparent);
            margin: 20px 0;
        }
        
        /* Button styling */
        .stButton>button {
            border-radius: 8px !important;
            border: none !important;
            background-color: #3498db !important;
            color: white !important;
            padding: 10px 24px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            width: 100% !important;
        }
        
        .stButton>button:hover {
            background-color: #2980b9 !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
        }
        
        /* Success message styling */
        .stAlert .st-bb {
            background-color: #2ecc71 !important;
            color: white !important;
            border-radius: 8px !important;
        }
        
        /* Error message styling */
        .stAlert .st-cm {
            background-color: #e74c3c !important;
            color: white !important;
            border-radius: 8px !important;
        }
        
        /* Text area styling */
        .stTextArea textarea {
            border-radius: 8px !important;
            border: 1px solid #dfe6e9 !important;
            padding: 10px !important;
        }
        
        /* Data editor styling */
        .stDataEditor {
            border-radius: 8px !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
        }
    </style>
    """, unsafe_allow_html=True)

# Inject CSS
inject_custom_css()

# ------------------ Emotion Suggestions Database ------------------
EMOTION_SUGGESTIONS = {
    # ... (keep your existing EMOTION_SUGGESTIONS dictionary exactly as is) ...
    'admiration': [
        "Write about what specifically you admire and why it inspires you.",
        "Consider how you might incorporate qualities you admire into your own life.",
        "Share your admiration with the person/thing you admire if possible."
    ],
    'amusement': [
        "Write down what made you laugh - humor is great to revisit later!",
        "Consider sharing this amusing moment with someone who might appreciate it.",
        "Reflect on how humor helps you cope with life's challenges."
    ],
    'anger': [
        "Try deep breathing: inhale for 4 seconds, hold for 4, exhale for 6.",
        "Write a letter expressing your anger (but don't send it).",
        "Go for a brisk walk to physically release the angry energy."
    ],
    'annoyance': [
        "List three things more important than this annoyance.",
        "Practice reframing: 'This is temporary and not worth my energy.'",
        "Do a quick physical reset (stretch, drink water, step outside)."
    ],
    'approval': [
        "Acknowledge what behaviors/values you're approving of and why they matter.",
        "Consider giving direct positive feedback to whoever earned your approval.",
        "Reflect on how your standards guide your relationships."
    ],
    'caring': [
        "Plan one small act of kindness you can do today.",
        "Write about who you care for and why they're important to you.",
        "Practice self-care - you can't pour from an empty cup."
    ],
    'confusion': [
        "Break the problem down into smaller questions to tackle one at a time.",
        "List what you DO know vs what's unclear.",
        "Give yourself permission to not have all answers right now."
    ],
    'curiosity': [
        "Jot down three questions you'd like to explore about this topic.",
        "Schedule 15 minutes to research one aspect that intrigues you.",
        "Find someone knowledgeable to ask about your area of curiosity."
    ],
    'desire': [
        "Visualize what fulfilling this desire would look/feel like.",
        "Identify one small step you could take toward this desire today.",
        "Examine if this desire aligns with your core values."
    ],
    'disappointment': [
        "Acknowledge what you hoped for vs what actually happened.",
        "List three alternative paths forward from here.",
        "Practice self-compassion - not all outcomes are in your control."
    ],
    'disapproval': [
        "Clarify what specific behavior/outcome you disapprove of and why.",
        "Consider if this warrants addressing directly or letting go.",
        "Reflect on how your values inform this disapproval."
    ],
    'disgust': [
        "Distance yourself physically/mentally from the source if possible.",
        "Focus on cleansing rituals (washing hands, cleaning space).",
        "Examine if this disgust reveals any important boundaries for you."
    ],
    'embarrassment': [
        "Ask yourself: 'Will this matter in 5 years?'",
        "Practice self-forgiveness - everyone has awkward moments.",
        "Consider reframing as a funny story you might tell later."
    ],
    'excitement': [
        "Channel this energy into planning or starting a related project.",
        "Share your excitement with someone who will celebrate with you.",
        "Savor the anticipation - the buildup is often the best part!"
    ],
    'fear': [
        "Name your fear specifically to reduce its power over you.",
        "Practice grounding: 5 things you see, 4 you feel, 3 you hear, 2 you smell, 1 you taste.",
        "Make a contingency plan for the worst-case scenario (it's usually not as bad as you imagine)."
    ],
    'gratitude': [
        "Write down three specific things you're grateful for today.",
        "Express your gratitude directly to someone who contributed.",
        "Create a gratitude ritual (daily list, gratitude jar, etc.)."
    ],
    'grief': [
        "Create a small ritual to honor what/who you've lost.",
        "Write a letter to express what wasn't said.",
        "Be patient with yourself - grief has no timeline."
    ],
    'joy': [
        "Fully savor this moment - describe it in vivid detail.",
        "Share your joy with others to multiply it.",
        "Create a 'joy anchor' (photo, memento) to revisit later."
    ],
    'love': [
        "Express your feelings directly to the person(s) involved.",
        "Reflect on how this love has changed you for the better.",
        "Channel loving energy into a creative outlet (writing, art)."
    ],
    'nervousness': [
        "List what's actually within your control vs what's not.",
        "Practice progressive muscle relaxation (tense/release muscle groups).",
        "Prepare thoroughly, then distract yourself until the event."
    ],
    'optimism': [
        "Harness this energy to set goals or make plans.",
        "Share your positive outlook with someone who needs encouragement.",
        "Balance optimism with practical next steps."
    ],
    'pride': [
        "Acknowledge exactly what you did to earn this feeling.",
        "Share your accomplishment with supportive people.",
        "Let this pride fuel your next challenge."
    ],
    'realization': [
        "Journal about how this insight changes your perspective.",
        "Identify one action step this realization inspires.",
        "Consider who else might benefit from hearing this insight."
    ],
    'relief': [
        "Notice how your body feels different now vs before the relief.",
        "Express gratitude that the stressful situation has passed.",
        "Use this calm space to reflect on lessons learned."
    ],
    'remorse': [
        "Make amends if possible and appropriate.",
        "Identify what you'll do differently next time.",
        "Practice self-forgiveness - growth requires missteps."
    ],
    'sadness': [
        "Let yourself cry - tears release stress hormones.",
        "Reach out to someone who listens without judgment.",
        "Engage in gentle, comforting activities (warm drink, soft blanket)."
    ],
    'surprise': [
        "Pause to fully process what surprised you and why.",
        "Consider if this surprise reveals any assumptions you were making.",
        "Share the surprising story with someone who would appreciate it."
    ],
    'neutral': [
        "Check in with your body - are there subtle feelings beneath the neutrality?",
        "Use this calm state to reflect or plan.",
        "Practice mindfulness - neutral moments are perfect for being present."
    ]
}

def get_ai_suggestion(emotion):
    """Returns a random suggestion for the given emotion"""
    suggestions = EMOTION_SUGGESTIONS.get(emotion, [])
    if suggestions:
        return random.choice(suggestions)
    return "Consider reflecting on what this emotion means to you."

# ------------------ Load Emotion Detection Model ------------------
# @st.cache_resource(ttl=24*3600) 
# def load_model():
#     model_path = r"C:\\Users\\MAMATHA\\Desktop\\EmoTrack\\refined_emotion_model"
#     tokenizer = BertTokenizer.from_pretrained(model_path)
#     model = BertForSequenceClassification.from_pretrained(model_path, num_labels=28)
#     model_weights = load_file(f"{model_path}/model.safetensors")
#     model.load_state_dict(model_weights)
#     model.eval()
#     model = model.to('cpu')  # Force CPU usage
#     return tokenizer, model

# tokenizer, model = load_model()
@st.cache_resource
def load_model():
    model_name = "Mamatha-k/emotrack-model"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    model.eval()
    return tokenizer, model

tokenizer, model = load_model()


emotion_labels = [
    'admiration', 'amusement', 'anger', 'annoyance', 'approval', 'caring', 'confusion', 'curiosity', 'desire',
    'disappointment', 'disapproval', 'disgust', 'embarrassment', 'excitement', 'fear', 'gratitude', 'grief', 'joy',
    'love', 'nervousness', 'optimism', 'pride', 'realization', 'relief', 'remorse', 'sadness', 'surprise', 'neutral']

def predict_emotions(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    inputs = {k: v.to('cpu') for k, v in inputs.items()}  # Move inputs to CPU
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    probabilities = torch.sigmoid(logits).squeeze().numpy()
    threshold = 0.5
    detected = {emotion_labels[i]: round(probabilities[i], 2) for i in range(len(probabilities)) if probabilities[i] > threshold}
    return detected

# ------------------ UI ------------------
st.title("Emotion-Aware Journal Assistant ✍️")

user_id = st.session_state.get("user_id", None)
if not user_id:
    st.error("❌ Access Denied. Please log in first.")
    st.stop()

# Create tabs with custom styling
write_tab, view_tab, mood_tab = st.tabs([
    "📝 Write Journal", 
    "📜 View Entries", 
    "📊 Mood Graph"
])

# ------------------ Write Journal Tab ------------------
with write_tab:
    with st.container():
        journal_text = st.text_area("📝 Write your journal entry here:", height=200)
        
        if journal_text.strip():
            detected_emotions = predict_emotions(journal_text)
            if detected_emotions:
                emotions_str = ", ".join([f"{k} ({v:.2f})" for k, v in detected_emotions.items()])
                st.success(f"**Detected Emotions:** {emotions_str}")

                # Get top emotion for suggestion
                top_emotion = max(detected_emotions, key=detected_emotions.get)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✨ Get Supportive Suggestion", key="suggestion_btn"):
                        suggestion = get_ai_suggestion(top_emotion)
                        st.markdown(f"💡 **For {top_emotion}:** {suggestion}")
                
                with col2:
                    if st.button("💡 Another Suggestion", key="another_suggestion_btn"):
                        another_suggestion = get_ai_suggestion(top_emotion)
                        st.markdown(f"💡 **Alternative suggestion:** {another_suggestion}")
            else:
                st.warning("No strong emotions detected.")

        if st.button("✅ Save Entry", key="save_btn"):
            if journal_text.strip():
                timestamp = datetime.datetime.now()
                detected_emotions = predict_emotions(journal_text) if journal_text.strip() else {}
                save_journal_entry(user_id, journal_text, timestamp, detected_emotions)
                st.success("Journal entry saved!")
                st.rerun()

# ------------------ View Entries Tab ------------------
with view_tab:
    with st.container():
        st.subheader("📜 Previous Entries")
        entries = get_user_journal_entries(user_id)

        if not entries:
            st.info("You haven't written any journal entries yet.")
        else:
            df = pd.DataFrame(entries)
            df["Timestamp"] = pd.to_datetime(df["Timestamp"])
            df["Timestamp"] = df["Timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")

            df['Select'] = False
            edited_df = st.data_editor(
                df,
                column_config={
                    "Timestamp": st.column_config.DatetimeColumn(format="YYYY-MM-DD HH:mm:ss"),
                    "Select": st.column_config.CheckboxColumn("Delete?", required=True),
                    "ID": None
                },
                hide_index=True,
                disabled=["Entry", "Timestamp", "Emotions"],
                use_container_width=True
            )

            if st.button("🗑️ Delete Selected", key="delete_btn"):
                if st.toggle("❗ Confirm permanent deletion", key="confirm_toggle"):
                    to_delete = edited_df[edited_df['Select']]['ID'].tolist()
                    if to_delete:
                        with st.spinner("Deleting entries..."):
                            for entry_id in to_delete:
                                if delete_journal_entry(entry_id, user_id):
                                    st.toast(f"Deleted entry {entry_id[:8]}...", icon="✅")
                                else:
                                    st.error(f"Failed to delete {entry_id[:8]} (not owner?)")
                        st.rerun()
                    else:
                        st.warning("No entries selected!")

# ------------------ Mood Graph Tab ------------------
with mood_tab:
    with st.container():
        st.subheader("📈 Weekly Mood Trends")

        entries = get_user_journal_entries(user_id)
        if not entries:
            st.info("No entries to show.")
        else:
            df = pd.DataFrame(entries)
            df["Timestamp"] = pd.to_datetime(df["Timestamp"])
            recent_df = df[df["Timestamp"] >= pd.Timestamp.now() - pd.Timedelta(days=7)]

            emotion_data = []
            for _, row in recent_df.iterrows():
                emotions = row['Emotions']
                if isinstance(emotions, str):
                    try:
                        emotions = eval(emotions) if isinstance(emotions, str) else emotions
                    except:
                        continue
                if emotions:
                    for emotion, score in emotions.items():
                        emotion_data.append({
                            "Date": row["Timestamp"].date(),
                            "Emotion": emotion,
                            "Score": float(score)
                        })

            if emotion_data:
                mood_df = pd.DataFrame(emotion_data)
                top_emotions = mood_df['Emotion'].value_counts().nlargest(5).index.tolist()
                
                col1, col2 = st.columns(2)
                with col1:
                    top_n = st.slider("Show top N emotions:", 
                                    min_value=3, 
                                    max_value=len(mood_df['Emotion'].unique()), 
                                    value=5)
                    top_emotions = mood_df['Emotion'].value_counts().nlargest(top_n).index.tolist()
                with col2:
                    selected_emotions = st.multiselect(
                        "Or select specific emotions:",
                        options=mood_df['Emotion'].unique(),
                        default=top_emotions
                    )
                
                filtered_data = mood_df[mood_df['Emotion'].isin(selected_emotions)] if selected_emotions else mood_df[mood_df['Emotion'].isin(top_emotions)]
                
                if not filtered_data.empty:
                    chart = alt.Chart(filtered_data).mark_line(point=True).encode(
                        x='Date:T',
                        y='Score:Q',
                        color='Emotion:N',
                        tooltip=['Emotion', 'Score', 'Date']
                    ).properties(
                        width=700,
                        height=400,
                        title="Emotion Intensity Over Time"
                    ).interactive()
                    
                    st.altair_chart(chart, use_container_width=True)
                else:
                    st.warning("No data matches your filters.")
            else:
                st.warning("No mood data available to chart.")

# Logout button
if st.button("Logout", key="logout_btn"):
    del st.session_state["user_id"]
    del st.session_state["user_email"]
    st.success("✅ Logged out! Redirecting to login page...")
    st.switch_page("app.py")