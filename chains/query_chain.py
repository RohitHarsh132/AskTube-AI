from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from utils.prompt_templates import get_prompt_template
from dotenv import load_dotenv
import os
import re

load_dotenv()

def preprocess_query(question):
    """
    Preprocess user query to improve retrieval
    Enhanced with better stop word filtering and context preservation
    """
    # Clean the question
    question = question.strip()
    
    # Extract key terms for better search
    # Remove common words that don't help with search
    stop_words = {'what', 'is', 'are', 'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'this', 'that', 'these', 'those'}
    
    # Keep the original question for context, but also create search terms
    search_terms = ' '.join([word for word in question.lower().split() if word not in stop_words])
    
    return question, search_terms

def context_processor(documents):
    """
    Process and format context for better LLM understanding
    """
    if not documents:
        return "No relevant information found in the video transcript."
    
    # Format context with better structure
    formatted_contexts = []
    for i, doc in enumerate(documents, 1):
        # Clean and format each chunk
        content = doc.page_content.strip()
        if content:
            formatted_contexts.append(f"Transcript Segment {i}:\n{content}\n")
    
    return "\n".join(formatted_contexts)

def build_chain(retriever):
    llm = GoogleGenerativeAI(
        model="gemini-2.5-flash", 
        temperature=0, 
        max_tokens=1000,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    template = get_prompt_template()
    parser = StrOutputParser()

    parallel_chain = RunnableParallel({
        "context": retriever | RunnableLambda(context_processor),
        "question": RunnablePassthrough(),
    })

    return parallel_chain | template | llm | parser