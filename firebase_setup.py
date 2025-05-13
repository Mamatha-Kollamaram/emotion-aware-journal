import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from firebase_admin import firestore
import numpy as np


# Load Firebase credentials from JSON file
cred = credentials.Certificate("firebase_service_key.json")

# Initialize Firebase (only if it's not already initialized)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Get Firestore database reference
db = firestore.client()

def save_journal_entry(user_id, entry_text, timestamp=None, emotions=None):
    """Enhanced journal entry saver with all fields."""
    entry_data = {
        "user_id": user_id,
        "entry": entry_text,
        "timestamp": timestamp or datetime.utcnow(),
        "emotions": convert_emotions_to_python_types(emotions),
        "last_updated": datetime.utcnow()
    }
    return db.collection("journal_entries").add(entry_data)

# In firebase_setup.py
# In your get_user_journal_entries() function (firebase_setup.py):
def get_user_journal_entries(user_id):
    """Retrieve journal entries with robust timestamp handling"""
    from datetime import datetime
    entries = []
    
    try:
        docs = db.collection("journal_entries") \
                .where("user_id", "==", user_id) \
                .order_by("timestamp", direction=firestore.Query.DESCENDING) \
                .stream()
        
        for doc in docs:
            data = doc.to_dict()
            try:
                timestamp = data.get("timestamp", datetime.utcnow()).strftime("%Y-%m-%d %H:%M:%S")
                entries.append({
                    "Entry": data.get("entry", "[No text]"),
                    "Timestamp": timestamp,
                    "Emotions": data.get("emotions", {}),
                    "ID": doc.id  # Useful for updates/deletes
                })
            except Exception as e:
                print(f"Skipping corrupt entry {doc.id}: {e}")
                
    except Exception as e:
        print(f"Firestore query failed: {e}")
        raise  # Re-raise for Streamlit error handling
    
    return entries

def convert_emotions_to_python_types(emotions):
    """Convert numpy floats to native Python floats"""
    if emotions is None:
        return None
    return {k: float(v) if isinstance(v, (np.floating, np.float32, np.float64)) else v
            for k, v in emotions.items()}

def delete_journal_entry(entry_id, requesting_user_id=None):  # Make optional
    doc_ref = db.collection("journal_entries").document(entry_id)
    doc = doc_ref.get()
    
    # Skip verification if no user_id provided (for admin cases)
    if requesting_user_id is None:
        doc_ref.delete()
        return True
        
    # Normal user case - verify ownership
    if doc.exists and doc.to_dict().get("user_id") == requesting_user_id:
        doc_ref.delete()
        return True
    return False








