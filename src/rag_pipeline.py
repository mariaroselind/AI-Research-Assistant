# src/rag_pipeline.py
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def generate_llm_answer(question: str, retrieved_chunks: list) -> str:
    """
    Combines retrieved chunks into a prompt template and calls 
    the free Groq Cloud API to generate a response.
    """
    raw_key = "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"
    
    # Updated model field to use the active llama-3.1-8b-instant footprint
    llm = ChatGroq(
        model="llama-3.1-8b-instant", 
        temperature=0.2,
        api_key=raw_key
    )
    
    # Combine the text contents of our retrieved chunks into one string
    context_text = ""
    for doc in retrieved_chunks:
        context_text += f"\n---\nSource: {doc.metadata['source']}\n{doc.page_content}\n"
        
    # System Prompt Architecture
    system_prompt_template = (
        "You are an expert AI Research Assistant. Your task is to provide comprehensive, "
        "accurate answers based strictly on the provided Context below.\n\n"
        "Guidelines:\n"
        "- Cite information directly from the source filename if available.\n"
        "- If the answer cannot be found in the context, politely state: 'I am sorry, but the provided documents do not contain enough information to answer that question.'\n"
        "- Do not make up facts or use outside training knowledge.\n\n"
        "Context:\n{context}\n"
    )
    
    # Create Prompt Layout
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt_template),
        ("human", "{question}")
    ])
    
    # Build and execute execution chain
    chain = prompt | llm | StrOutputParser()
    
    response = chain.invoke({
        "context": context_text,
        "question": question
    })
    
    return response