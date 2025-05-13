# Emotion-Aware Journal

## Description

The **Emotion-Aware Journal** is a web application built using **Streamlit** and **Hugging Face's Transformers**. It allows users to track their emotions over time by predicting their mood based on text input. The system uses a pre-trained emotion detection model to classify the user's emotional state (e.g., happy, sad, neutral, angry) from the text they provide.

## Features

- **Mood Prediction:** Users can enter text describing how they feel, and the model predicts their mood based on the input.
- **Emotion Detection:** The application uses a fine-tuned emotion detection model to predict the user's emotional state (e.g., happy, sad, neutral, angry).
- **Cloud Hosting:** The app is hosted on Streamlit Cloud, allowing easy access for anyone to use it.

## Technologies Used

- **Streamlit:** For creating the interactive web interface.
- **Hugging Face Transformers:** For loading and using pre-trained models for emotion detection.
- **PyTorch:** For model inference and prediction.
- **GitHub:** For version control and project hosting.
- **Streamlit Cloud:** For hosting the application online.

## Setup

To run the app locally, follow these steps:

### Prerequisites

- Python 3.x
- `pip` package manager

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Mamatha-Kollamaram/emotion-aware-journal.git
   cd emotion-aware-journal
   ```
2. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
   
## Model

The app uses the EmoTrack model, hosted on Hugging Face, for emotion classification. The model is loaded dynamically to predict the mood based on user input.

## Contributing

Contributions are welcome! If you would like to improve the app, feel free to fork the repository and submit a pull request. If you find any bugs or issues, please open an issue on GitHub.

## License

This project is licensed under the MIT License.

## Acknowledgments

***Thanks to Hugging Face for providing the pre-trained models.***
***Thanks to Streamlit for the simple, easy-to-use interface that makes building web apps fun!***
   

This README includes the following sections:
1. **Project description** to explain the purpose.
2. **Features** to describe the capabilities of the app.
3. **Technologies used** to mention the stack.
4. **Setup instructions** for running the app locally.
5. **Model** section to explain how the model is used in the app.
6. **Contributing** to encourage open-source contributions.
7. **License** to clarify usage rights.

You can adapt it to your needs and add any additional information or sections relevant to your project.
