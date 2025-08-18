# Mindmate: An Advanced AI Mental Health Advisor

**Mindmate** is a state-of-the-art conversational AI designed to provide a safe, empathetic, and adaptive space for individuals to explore their thoughts and feelings. Leveraging a multi-layered AI architecture, this project demonstrates a sophisticated approach to building responsible and helpful mental wellness tools.

## Introduction

In an era where accessible mental health support is crucial, Mindmate serves as a proof-of-concept for an AI-powered companion. It is built on the principle of empathetic listening, providing users with a non-judgmental counterpart for self-reflection. The system is designed not to replace professional therapy, but to act as a supplementary tool that can help users identify patterns in their thoughts and learn about evidence-informed wellness concepts in a conversational context.

## Core Features

Mindmate integrates several advanced systems to create a responsive and insightful user experience:

* **Conversational AI Core:** At its heart is a powerful large language model (`gemma-3`) fine-tuned with a carefully crafted system prompt that prioritizes empathy, open-ended questions, and non-prescriptive guidance.
* **Retrieval-Augmented Generation (RAG):** The AI's responses are grounded in a curated knowledge base of therapeutic concepts from CBT, mindfulness, and positive psychology, ensuring the information provided is evidence-informed and relevant.
* **Dynamic User Dashboard:** Mindmate can analyze the user's session journal to generate a comprehensive dashboard. This includes:
    * **Sentiment Analysis:** An overall mood assessment of the conversation.
    * **Thematic Identification:** Key topics and themes that emerge over time.
    * **Actionable Recommendations:** Personalized, gentle suggestions with explanations on why they might be helpful.
* **Intelligent Flagging System:** A two-tiered safety mechanism is in place:
    1.  **Keyword Detection:** Immediately flags messages with high-risk crisis keywords.
    2.  **AI-Powered Severity Scoring:** A dedicated classification model analyzes the nuance of user input to assess its severity, providing a warning and resources when necessary.
* **Self-Improving System Prompt:** The application features a meta-analysis layer where a secondary AI model analyzes the conversation to provide a dynamic, one-time directive to the main chat model, helping it adapt its tone and approach based on the user's evolving needs.

## System Architecture

Mindmate employs a multi-model strategy to optimize performance and reliability:

1.  **Chat & Reasoning:** A powerful, large-scale model handles the core conversational tasks, providing nuanced and empathetic responses.
2.  **Dashboard & JSON Generation:** A model known for its reliability with structured data (`deepseek-r1`) is used exclusively for generating the dashboard insights, ensuring robust JSON output.
3.  **Classification & Analysis:** A smaller, faster model (`gemma-2`) is used for real-time tasks like severity scoring and dynamic prompt generation, ensuring these checks don't introduce latency.

This distributed cognition approach ensures that the right tool is used for each specific task, leading to a more efficient and effective system.

## Technology Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **Core Libraries:** `sentence-transformers`, `numpy`, `requests`
* **LLM Orchestration:** OpenRouter API
* **Models:** `gemma-3`, `deepseek-r1`, `gemma-2`

## Setup and Installation

To run this project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/IncognitoQuack/Mindmate.git](https://github.com/IncognitoQuack/Mindmate.git)
    cd Mindmate
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a file named `.env` in the root directory and add your API keys:
    ```
    OPENROUTER_API_KEY="your_primary_key_here"
    OPENROUTER_API_KEY_DASHBOARD="your_secondary_key_here"
    ```

5.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

## Usage

1.  Launch the application.
2.  Enter your OpenRouter API keys in the sidebar.
3.  Begin a conversation in the **Chat** tab.
4.  After a few exchanges, navigate to the sidebar and click **Generate Dashboard Insights**.
5.  Switch to the **Dashboard** tab to view the analysis of your session.

## Ethical Considerations & Disclaimer

**Mindmate is an experimental proof-of-concept and is not a substitute for professional medical advice, diagnosis, or treatment.** It is not a licensed medical device or a healthcare provider. If you are in crisis or believe you may have a medical condition, please consult with a qualified healthcare professional immediately. The flagging system is designed as a safety net but should not be solely relied upon for crisis management.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
