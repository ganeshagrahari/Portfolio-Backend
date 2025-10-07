"""
RAG (Retrieval-Augmented Generation) System
Handles document loading, vector store, and chat functionality
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document

from app.core.config import settings


class RAGChatbot:
    """RAG-based chatbot for Ganesh's portfolio"""
    
    def __init__(self):
        """Initialize the RAG chatbot"""
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            temperature=settings.OPENAI_TEMPERATURE,
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.vectorstore: Optional[FAISS] = None
        self.qa_chain = None
        
    def load_documents_from_directory(self, directory: str) -> List[Document]:
        """Load all text files from a directory"""
        documents = []
        data_path = Path(directory)
        
        if not data_path.exists():
            raise FileNotFoundError(f"Directory {directory} does not exist")
        
        # Load all .txt and .md files
        txt_files = list(data_path.glob("*.txt"))
        md_files = list(data_path.glob("*.md"))
        all_files = txt_files + md_files
        
        for file_path in all_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    documents.append(Document(
                        page_content=content,
                        metadata={"source": file_path.name}
                    ))
            except Exception as e:
                print(f"Error loading {file_path.name}: {e}")
        
        # Load PDF files if any
        pdf_files = list(data_path.glob("*.pdf"))
        if pdf_files:
            try:
                from PyPDF2 import PdfReader
                for pdf_path in pdf_files:
                    try:
                        reader = PdfReader(str(pdf_path))
                        pdf_content = ""
                        for page in reader.pages:
                            pdf_content += page.extract_text() + "\n"
                        
                        if pdf_content.strip():
                            documents.append(Document(
                                page_content=pdf_content,
                                metadata={"source": pdf_path.name}
                            ))
                    except Exception as e:
                        print(f"Error loading {pdf_path.name}: {e}")
            except ImportError:
                print("PyPDF2 not installed. Skipping PDF files.")
        
        return documents
        
    def create_vectorstore(self, documents: List[Document]) -> None:
        """Create FAISS vector store from documents"""
        if not documents:
            raise ValueError("No documents provided")
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len
        )
        
        chunks = text_splitter.split_documents(documents)
        
        # Create FAISS vectorstore
        self.vectorstore = FAISS.from_documents(chunks, self.embeddings)
        
        # Save vectorstore to disk
        self.vectorstore.save_local(settings.VECTOR_STORE_PATH)
        
    def load_vectorstore(self) -> bool:
        """Load existing vectorstore from disk"""
        try:
            self.vectorstore = FAISS.load_local(
                settings.VECTOR_STORE_PATH,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            return True
        except Exception:
            return False
        
    def setup_qa_chain(self) -> None:
        """Set up the QA chain with custom prompt"""
        if not self.vectorstore:
            raise ValueError("Vector store not initialized")
        
        # Custom prompt template
        template = """You are Ganesh Agrahari's personal AI assistant named Viag. Your role is to help visitors learn about Ganesh - his skills, projects, experience, education, and how to contact him.

Be friendly, professional, and informative. Always provide SPECIFIC and DETAILED information from the context.

IMPORTANT GUIDELINES:
1. **Experience Questions**: Provide detailed information about his internships, roles, responsibilities, and achievements. Include company names, positions, duration, and specific contributions.
2. **Project Questions**: Give specific details including technologies used, features, achievements, and GitHub/demo links.
3. **Skills Questions**: Categorize them clearly (Advanced skills vs Learning) with specific technologies.
4. **Education Questions**: Mention his degree, university, specialization, and expected graduation.
5. **Contact Questions**: Provide email (ganeshagrahari108@gmail.com) and suggest meeting via email with time slots.
6. **Be Specific**: Use actual names, numbers, percentages, and details from the context. Don't give generic answers.
7. **Length**: Provide comprehensive answers for experience/project questions (4-6 sentences), shorter for simple questions.

Context from knowledge base:
{context}

Question: {question}

Detailed Answer:"""

        PROMPT = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        # Create retrieval QA chain
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": settings.RETRIEVAL_K}
            ),
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=True
        )
        
    def chat(self, question: str) -> Dict[str, any]:
        """Process a chat question and return response"""
        if not self.qa_chain:
            raise ValueError("QA chain not initialized")
        
        result = self.qa_chain.invoke({"query": question})
        
        return {
            "question": question,
            "answer": result["result"],
            "sources": [doc.metadata.get("source", "unknown") for doc in result["source_documents"]]
        }
    
    def initialize(self) -> None:
        """Initialize the RAG system (load or create vectorstore)"""
        # Try to load existing vectorstore
        if not self.load_vectorstore():
            # Load documents and create new vectorstore
            documents = self.load_documents_from_directory(settings.DATA_PATH)
            if not documents:
                raise ValueError(f"No documents found in {settings.DATA_PATH}")
            self.create_vectorstore(documents)
        
        # Setup QA chain
        self.setup_qa_chain()


# Global chatbot instance
_chatbot_instance: Optional[RAGChatbot] = None


def get_chatbot() -> RAGChatbot:
    """Get or create the global chatbot instance"""
    global _chatbot_instance
    
    if _chatbot_instance is None:
        _chatbot_instance = RAGChatbot()
        _chatbot_instance.initialize()
    
    return _chatbot_instance
