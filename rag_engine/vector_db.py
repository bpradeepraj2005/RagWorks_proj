import chromadb
from chromadb.utils import embedding_functions
import os
import logging

class RAGEngine:
    def __init__(self):
        self.persist_directory = os.path.join(os.path.dirname(__file__), "chroma_data")
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        
        # Sentence Transformers local model (runs completely free on CPU)
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        
        self.collection = self.client.get_or_create_collection(
            name="store_policies", 
            embedding_function=self.embedding_function
        )
        
        self._initialize_knowledge()

    def _initialize_knowledge(self):
        if self.collection.count() == 0:
            doc_path = os.path.join(os.path.dirname(__file__), "store_policies.txt")
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple chunking by double newline
            chunks = [chunk.strip() for chunk in content.split("\n\n") if chunk.strip()]
            
            self.collection.add(
                documents=chunks,
                ids=[f"policy_chunk_{i}" for i in range(len(chunks))]
            )
            logging.info(f"RAG Knowledge Base initialized with {len(chunks)} documents!")

    def query(self, question: str, n_results: int = 2) -> str:
        logging.info(f"RAG Query execution: '{question}'")
        results = self.collection.query(
            query_texts=[question],
            n_results=n_results
        )
        if results['documents'] and len(results['documents'][0]) > 0:
            return "\n\n".join(results['documents'][0])
        return "No relevant policies found."
