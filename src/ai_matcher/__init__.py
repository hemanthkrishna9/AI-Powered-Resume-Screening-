"""
AI Matcher Module.

This module handles AI-powered matching between resumes and job descriptions
using sentence embeddings and vector similarity.
"""

from .embeddings import EmbeddingGenerator
from .matcher import ResumeMatcher
from .ranker import CandidateRanker

__all__ = ["EmbeddingGenerator", "ResumeMatcher", "CandidateRanker"]
