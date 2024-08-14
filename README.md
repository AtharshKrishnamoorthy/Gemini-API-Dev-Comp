
# DOCU GENIE: AI-Powered Document Summarizer

DOCU GENIE is an advanced AI-powered document summarization tool that leverages the power of Google's Gemini model to provide intelligent summaries of PDF documents and handwritten or typed notes. With additional features like text-to-speech and interactive chat, DOCU GENIE aims to revolutionize the way users interact with and digest information from various document types.

## Demo Video

[![DOCU GENIE Demo](https://img.youtube.com/vi/iM93tBZqsIE/0.jpg)](https://youtu.be/iM93tBZqsIE?si=d_LXpALT_Ux2vWMu)

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [API Keys](#api-keys)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

DOCU GENIE offers a range of powerful features to enhance your document summarization experience:

1. **PDF Summarization**: Upload PDF documents and receive concise, intelligent summaries.
2. **Notes Image Summarization**: Analyze and summarize handwritten or typed notes from uploaded images.
3. **Interactive Chat**: Engage in a conversation about the summarized content for further clarification or insights.
4. **Text-to-Speech**: Listen to summaries with the built-in text-to-speech functionality.
5. **Enhanced PDF Generation**: Download beautifully formatted PDF summaries with proper styling and formatting.
6. **User Feedback Loop**: Provide feedback on summaries and request modifications for improved results.
7. **Gemini AI Integration**: Utilizes Google's advanced Gemini model for high-quality summarization and natural language understanding.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7+
- Streamlit
- PyPDF2
- Reportlab
- Pillow (PIL)
- Google Generative AI Python SDK
- Deepgram API (for text-to-speech functionality)

## Installation

1. Clone the repository:

`git clone https://github.com/AtharshKrishnamoorthy/Gemini-API-Dev-Comp
cd docu-genie`

2. Install the required packages:

`pip install -r requirements_gemini.txt`

3. Set up your environment variables (see [Configuration](#configuration) section).

## Usage

To run DOCU GENIE:

1. Navigate to the project directory.
2. Run the Streamlit app:

`streanmlit run main.py`

3. Open your web browser and go to `http://localhost:8501` (or the address provided in the terminal).


### PDF Summarizer

1. Select "PDF Summarizer" from the sidebar.
2. Upload a PDF file using the file uploader.
3. Click the "Summarize" button to generate a summary.
4. Optionally, use the "Read Summary Aloud" feature to listen to the summary.
5. Provide feedback on the summary quality and request modifications if needed.
6. Download the final summary as an enhanced PDF.

### Note Summarizer

1. Select "Note Summarizer" from the sidebar.
2. Upload an image of handwritten or typed notes.
3. Click the "Summarize Notes" button to analyze and summarize the content.
4. View the summary and optionally download it as a PDF or listen to it.

### Chat Functionality

- After generating a summary, use the chat input at the bottom of the page to ask questions or request further information about the summarized content.

## Configuration

Create a `.env` file in the project root directory with the following contents:

`GEMINI_API_KEY=your_gemini_api_key_here
DEEPGRAM_API_KEY=your_deepgram_api_key_here`


Replace `your_gemini_api_key_here` and `your_deepgram_api_key_here` with your actual API keys.

## API Keys

To use DOCU GENIE, you'll need to obtain the following API keys:

1. **Google Gemini API Key**: Sign up for Google AI Studio and obtain an API key for the Gemini model.
2. **Deepgram API Key**: Create an account on Deepgram and get an API key for text-to-speech functionality.

## Contributing

Contributions to DOCU GENIE are welcome! Here's how you can contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch-name`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the original branch: `git push origin feature-branch-name`.
5. Create a pull request.

Please make sure to update tests as appropriate and adhere to the project's coding standards.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Contact

If you have any questions, feel free to reach out:

- Project Maintainer: Atharsh K
- Email: atharshkrishnamoorthy@gmail.com
- Project Link: https://github.com/AtharshKrishnamoorthy/Gemini-API-Dev-Comp

---

DOCU GENIE - Empowering intelligent document summarization with AI.
