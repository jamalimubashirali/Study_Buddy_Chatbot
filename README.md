# Study Buddy Chatbot

A conversational AI chatbot designed to assist with studying various subjects like Mathematics, Physics, Chemistry, Biology, Computer Science, and History. Built with Streamlit, LangChain, and HuggingFace models.

## Features

- Subject-specific tutoring: Choose from a list of subjects to get tailored assistance.
- Conversational memory: Remembers previous interactions within a session.
- Streaming responses: Simulates typing for a more interactive experience.
- Strict topic adherence: Only answers questions related to the selected subject.

## Installation

1. Clone or download the repository.
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Set up environment variables:
   - Create a `.env` file in the project root.
   - Add your HuggingFace API token:
     ```
     HUGGINGFACEHUB_API_TOKEN=your_token_here
     ```

## Usage

Run the Streamlit app:
```
streamlit run app.py
```

Open the provided URL in your browser. Select a subject and start chatting!

## Requirements

- Python 3.8+
- HuggingFace account with API token
- Internet connection for model inference

## Contributing

Feel free to submit issues or pull requests for improvements.

## License

This project is open-source. Use at your own risk.
