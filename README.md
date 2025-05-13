# Emotion-Aware Journal 🌈🧠

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-streamlit-app-url.streamlit.app/)
![GitHub License](https://img.shields.io/github/license/Mamatha-Kollamaram/emotion-aware-journal)

The **Emotion-Aware Journal** is an intelligent web application that helps users track their emotional patterns over time. Powered by **NLP** and a fine-tuned **BERT** model, this app analyzes written journal entries and predicts the user’s mood using advanced emotion detection techniques.

![App Screenshot](https://via.placeholder.com/800x400?text=Emotion-Aware+Journal+Screenshot) <!-- Replace with actual screenshot -->

---

## 🧩 Features

- 🎯 **Advanced Mood Prediction**: Detects up to **28 distinct emotions** from journal entries
- 🔐 **Secure Cloud Storage**: Firebase for user authentication and storing journal entries
- 📊 **Interactive Visualizations**: Trend tracking and analytics for emotional patterns
- 🌍 **Accessible Anywhere**: Responsive design using Streamlit Cloud
- ⚡ **Real-Time Processing**: Get instant emotion predictions from your text

---

## 🛠️ Tech Stack

| Component        | Technology |
|------------------|------------|
| Frontend         | Streamlit |
| NLP Model        | Fine-tuned BERT (via Hugging Face Transformers) |
| Backend & Auth   | Firebase (Firestore + Authentication) |
| ML Framework     | PyTorch |
| Hosting          | Streamlit Cloud |

---

## 🚀 Getting Started

### 📌 Prerequisites
- Python 3.8+
- Firebase Project & credentials
- Streamlit Account

### 💻 Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/Mamatha-Kollamaram/emotion-aware-journal.git
cd emotion-aware-journal

# 2. Create a virtual environment
python -m venv venv
# Activate:
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### 🔐 Firebase Setup

1. Rename `firebase-config-example.json` → `firebase-config.json`
2. Add your Firebase Admin SDK credentials.

### ▶️ Run the App

```bash
streamlit run app.py
```

---

## ☁️ Deploying to Streamlit Cloud

1. Push your code to GitHub
2. Create a new app at [Streamlit Cloud](https://streamlit.io/cloud)
3. Set environment variables for Firebase (via app settings)
4. Deploy and share!

---

## 🤖 Model Details

The app uses a **fine-tuned BERT-base-uncased** model trained to classify **28 emotions**, including:

- Joy 😊
- Anger 😠
- Sadness 😢
- Fear 😨
- Surprise 😲
- ... *(add complete list of 28 emotions here)*

### Current Capabilities
- Classifies emotion-rich content with high accuracy
- Supports real-time emotion recognition
- Learns from user text inputs to identify core emotions

### Future Improvements
- Multilingual emotion detection
- Deeper contextual understanding
- Emotion-based recommendations

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

```bash
# 1. Fork the repository
# 2. Create your feature branch
git checkout -b feature/YourFeature

# 3. Commit your changes
git commit -m "Add YourFeature"

# 4. Push to GitHub
git push origin feature/YourFeature

# 5. Open a Pull Request
```

Feel free to report issues or suggest features via the [Issues Tab](https://github.com/Mamatha-Kollamaram/emotion-aware-journal/issues).

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙌 Acknowledgments

- 🤗 [Hugging Face](https://huggingface.co/) for pre-trained NLP models
- 🧠 [PyTorch](https://pytorch.org/) for model building and inference
- 🎈 [Streamlit](https://streamlit.io/) for enabling fast web app development
- 🔥 [Firebase](https://firebase.google.com/) for backend and authentication services

> Developed with ❤️ by Mamatha Kollamaram

---