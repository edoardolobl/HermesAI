# HermesAI: Your Personalized Language Learning Companion 🌍📚

<p align="center">
  <img src="assets/hermesAI_thumb.png" alt="HermesAI Logo" title="HermesAI" width="60%" height="60%">
</p>

HermesAI is an AI-powered chatbot designed to make learning a new language an engaging and personalized experience. Like the mythological messenger Hermes, our AI swiftly guides you on your language acquisition journey!  

## Features:

* **CEFR Level Assessment**: Determine your proficiency level with interactive questions powered by Google's Gemini Pro.
* **Personality Test**: Discover your unique learner profile to receive tailored recommendations.
* **Personalized Learning Path**: Obtain a customized study plan with resources, strategies, and activities aligned with your level and personality.
* **Exercise Examples**: Practice your skills with targeted exercises designed to help you progress.

## Getting Started:

1. **Clone the repository:**
   
   ```bash
   git clone https://github.com/your-username/hermesai.git
   ```

3. **Set up your Google API Key:**
- Obtain your API key from the [Google AI Studio](https://aistudio.google.com/app).
- Set the `GOOGLE_API_KEY` environment variable:
  
  ```bash
  export GOOGLE_API_KEY='your_api_key_here'
  ```

3. **Install the Python SDK:**  
- The Python SDK for the Gemini API, is contained in the **`google-generativeai package`**. Install the dependency using pip:
    
  ```bash
  pip install -q -U google-generativeai
  ```

4. **Run the Chatbot 🤖:**
   
   ```bash
   python chatbot.py
   ```

## Usage:

- Once you run the chatbot, you'll be greeted with a friendly menu guiding you through the following steps:
- Register your name: Personalize your experience by providing your name.
- Take the CEFR assessment: Determine your proficiency level in your chosen language (English, Italian, French, German, Spanish).
- Discover your learner profile: Answer a series of questions to reveal your learning preferences.
- Receive your personalized learning plan: Access a customized plan that takes into account your level and learner profile.
- Explore exercises: Put your knowledge into practice with exercises tailored to your needs.

## Contributing:

- Contributions from the community are welcomed!
- Bug reports: Report any issues you encounter on the issues page.
- Feature requests: Suggest new features or improvements.
- Pull requests: Contribute code to enhance the project.
