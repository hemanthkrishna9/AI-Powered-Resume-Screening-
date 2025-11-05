"""
Embedding Generator - Generate semantic embeddings from text.

This module uses Azure OpenAI to create vector embeddings
for resumes and job descriptions.
"""

from typing import List, Union
import logging
import numpy as np

from .azure_openai_client import AzureOpenAIClient

logger = logging.getLogger(__name__)


class EmbeddingGenerator:
    """
    Generate semantic embeddings using Azure OpenAI.

    This class encapsulates the Azure OpenAI embedding model and provides
    methods to generate embeddings for text data.
    """

    def __init__(self):
        """Initialize the embedding generator with Azure OpenAI."""
        logger.info("Initializing EmbeddingGenerator with Azure OpenAI")

        try:
            self.client = AzureOpenAIClient()
            self.embedding_dim = self.client.get_embedding_dimension()
            logger.info(f"Embedding generator initialized (dimension: {self.embedding_dim})")
        except Exception as e:
            logger.error(f"Failed to initialize Azure OpenAI client: {e}")
            raise

    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text.

        Args:
            text: Input text to embed

        Returns:
            Numpy array containing the embedding vector
        """
        if not text or not text.strip():
            logger.warning("Empty text provided for embedding")
            return np.zeros(self.embedding_dim)

        try:
            embedding = self.client.generate_embedding(text)
            logger.debug(f"Generated embedding for text (length: {len(text)} chars)")
            return embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return np.zeros(self.embedding_dim)

    def generate_embeddings(self, texts: List[str], batch_size: int = 16) -> np.ndarray:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of texts to embed
            batch_size: Number of texts to process in each batch

        Returns:
            Numpy array of shape (n_texts, embedding_dim)
        """
        if not texts:
            logger.warning("Empty text list provided")
            return np.zeros((0, self.embedding_dim))

        try:
            logger.info(f"Generating embeddings for {len(texts)} texts")
            embeddings = self.client.generate_embeddings(texts, batch_size=batch_size)
            logger.info(f"Generated embeddings with shape: {embeddings.shape}")
            return embeddings
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {e}")
            return np.zeros((len(texts), self.embedding_dim))

    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of embeddings produced by the model.

        Returns:
            Embedding dimension size
        """
        return self.embedding_dim
