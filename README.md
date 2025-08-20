# Mindmate: An Advanced AI Mental Health Companion

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.37.0-red.svg?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/status-active-success.svg?style=for-the-badge)]()

**Mindmate** is a state-of-the-art conversational AI, engineered to provide a secure, empathetic, and adaptive space for individuals to explore their thoughts and feelings. By integrating a multi-layered AI architecture with a sophisticated, data-driven analytics dashboard, this project demonstrates a professional framework for building responsible and impactful mental wellness technology.

---

### ✨ **[View Live Demo](https://mindmate-5shyhgumxj6dqkczgmb3kt.streamlit.app/)** ✨

---

> **Note:** The live demo is hosted on a community cloud. Please allow a moment for the application to wake up if it's been idle.

## Problem Statement

Mental health challenges among students and professionals are actively rising, yet access to timely, affordable, open, and inclusive support remains limited.  
Traditional counseling services are often constrained by high costs, limited availability, and social stigma—leaving many without consistent emotional support.  

At the same time, existing digital learning platforms lack integrated wellness features that can monitor emotional well-being daily, encourage positive habits, and provide real-time assistance.  

There is a clear need for an accessible, secure, and empathetic digital companion that bridges this gap by offering personalized check-ins, actionable insights, and crisis-sensitive guidance, while ensuring user privacy is protected.

---

## Introduction

In an era where accessible mental health support is crucial, Mindmate serves as an advanced prototype for an AI-powered companion. It is founded on the principle of empathetic listening, providing users with a non-judgmental counterpart for self-reflection. The system is architected not to replace professional therapy, but to act as a powerful supplementary tool. It empowers users to identify patterns in their thoughts, visualize their emotional journey, and learn about evidence-informed wellness concepts within a secure, intuitive, and highly responsive conversational interface.

---

![Mindmate Application Screenshot](https://github.com/IncognitoQuack/Mindmate/blob/main/demo.png) 

---

## Key Innovations

| Feature                        | Description                                                                                                                              |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| 🧠 **Adaptive AI Core** | A dynamic system prompt that self-improves based on conversational flow, adapting the AI's tone and therapeutic approach in real-time.     |
| 📊 **Advanced Analytics** | A comprehensive dashboard with live session metrics and an emotional journey chart, providing users with tangible, data-driven insights. |
| 🔐 **Secure Session Management** | A professional-grade session manager handles API keys securely, ensuring user privacy and key protection without exposing sensitive data. |
| 🛡️ **Intelligent Safety System** | A robust, two-tiered flagging mechanism combines keyword detection with AI-powered severity scoring for responsible crisis management.   |
| 📚 **Grounded Responses (RAG)** | AI responses are grounded in a curated knowledge base of therapeutic concepts, ensuring guidance is relevant and evidence-informed.      |

## System Architecture & Philosophy

Mindmate is built on a philosophy of **Distributed Cognition**, employing a multi-model strategy to optimize performance, reliability, and cost-effectiveness.

1.  **Chat & Reasoning (`google/gemma-3-27b-it`):** A powerful, large-scale model is dedicated to the core conversational tasks, providing nuanced and empathetic responses.
2.  **Dashboard & Structured Data (`deepseek/deepseek-r1-0528`):** A model renowned for its reliability with structured data is used exclusively for generating the dashboard's JSON insights, ensuring robustness.
3.  **Classification & Meta-Analysis (`google/gemma-2-9b-it`):** A smaller, faster model handles real-time tasks like severity scoring and dynamic prompt generation, ensuring these crucial checks occur without user-facing latency.

This approach ensures that the right tool is used for each specific task, leading to a more efficient, intelligent, and effective system.

## Technology Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **Core Libraries:** `sentence-transformers`, `numpy`, `requests`, `plotly`
* **LLM Orchestration:** OpenRouter API

## Setup and Installation

To run this project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/IncognitoQuack/Mindmate.git
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
    streamlit run main.py
    ```

## Ethical Considerations & Disclaimer

**Mindmate is an experimental proof-of-concept and is not a substitute for professional medical advice, diagnosis, or treatment.** It is not a licensed medical device or a healthcare provider. If you are in crisis or believe you may have a medical condition, please consult with a qualified healthcare professional immediately. The flagging system is designed as a safety net but should not be solely relied upon for crisis management.

## Authors

This project was crafted with care by **Team BinaryDuo**.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
