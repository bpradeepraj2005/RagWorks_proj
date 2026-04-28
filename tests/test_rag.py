import os
import sys

# Ensure imports work from the root directory during testing
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from rag_engine.vector_db import RAGEngine

def test_rag_initialization():
    engine = RAGEngine()
    # Ensure collection was created and populated
    assert engine.collection.count() > 0

def test_rag_retrieval_accuracy():
    engine = RAGEngine()
    # Test a specific policy
    result = engine.query("What is the return policy for electronics?")
    
    # The return policy string mentions '14 days' and 'electronics'
    assert "electronics" in result.lower()
    assert "14 days" in result.lower()
