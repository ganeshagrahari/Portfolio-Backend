# Ganesh's RAG Chatbot Backend

A custom RAG (Retrieval-Augmented Generation) chatbot built with LangChain, FAISS, and OpenAI.

## 🎉 Current Status: Step 2 In Progress 🚀

✅ Step 1: Prototype Complete
🔄 Step 2: Production Backend Built - Ready to Test!

## 🚀 Quick Start

### Test the Prototype (Step 1)

```bash
cd backend
bash run_test.sh
```

### Run Production Server (Step 2)

```bash
cd backend
bash start_server.sh
```

Then visit:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Test: `python test_api.py`

### Manual Setup

```bash
# 1. Navigate to backend directory
cd backend

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 6. Run the enhanced prototype
python test_prototype.py
```

### What Happens

The prototype will:
- Load data from `data/` directory (4 text files about Ganesh)
- Create a FAISS vector store (cached for future runs)
- Run 8 automatic test questions
- Enter interactive mode for custom questions

**See [TESTING_GUIDE.md](TESTING_GUIDE.md) for detailed instructions!**

## 📁 Project Structure

```
backend/
├── data/                      # Knowledge base files
│   ├── about_ganesh.txt      # Personal info and skills
│   ├── projects.txt          # Project portfolio
│   ├── experience.txt        # Work experience
│   └── contact_info.txt      # Contact details
├── prototype_rag.py          # Simple RAG prototype (basic)
├── test_prototype.py         # Enhanced prototype (loads from files)
├── setup_and_test.sh         # Automated setup script
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── .env                      # Your environment variables (gitignored)
├── .gitignore               # Git ignore rules
├── README.md                # This file
└── TESTING_GUIDE.md         # Detailed testing instructions
```

## 🧪 Testing the Prototype

The prototype includes automatic test questions:
1. "What are Ganesh's main skills?"
2. "Tell me about his projects"
3. "What is his educational background?"
4. "How can I contact Ganesh?"

After tests, you can ask your own questions interactively!

## 🔜 Next Steps

After testing the prototype, we'll build:
1. Complete FastAPI backend with REST endpoints
2. Data ingestion pipeline for multiple file types
3. Modern chat UI in Next.js
4. Meeting scheduling feature
5. Code examples feature
6. Deployment configuration for Render

## 📝 Notes

- This prototype uses `gpt-3.5-turbo` for cost efficiency
- FAISS vector store is stored in memory (will persist to disk in production)
- Sample data is hardcoded (will load from files in production)
