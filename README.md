# 🤖 Portfolio AI Chatbot Backend

> **Live Backend**: https://portfolio-backend-9g97.onrender.com  
> **Frontend**: https://ganesh-portfolio-site.vercel.app/  
> **Status**: ✅ Deployed and Running

A production-ready RAG (Retrieval-Augmented Generation) chatbot backend built with FastAPI, LangChain, FAISS, and OpenAI. This backend powers the AI assistant "Viag" on Ganesh's portfolio website.

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [API Documentation](#-api-documentation)
- [Environment Variables](#-environment-variables)
- [Deployment](#-deployment)
- [Development](#-development)
- [Testing](#-testing)
- [Troubleshooting](#-troubleshooting)

---

## ✨ Features

- **🧠 RAG-Powered Responses**: Uses FAISS vector store for semantic search over knowledge base
- **💬 Conversational Memory**: Maintains context across multiple messages in a session
- **📚 Knowledge Base**: Loads data from markdown/text files about experience, projects, skills, etc.
- **🔄 Session Management**: Tracks conversations with unique session IDs
- **🚀 Production Ready**: Deployed on Render with automatic deployments
- **📖 Auto-Generated Docs**: FastAPI provides interactive API documentation
- **🔒 CORS Enabled**: Configured for secure cross-origin requests
- **⚡ Fast & Efficient**: Uses FAISS for lightning-fast vector similarity search

---

## 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| **FastAPI** | High-performance Python web framework |
| **LangChain** | LLM orchestration and RAG pipeline |
| **FAISS** | Vector similarity search (Facebook AI) |
| **OpenAI GPT-3.5** | Language model for generating responses |
| **Uvicorn** | ASGI server for production |
| **Python 3.11+** | Programming language |

---

## 📁 Project Structure

```
Portfolio-Backend/
├── app/                          # Application code
│   ├── main.py                   # FastAPI entry point & routes
│   ├── api/                      # API endpoints
│   │   └── chat.py              # Chat endpoint logic
│   ├── core/                     # Core functionality
│   │   ├── config.py            # Configuration & settings
│   │   └── rag.py               # RAG system implementation
│   └── models/                   # Data models
│       └── schemas.py           # Pydantic schemas
│
├── data/                         # Knowledge base files
│   ├── about_ganesh.md          # Personal info, skills, bio
│   ├── experience.md            # Work experience & roles
│   ├── projects.txt             # Project portfolio
│   ├── contact_info.txt         # Contact information
│   └── Ganesh-Agrahari-2.pdf    # Resume (optional)
│
├── faiss_index/                  # Vector store (auto-generated)
│   ├── index.faiss              # FAISS index file
│   └── index.pkl                # Metadata pickle file
│
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker configuration
├── render.yaml                   # Render deployment config
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore rules
├── start_server.sh              # Local development script
├── rebuild_index.sh             # Rebuild FAISS index script
└── README.md                     # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Git

### Local Development Setup

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/Portfolio-Backend.git
cd Portfolio-Backend

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
nano .env  # Add your OPENAI_API_KEY

# 5. Run the server
bash start_server.sh
```

The server will start at: **http://localhost:8000**

### Quick Test

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test chat endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are Ganesh'\''s skills?", "session_id": "test123"}'
```

---

## 📖 API Documentation

### Base URL

- **Production**: `https://portfolio-backend-9g97.onrender.com`
- **Local**: `http://localhost:8000`

### Interactive Docs

- **Swagger UI**: `https://portfolio-backend-9g97.onrender.com/docs`
- **ReDoc**: `https://portfolio-backend-9g97.onrender.com/redoc`

### Endpoints

#### 1. Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "message": "Ganesh's AI Assistant API is running"
}
```

#### 2. Chat Endpoint

```http
POST /api/chat
```

**Request Body:**
```json
{
  "message": "What are your skills?",
  "session_id": "unique-session-id"
}
```

**Response:**
```json
{
  "response": "I have expertise in Python, FastAPI, React, Next.js...",
  "sources": ["about_ganesh.md", "experience.md"],
  "session_id": "unique-session-id"
}
```

**Parameters:**
- `message` (string, required): User's question or message
- `session_id` (string, required): Unique identifier for conversation session

---

## 🔐 Environment Variables

Create a `.env` file in the root directory:

```bash
# Required
OPENAI_API_KEY=sk-proj-your-actual-api-key-here

# Optional (with defaults)
ENVIRONMENT=production
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_TEMPERATURE=0.7
CORS_ORIGINS=https://ganesh-portfolio-site.vercel.app,http://localhost:3000
```

### Variable Descriptions

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key (required) | None |
| `ENVIRONMENT` | Environment mode | `production` |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-3.5-turbo` |
| `OPENAI_TEMPERATURE` | Response randomness (0-1) | `0.7` |
| `CORS_ORIGINS` | Allowed origins (comma-separated) | See above |

---

## 🚀 Deployment

### Deploy to Render

This backend is configured for one-click deployment to Render.

#### Prerequisites
- GitHub account
- Render account ([Sign up free](https://render.com))
- OpenAI API key

#### Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Create Web Service on Render**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will auto-detect settings from `render.yaml`

3. **Add Environment Variables**
   - Go to your service → "Environment"
   - Add `OPENAI_API_KEY` with your actual key
   - Add `CORS_ORIGINS` with your frontend URL

4. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for deployment
   - Your backend will be live at: `https://your-service.onrender.com`

#### Auto-Deployment

Every push to `main` branch triggers automatic redeployment on Render.

---

## 💻 Development

### Project Architecture

```
User Request
    ↓
FastAPI Endpoint (/api/chat)
    ↓
RAG System (core/rag.py)
    ↓
1. Query FAISS Vector Store
2. Retrieve relevant documents
3. Build context with conversation history
4. Send to OpenAI API
    ↓
Response with sources
```

### Key Components

#### 1. **RAG System** (`app/core/rag.py`)
- Loads documents from `data/` directory
- Creates FAISS vector embeddings
- Handles semantic search
- Manages conversation memory

#### 2. **API Routes** (`app/main.py`, `app/api/chat.py`)
- FastAPI endpoints
- Request validation
- Error handling
- CORS configuration

#### 3. **Data Models** (`app/models/schemas.py`)
- Pydantic models for request/response validation
- Type safety

### Adding New Knowledge

1. **Add/Edit files in `data/` directory**
   ```bash
   nano data/new_info.md
   ```

2. **Rebuild FAISS index**
   ```bash
   bash rebuild_index.sh
   ```

3. **Commit and push**
   ```bash
   git add data/
   git commit -m "Update: added new information"
   git push origin main
   ```

Render will auto-deploy and rebuild the index.

---

## 🧪 Testing

### Manual Testing

```bash
# Start local server
bash start_server.sh

# In another terminal, test endpoints
curl http://localhost:8000/health

curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about your experience", "session_id": "test"}'
```

### Test Questions

Try these questions to test the chatbot:
- "What are your main skills?"
- "Tell me about your projects"
- "What is your work experience?"
- "How can I contact you?"
- "What technologies do you know?"

### Production Testing

```bash
# Test production backend
curl https://portfolio-backend-9g97.onrender.com/health

curl -X POST https://portfolio-backend-9g97.onrender.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "session_id": "prod-test"}'
```

---

## 🔧 Troubleshooting

### Issue: "FAISS index not found"

**Solution:**
```bash
bash rebuild_index.sh
```

### Issue: "OpenAI API key not found"

**Solution:**
1. Check `.env` file exists
2. Verify `OPENAI_API_KEY` is set correctly
3. Restart the server

### Issue: CORS errors

**Solution:**
1. Check `CORS_ORIGINS` includes your frontend URL
2. Ensure no trailing slashes in URLs
3. Restart service after changing environment variables

### Issue: Slow first response (Render Free Tier)

**Cause:** Free tier services sleep after 15 minutes of inactivity

**Solution:**
- First request takes 30-60 seconds to wake up
- Subsequent requests are fast
- Upgrade to Starter plan ($7/month) for always-on service

### Issue: Rate limit errors

**Cause:** OpenAI API rate limits exceeded

**Solution:**
1. Wait a few minutes
2. Check usage at https://platform.openai.com/usage
3. Upgrade OpenAI plan if needed

---

## 📊 Monitoring & Maintenance

### Check Logs

**Render Dashboard:**
1. Go to https://dashboard.render.com
2. Select your service
3. Click "Logs" tab

### Monitor Costs

- **Render**: Free tier or check billing dashboard
- **OpenAI**: https://platform.openai.com/usage
- **Estimated monthly cost**: $1-5 for personal portfolio

### Update Dependencies

```bash
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt
git commit -am "Update dependencies"
git push origin main
```

---

## 📚 Additional Resources

### Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [Render Documentation](https://render.com/docs)

### Related Repositories
- **Frontend**: [Portfolio-Site](https://github.com/ganeshagrahari/ganesh-site-deploy)

---

## 📝 License

This project is for personal portfolio use.

---

## 👤 Author

**Ganesh Agrahari**

- Portfolio: https://ganesh-portfolio-site.vercel.app/
- GitHub: [@ganeshagrahari](https://github.com/ganeshagrahari)

---

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Powered by [OpenAI](https://openai.com/)
- Vector search by [FAISS](https://github.com/facebookresearch/faiss)
- Orchestrated with [LangChain](https://python.langchain.com/)

---

**Need help?** Open an issue or check the troubleshooting section above.

**Happy coding!** 🚀
