# Verity Finance 🚀

[![MIT License](https://img.shields.io/badge/License-Apache-green.svg)](http://www.apache.org/licenses/LICENSE-2.0)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.5.3-blue.svg)](https://www.typescriptlang.org/)
[![React](https://img.shields.io/badge/React-18.3.1-blue.svg)](https://reactjs.org/)
[![Python](https://img.shields.io/badge/Python-3.11+-yellow.svg)](https://www.python.org/)

Verity Finance leverages AI to generate accurate, data-driven financial reports. It analyzes market trends, historical data, and real-time insights, ensuring consistency and enhancing decision-making for financial firms.

## 📺 Demo

[![Verity Finance Demo](https://img.shields.io/badge/Watch-Demo-red)](https://youtu.be/0B1hBPZt2DI)

> 🎥 Click the badge above to watch Verity Finance in action!

## ✨ Features

- Real-time financial tracking and analytics
- Secure user authentication
- Interactive dashboards and reports
- Budget planning and forecasting
- Transaction categorization with AI
- Customizable alerts and notifications

## 🛠️ Tech Stack

### Frontend

- React
- TypeScript
- ShadCN UI components
- Recharts for data visualization
- Framer Motion
- Clerk.js for authentication

### Backend

- Python 3.11+
- Flask framework
- Tavily API, Rapid API, YFinance API and Prophet for real-time financial data
- OpenAI and Gemini

## 🚀 Getting Started

### Prerequisites

- Node.js 16+
- Python 3.11+

### Installation

1. Clone the repository

```bash
git clone https://github.com/sameer240704/verity-finance-datazen.git
cd frontend
```

2. Install frontend dependencies

```bash
cd frontend
npm install
```

3. Install backend dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

4. Set up environment variables

```bash
# Frontend (.env)
VITE_CLERK_PUBLISHABLE_KEY=
VITE_CLERK_SECRET_KEY=
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/portfolio
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/portfolio
VITE_GNEWS_API_KEY=

# Backend (.env)
OPENAI_KEY=
GEMINI_API_KEY=
RAPID_API_KEY=
TAVILY_API_KEY=
```

5. Start the development servers

Frontend:

```bash
cd frontend
npm start
```

Backend:

```bash
cd backend
python app.py
```

Visit `http://localhost:5173` to access the application.

## 📄 License

This project is licensed under the Apache-2.0 License - see the [LICENSE](http://www.apache.org/licenses/LICENSE-2.0) file for details.

## 🙏 Acknowledgments

- [React Documentation](https://reactjs.org/)
- [Flask](https://flask.palletsprojects.com/en/stable/api/)
- [TypeScript](https://www.typescriptlang.org/)
- All our contributors and supporters
