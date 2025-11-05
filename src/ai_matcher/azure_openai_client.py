"""
Azure OpenAI Client - Integration with Azure OpenAI Services.

This module provides a client for Azure OpenAI API to generate embeddings
and use GPT models for candidate matching explanations.
"""

from typing import List, Dict, Optional, Union
import logging
from openai import AzureOpenAI
import numpy as np

from config.settings import settings

logger = logging.getLogger(__name__)


class AzureOpenAIClient:
    """
    Client for Azure OpenAI API.

    Handles embeddings generation and GPT completions using Azure OpenAI infrastructure.
    """

    def __init__(self):
        """Initialize Azure OpenAI client."""
        if not settings.AZURE_OPENAI_ENABLED:
            logger.warning("Azure OpenAI is disabled in settings")
            self.client = None
            return

        if not settings.AZURE_OPENAI_API_KEY or not settings.AZURE_OPENAI_ENDPOINT:
            logger.error("Azure OpenAI credentials not configured")
            raise ValueError("Azure OpenAI API key and endpoint must be set in environment variables")

        try:
            self.client = AzureOpenAI(
                api_key=settings.AZURE_OPENAI_API_KEY,
                api_version=settings.AZURE_OPENAI_API_VERSION,
                azure_endpoint=settings.AZURE_OPENAI_ENDPOINT
            )

            # GPT client with different API version
            self.gpt_client = AzureOpenAI(
                api_key=settings.AZURE_OPENAI_API_KEY,
                api_version=settings.AZURE_GPT_API_VERSION,
                azure_endpoint=settings.AZURE_OPENAI_ENDPOINT
            )

            logger.info("Azure OpenAI client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Azure OpenAI client: {e}")
            raise

    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text using Azure OpenAI.

        Args:
            text: Input text to embed

        Returns:
            Numpy array containing the embedding vector
        """
        if not self.client:
            logger.error("Azure OpenAI client not initialized")
            return np.zeros(settings.AZURE_EMBEDDING_DIMENSION)

        if not text or not text.strip():
            logger.warning("Empty text provided for embedding")
            return np.zeros(settings.AZURE_EMBEDDING_DIMENSION)

        try:
            # Clean and prepare text
            text = text.strip().replace("\n", " ")

            # Generate embedding
            response = self.client.embeddings.create(
                input=text,
                model=settings.AZURE_EMBEDDING_DEPLOYMENT
            )

            embedding = response.data[0].embedding
            logger.debug(f"Generated embedding with dimension: {len(embedding)}")

            return np.array(embedding, dtype=np.float32)

        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return np.zeros(settings.AZURE_EMBEDDING_DIMENSION)

    def generate_embeddings(self, texts: List[str], batch_size: int = 16) -> np.ndarray:
        """
        Generate embeddings for multiple texts in batches.

        Args:
            texts: List of texts to embed
            batch_size: Number of texts to process in each batch

        Returns:
            Numpy array of shape (n_texts, embedding_dim)
        """
        if not self.client:
            logger.error("Azure OpenAI client not initialized")
            return np.zeros((len(texts), settings.AZURE_EMBEDDING_DIMENSION))

        if not texts:
            logger.warning("Empty text list provided")
            return np.zeros((0, settings.AZURE_EMBEDDING_DIMENSION))

        logger.info(f"Generating embeddings for {len(texts)} texts in batches of {batch_size}")

        all_embeddings = []

        try:
            # Process in batches
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]

                # Clean texts
                clean_batch = [text.strip().replace("\n", " ") for text in batch]

                # Generate embeddings for batch
                response = self.client.embeddings.create(
                    input=clean_batch,
                    model=settings.AZURE_EMBEDDING_DEPLOYMENT
                )

                # Extract embeddings
                batch_embeddings = [item.embedding for item in response.data]
                all_embeddings.extend(batch_embeddings)

                logger.debug(f"Processed batch {i // batch_size + 1}/{(len(texts) + batch_size - 1) // batch_size}")

            embeddings_array = np.array(all_embeddings, dtype=np.float32)
            logger.info(f"Generated embeddings with shape: {embeddings_array.shape}")

            return embeddings_array

        except Exception as e:
            logger.error(f"Error generating batch embeddings: {e}")
            return np.zeros((len(texts), settings.AZURE_EMBEDDING_DIMENSION))

    def generate_match_explanation(
        self,
        resume_data: Dict,
        job_description: str,
        match_score: float,
        matching_skills: List[str],
        missing_skills: List[str]
    ) -> str:
        """
        Generate human-readable explanation for candidate match using GPT.

        Args:
            resume_data: Parsed resume data
            job_description: Job description text
            match_score: Computed match score (0-1)
            matching_skills: List of matching skills
            missing_skills: List of missing skills

        Returns:
            Generated explanation text
        """
        if not self.gpt_client:
            logger.warning("GPT client not initialized, returning basic explanation")
            return self._generate_basic_explanation(match_score, matching_skills, missing_skills)

        try:
            # Prepare prompt
            prompt = self._create_explanation_prompt(
                resume_data, job_description, match_score, matching_skills, missing_skills
            )

            # Generate explanation
            response = self.gpt_client.chat.completions.create(
                model=settings.AZURE_GPT_DEPLOYMENT,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert HR analyst providing concise candidate match explanations."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=300
            )

            explanation = response.choices[0].message.content.strip()
            logger.debug("Generated match explanation using GPT")

            return explanation

        except Exception as e:
            logger.error(f"Error generating GPT explanation: {e}")
            return self._generate_basic_explanation(match_score, matching_skills, missing_skills)

    def _create_explanation_prompt(
        self,
        resume_data: Dict,
        job_description: str,
        match_score: float,
        matching_skills: List[str],
        missing_skills: List[str]
    ) -> str:
        """Create prompt for explanation generation."""
        match_percentage = int(match_score * 100)

        prompt = f"""
Analyze this candidate match and provide a concise explanation (2-3 sentences):

Match Score: {match_percentage}%
Matching Skills: {', '.join(matching_skills[:10]) if matching_skills else 'None'}
Missing Skills: {', '.join(missing_skills[:5]) if missing_skills else 'None'}
Candidate Experience: {resume_data.get('total_experience', 'Not specified')} years

Provide a professional, actionable explanation focusing on:
1. Why this is a good/moderate/weak match
2. Key strengths relevant to the role
3. Any critical gaps (if score < 70%)

Keep it concise and recruiter-friendly.
"""
        return prompt.strip()

    def _generate_basic_explanation(
        self,
        match_score: float,
        matching_skills: List[str],
        missing_skills: List[str]
    ) -> str:
        """Generate basic explanation without GPT."""
        match_percentage = int(match_score * 100)

        if match_score >= 0.8:
            quality = "Excellent"
        elif match_score >= 0.6:
            quality = "Good"
        elif match_score >= 0.4:
            quality = "Moderate"
        else:
            quality = "Weak"

        explanation = f"{quality} match ({match_percentage}%). "

        if matching_skills:
            explanation += f"Strong in: {', '.join(matching_skills[:5])}. "

        if missing_skills and match_score < 0.7:
            explanation += f"Missing: {', '.join(missing_skills[:3])}."

        return explanation.strip()

    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings produced by the model."""
        return settings.AZURE_EMBEDDING_DIMENSION

    def test_connection(self) -> bool:
        """
        Test Azure OpenAI connection.

        Returns:
            True if connection successful
        """
        try:
            test_embedding = self.generate_embedding("test")
            return len(test_embedding) == settings.AZURE_EMBEDDING_DIMENSION
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
