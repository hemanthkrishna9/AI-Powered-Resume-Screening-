"""
Candidate Ranker - Rank candidates based on match scores.

This module ranks candidates and provides filtering and sorting capabilities.
"""

from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class CandidateRanker:
    """
    Rank and filter candidates based on match scores and criteria.

    This class provides methods to rank candidates, apply filters,
    and generate ranked shortlists.
    """

    def __init__(self, min_score: float = 0.5):
        """
        Initialize the candidate ranker.

        Args:
            min_score: Minimum match score threshold for candidates
        """
        self.min_score = min_score
        logger.info(f"CandidateRanker initialized with min_score: {min_score}")

    def rank_candidates(
        self, candidates: List[Dict], key: str = "match_score"
    ) -> List[Dict]:
        """
        Rank candidates by a specified scoring key.

        Args:
            candidates: List of candidate dictionaries
            key: Key to use for ranking (default: "match_score")

        Returns:
            Sorted list of candidates in descending order
        """
        logger.info(f"Ranking {len(candidates)} candidates by {key}")

        # Sort by the specified key in descending order
        ranked = sorted(
            candidates,
            key=lambda x: x.get(key, 0),
            reverse=True
        )

        return ranked

    def filter_by_score(
        self, candidates: List[Dict], min_score: Optional[float] = None
    ) -> List[Dict]:
        """
        Filter candidates by minimum score threshold.

        Args:
            candidates: List of candidate dictionaries
            min_score: Minimum score threshold (uses instance default if None)

        Returns:
            Filtered list of candidates
        """
        threshold = min_score if min_score is not None else self.min_score
        logger.info(f"Filtering candidates with score >= {threshold}")

        filtered = [
            candidate for candidate in candidates
            if candidate.get("match_score", 0) >= threshold
        ]

        logger.info(f"Filtered to {len(filtered)} candidates")
        return filtered

    def get_top_n(
        self, candidates: List[Dict], n: int = 10
    ) -> List[Dict]:
        """
        Get top N candidates.

        Args:
            candidates: List of candidate dictionaries
            n: Number of top candidates to return

        Returns:
            Top N candidates
        """
        logger.info(f"Getting top {n} candidates")
        ranked = self.rank_candidates(candidates)
        return ranked[:n]

    def generate_shortlist(
        self,
        candidates: List[Dict],
        top_n: int = 10,
        min_score: Optional[float] = None
    ) -> Dict:
        """
        Generate a shortlist with ranked and filtered candidates.

        Args:
            candidates: List of candidate dictionaries
            top_n: Maximum number of candidates in shortlist
            min_score: Minimum score threshold

        Returns:
            Dictionary containing shortlist and statistics
        """
        logger.info("Generating candidate shortlist")

        # Filter and rank
        filtered = self.filter_by_score(candidates, min_score)
        shortlist = self.get_top_n(filtered, top_n)

        return {
            "shortlist": shortlist,
            "total_candidates": len(candidates),
            "filtered_count": len(filtered),
            "shortlisted_count": len(shortlist),
            "min_score_used": min_score if min_score is not None else self.min_score
        }
