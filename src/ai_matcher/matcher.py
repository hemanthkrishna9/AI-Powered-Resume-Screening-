"""
Resume Matcher - Match resumes against job descriptions.

This module implements the core matching logic using vector similarity
and provides match scores with explanations using Azure OpenAI.
"""

from typing import Dict, List, Tuple, Optional
import logging
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from .embeddings import EmbeddingGenerator
from .azure_openai_client import AzureOpenAIClient

logger = logging.getLogger(__name__)


class ResumeMatcher:
    """
    Match resumes against job descriptions using semantic similarity.

    This class uses embeddings to compute similarity scores and
    provides AI-powered explanations for the matches.
    """

    def __init__(self, embedding_generator: Optional[EmbeddingGenerator] = None):
        """
        Initialize the resume matcher.

        Args:
            embedding_generator: Instance of EmbeddingGenerator (creates new if None)
        """
        if embedding_generator is None:
            self.embedding_generator = EmbeddingGenerator()
        else:
            self.embedding_generator = embedding_generator

        try:
            self.azure_client = AzureOpenAIClient()
        except Exception as e:
            logger.warning(f"Failed to initialize Azure client for explanations: {e}")
            self.azure_client = None

        logger.info("ResumeMatcher initialized")

    def compute_similarity(
        self, resume_embedding: np.ndarray, jd_embedding: np.ndarray
    ) -> float:
        """
        Compute cosine similarity between resume and job description.

        Args:
            resume_embedding: Resume embedding vector
            jd_embedding: Job description embedding vector

        Returns:
            Similarity score between 0 and 1
        """
        try:
            # Reshape for sklearn
            resume_emb = resume_embedding.reshape(1, -1)
            jd_emb = jd_embedding.reshape(1, -1)

            similarity = cosine_similarity(resume_emb, jd_emb)[0][0]

            # Normalize to 0-1 range (cosine similarity can be -1 to 1)
            normalized_score = (similarity + 1) / 2

            return float(normalized_score)

        except Exception as e:
            logger.error(f"Error computing similarity: {e}")
            return 0.0

    def match_resume_to_jd(
        self, resume_data: Dict, job_description: str, jd_skills: Optional[List[str]] = None
    ) -> Dict:
        """
        Match a single resume against a job description.

        Args:
            resume_data: Parsed resume data dictionary
            job_description: Job description text
            jd_skills: Optional list of required skills from JD

        Returns:
            Dictionary containing match score and explanation
        """
        logger.info("Matching resume to job description")

        try:
            # Create resume text from extracted data
            resume_text = self._create_resume_text(resume_data)

            # Generate embeddings
            resume_embedding = self.embedding_generator.generate_embedding(resume_text)
            jd_embedding = self.embedding_generator.generate_embedding(job_description)

            # Compute similarity score
            match_score = self.compute_similarity(resume_embedding, jd_embedding)

            # Extract skills
            resume_skills = set([s.lower() for s in resume_data.get('skills', [])])

            # Match skills
            matching_skills = []
            missing_skills = []

            if jd_skills:
                jd_skills_lower = set([s.lower() for s in jd_skills])
                matching_skills = list(resume_skills.intersection(jd_skills_lower))
                missing_skills = list(jd_skills_lower.difference(resume_skills))

            # Skill match score
            skill_match_score = len(matching_skills) / len(jd_skills) if jd_skills else match_score

            # Experience match (simplified)
            total_exp = resume_data.get('total_experience', 0)
            experience_match = min(total_exp / 5.0, 1.0)  # Normalize to 5 years

            # Education match (simplified - if they have a degree)
            education_match = 1.0 if resume_data.get('education', []) else 0.5

            # Weighted final score
            final_score = (
                match_score * 0.5 +  # Semantic similarity
                skill_match_score * 0.3 +  # Skills match
                experience_match * 0.15 +  # Experience
                education_match * 0.05  # Education
            )

            # Generate AI explanation
            explanation = self._generate_explanation(
                resume_data, job_description, final_score, matching_skills, missing_skills
            )

            return {
                "match_score": round(final_score, 3),
                "semantic_score": round(match_score, 3),
                "skill_match_score": round(skill_match_score, 3),
                "matching_skills": matching_skills[:10],  # Top 10
                "missing_skills": missing_skills[:10],  # Top 10
                "experience_match": round(experience_match, 3),
                "education_match": round(education_match, 3),
                "total_experience": total_exp,
                "explanation": explanation
            }

        except Exception as e:
            logger.error(f"Error matching resume: {e}")
            return {
                "match_score": 0.0,
                "matching_skills": [],
                "missing_skills": [],
                "experience_match": 0.0,
                "education_match": 0.0,
                "explanation": f"Error during matching: {str(e)}"
            }

    def batch_match(
        self, resumes: List[Dict], job_description: str, jd_skills: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Match multiple resumes against a job description.

        Args:
            resumes: List of parsed resume data dictionaries
            job_description: Job description text
            jd_skills: Optional list of required skills from JD

        Returns:
            List of match results for each resume
        """
        logger.info(f"Batch matching {len(resumes)} resumes")

        results = []
        for idx, resume in enumerate(resumes):
            logger.info(f"Matching resume {idx + 1}/{len(resumes)}")
            match_result = self.match_resume_to_jd(resume, job_description, jd_skills)
            match_result['resume_id'] = resume.get('id', f'resume_{idx}')
            match_result['candidate_name'] = resume.get('contact', {}).get('name', 'Unknown')
            results.append(match_result)

        logger.info(f"Completed batch matching for {len(resumes)} resumes")
        return results

    def _create_resume_text(self, resume_data: Dict) -> str:
        """Create searchable text from resume data."""
        text_parts = []

        # Add skills
        skills = resume_data.get('skills', [])
        if skills:
            text_parts.append(f"Skills: {', '.join(skills)}")

        # Add experience
        experience = resume_data.get('experience', [])
        for exp in experience:
            text_parts.append(f"{exp.get('role', '')} at {exp.get('company', '')}")

        # Add education
        education = resume_data.get('education', [])
        for edu in education:
            text_parts.append(f"{edu.get('degree', '')} from {edu.get('institution', '')}")

        # Add certifications
        certifications = resume_data.get('certifications', [])
        if certifications:
            text_parts.append(f"Certifications: {', '.join(certifications)}")

        # Add raw summary
        summary = resume_data.get('summary', '')
        if summary:
            text_parts.append(summary)

        return " | ".join(text_parts)

    def _generate_explanation(
        self,
        resume_data: Dict,
        job_description: str,
        match_score: float,
        matching_skills: List[str],
        missing_skills: List[str]
    ) -> str:
        """Generate AI-powered explanation for the match."""
        if self.azure_client:
            try:
                explanation = self.azure_client.generate_match_explanation(
                    resume_data, job_description, match_score, matching_skills, missing_skills
                )
                return explanation
            except Exception as e:
                logger.warning(f"Failed to generate AI explanation: {e}")

        # Fallback to basic explanation
        return self._basic_explanation(match_score, matching_skills, missing_skills)

    def _basic_explanation(
        self, match_score: float, matching_skills: List[str], missing_skills: List[str]
    ) -> str:
        """Generate basic explanation without AI."""
        match_percentage = int(match_score * 100)

        if match_score >= 0.8:
            quality = "Excellent"
            advice = "Strong candidate, highly recommended for interview."
        elif match_score >= 0.6:
            quality = "Good"
            advice = "Suitable candidate with relevant experience."
        elif match_score >= 0.4:
            quality = "Moderate"
            advice = "May be considered if specific skills can be developed."
        else:
            quality = "Weak"
            advice = "Not recommended for this position."

        explanation = f"{quality} match ({match_percentage}%). "

        if matching_skills:
            explanation += f"Strong skills: {', '.join(matching_skills[:5])}. "

        if missing_skills and match_score < 0.7:
            explanation += f"Missing: {', '.join(missing_skills[:3])}. "

        explanation += advice

        return explanation.strip()
