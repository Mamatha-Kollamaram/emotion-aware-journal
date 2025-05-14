#  Emotion-Aware Journal

Emotion-Aware Journal is a personalized journaling web app that uses Natural Language Processing (NLP) to detect emotions from user-written journal entries. The app helps users reflect on their emotions over time and supports emotional awareness and mental well-being.

##  Features

- **User Authentication** via Firebase.
- **Personalized Journal Entries** stored in Firebase Realtime Database.
- **Emotion Detection** using a fine-tuned BERT-base-uncased model from Hugging Face Transformers, trained on the **GoEmotions** dataset (Kaggle). It currently identifies **28 different emotions**.
- **Mood Graph Visualization** that displays trends in the user's emotions over the **past 7 days**. Users can visualize how their top _n_ emotions have fluctuated over time, providing deeper insights into their emotional journey.
- **View Past Entries** along with detected emotions and dates.
- **Delete Entries** with a single click.
- Built with a focus on **scalability** and future enhancement of the emotion detection model.

##  Emotion Detection

The emotion classification model is based on a fine-tuned **BERT-base-uncased** model from Hugging Face’s Transformers library. It was fine-tuned using the **GoEmotions dataset** ([available on Kaggle](https://www.kaggle.com/datasets/google/goemotions)) to detect **28 distinct emotions**, including:

`admiration`, `amusement`, `anger`, `annoyance`, `approval`, `caring`, `confusion`, `curiosity`, `desire`, `disappointment`, `disapproval`, `disgust`, `embarrassment`, `excitement`, `fear`, `gratitude`, `grief`, `joy`, `love`, `nervousness`, `optimism`, `pride`, `realization`, `relief`, `remorse`, `sadness`, `surprise`, and `neutral`.

The current model can still be improved for real-world robustness, and future updates will aim to enhance accuracy and performance.

##  Model Hosting

This model is available on the Hugging Face Model Hub and can be accessed directly at:  
 [Mamatha-k/emotrack-model](https://huggingface.co/Mamatha-k/emotrack-model)

The app loads this model at runtime using the `transformers` library.

##  Live Demo

🔗 [Click here to open the app](https://emotion-aware-journal-hync9gisopfqjna6yjnpig.streamlit.app/)

##  Screenshots

```markdown
![Homepage](screenshots/homepage.png)
![Journal Entry](screenshots/journal_entry.png)
![View Entries](screenshots/view_entries.png)
![Mood Graph](screenshots/mood_graph.png)
```

##  Technologies Used

- [Streamlit](https://streamlit.io/) – Frontend UI
- [Firebase Authentication](https://firebase.google.com/products/auth) – User login and registration
- [Firebase Realtime Database](https://firebase.google.com/products/realtime-database) – Entry storage
- [Hugging Face Transformers](https://huggingface.co/transformers/) – BERT model for emotion classification
- [GoEmotions Dataset](https://www.kaggle.com/datasets) – Dataset used for training emotion classifier

##  Prerequisites

Make sure you have the following installed:

- Python 3.8+
- `pip`
- Firebase Admin SDK credentials (as `firebase_service_key.json` or stored in Streamlit secrets)

Install dependencies:

```bash
pip install -r requirements.txt
```

##  Project Structure

```
emotion-aware-journal/
├── app.py
├── firebase_setup.py
├── pages/
│ ├── journal.py
│ └── login.py
├── model/
│ └── emotion_classifier.py
├── firebase_service_key.json # or set in secrets
├── requirements.txt
├── screenshots/
│ ├── homepage.png
│ ├── journal_page.png
│ ├── view_entries.png
│ └── mood_graph.png
└── README.md
```

##  Security Considerations

- Keep your Firebase credentials secure. If deploying on Streamlit Cloud, store them in `st.secrets`.
- Authentication is handled via Firebase, ensuring secure sign-ins.

##  License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

##  Contact

For questions or feedback, feel free to open an issue or contact the maintainer:

**Mamatha Kollamaram**  
[GitHub Profile](https://github.com/Mamatha-Kollamaram)
