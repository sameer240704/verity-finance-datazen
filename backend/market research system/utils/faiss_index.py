import faiss
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.retrievers import BM25Retriever, EnsembleRetriever
import os

class FAISSIndex:
    def __init__(self, index_path="faiss_index", embedding_model_name="sentence-transformers/all-mpnet-base-v2"):
        self.index_path = index_path
        self.embedding_model_name = embedding_model_name
        self.embedding_model = None
        self.faiss_index = None
        self.ensemble_retriever = None
        self.load_index()  # Load the index on initialization

    def load_index(self):
        """
        Loads the FAISS index and creates the ensemble retriever.
        """
        try:
            self.embedding_model = HuggingFaceEmbeddings(model_name=self.embedding_model_name)
            self.faiss_index = FAISS.load_local(
                self.index_path, self.embedding_model, allow_dangerous_deserialization=True
            )
            self.ensemble_retriever = self.create_ensemble_retriever()
            print("FAISS index loaded successfully.")
        except Exception as e:
            print(f"Error loading FAISS index: {e}")
            self.faiss_index = None
            self.ensemble_retriever = None

    def create_ensemble_retriever(self):
        """
        Creates an ensemble retriever with BM25 and FAISS.
        """
        docs = list(self.faiss_index.docstore._dict.values())
        bm25_retriever = BM25Retriever.from_documents(docs)
        bm25_retriever.k = 5 # You can adjust k as needed
        faiss_retriever = self.faiss_index.as_retriever(search_kwargs={"k": 5, "search_type": "similarity"})
        ensemble_retriever = EnsembleRetriever(
            retrievers=[bm25_retriever, faiss_retriever], weights=[0.3, 0.7]
        )
        return ensemble_retriever

    def query_index(self, query, top_k=5):
        """
        Queries the FAISS index using the ensemble retriever.

        Args:
            query: The query string.
            top_k: The number of top results to return.

        Returns:
            A list of relevant document chunks.
        """
        if self.ensemble_retriever is None:
            print("Ensemble retriever is not initialized. Load the index first.")
            return []

        results = self.ensemble_retriever.get_relevant_documents(query)[:top_k]
        return [result.page_content for result in results]