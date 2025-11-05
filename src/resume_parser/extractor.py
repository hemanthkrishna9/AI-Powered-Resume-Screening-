"""
Data Extractor - Extract structured information from resume text.

This module contains functionality to extract specific fields
from parsed resume text using NLP techniques.
"""

from typing import Dict, List, Optional
import logging
import re
import spacy
from datetime import datetime

logger = logging.getLogger(__name__)


class DataExtractor:
    """
    Extract structured data from resume text.

    Uses NLP and pattern matching to identify and extract:
    - Contact information
    - Skills
    - Work experience
    - Education
    - Certifications
    """

    def __init__(self):
        """Initialize the data extractor."""
        logger.info("DataExtractor initialized")

        try:
            # Load spaCy model
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("Loaded spaCy model: en_core_web_sm")
        except Exception as e:
            logger.warning(f"Failed to load spaCy model: {e}")
            self.nlp = None

        # Common technical skills
        self.common_skills = {
            # Programming Languages
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'php', 'go', 'rust', 'swift', 'kotlin',
            # Web Technologies
            'html', 'css', 'react', 'angular', 'vue', 'nodejs', 'express', 'django', 'flask', 'fastapi',
            # Databases
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'oracle', 'dynamodb',
            # Cloud & DevOps
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'gitlab', 'terraform', 'ansible',
            # Data Science & ML
            'machine learning', 'deep learning', 'nlp', 'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
            # Others
            'git', 'linux', 'api', 'rest', 'graphql', 'microservices', 'agile', 'scrum', 'ci/cd'
        }

    def extract_all(self, text: str) -> Dict:
        """
        Extract all information from resume text.

        Args:
            text: Raw resume text

        Returns:
            Dictionary containing all extracted fields
        """
        logger.info("Extracting data from resume text")

        contact_info = self.extract_contact(text)
        skills = self.extract_skills(text)
        experience = self.extract_experience(text)
        education = self.extract_education(text)
        certifications = self.extract_certifications(text)

        # Calculate total experience
        total_experience = self._calculate_total_experience(experience)

        return {
            "contact": contact_info,
            "skills": skills,
            "experience": experience,
            "education": education,
            "certifications": certifications,
            "total_experience": total_experience,
            "summary": self._generate_summary(skills, experience, education)
        }

    def extract_contact(self, text: str) -> Dict:
        """Extract contact information."""
        contact = {
            "email": None,
            "phone": None,
            "linkedin": None,
            "github": None
        }

        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, text)
        if email_match:
            contact["email"] = email_match.group(0)

        # Extract phone
        phone_pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
        phone_match = re.search(phone_pattern, text)
        if phone_match:
            contact["phone"] = phone_match.group(0).strip()

        # Extract LinkedIn
        linkedin_pattern = r'(?:linkedin\.com/in/|linkedin\.com/profile/view\?id=)([A-Za-z0-9\-]+)'
        linkedin_match = re.search(linkedin_pattern, text, re.IGNORECASE)
        if linkedin_match:
            contact["linkedin"] = linkedin_match.group(0)

        # Extract GitHub
        github_pattern = r'github\.com/([A-Za-z0-9\-]+)'
        github_match = re.search(github_pattern, text, re.IGNORECASE)
        if github_match:
            contact["github"] = github_match.group(0)

        logger.debug(f"Extracted contact: {contact}")
        return contact

    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from text."""
        skills = set()
        text_lower = text.lower()

        # Extract common technical skills
        for skill in self.common_skills:
            if skill.lower() in text_lower:
                skills.add(skill.title())

        # Extract skills from "Skills:" section
        skills_section_pattern = r'(?:skills|technical skills|core competencies)[\s:]+([^\n]+(?:\n[^\n]+)*?)(?:\n\n|\n[A-Z])'
        skills_match = re.search(skills_section_pattern, text, re.IGNORECASE)
        if skills_match:
            skills_text = skills_match.group(1)
            # Split by common delimiters
            for skill in re.split(r'[,;•|]', skills_text):
                skill = skill.strip()
                if skill and len(skill) > 2:
                    skills.add(skill.title())

        logger.debug(f"Extracted {len(skills)} skills")
        return sorted(list(skills))

    def extract_experience(self, text: str) -> List[Dict]:
        """Extract work experience."""
        experience_list = []

        # Pattern to find experience section
        exp_pattern = r'(?:experience|work history|employment)[\s:]+([^\n]+(?:\n[^\n]+)*?)(?:\n\n|\neducation|\ncertifications|$)'
        exp_match = re.search(exp_pattern, text, re.IGNORECASE | re.DOTALL)

        if exp_match:
            exp_text = exp_match.group(1)

            # Try to find company names and roles
            # Common patterns: "Software Engineer at Google", "Google - Software Engineer"
            job_pattern = r'([^\n]+?)\s+(?:at|@|-)\s+([^\n]+?)(?:\n|$)'
            for match in re.finditer(job_pattern, exp_text):
                role = match.group(1).strip()
                company = match.group(2).strip()

                experience_list.append({
                    "company": company,
                    "role": role,
                    "duration": self._extract_duration(match.group(0))
                })

        logger.debug(f"Extracted {len(experience_list)} experience entries")
        return experience_list

    def extract_education(self, text: str) -> List[Dict]:
        """Extract education details."""
        education_list = []

        # Common degree patterns
        degree_patterns = [
            r'(B\.?Tech|Bachelor of Technology|B\.?E\.?|Bachelor of Engineering|B\.?S\.?|Bachelor of Science)',
            r'(M\.?Tech|Master of Technology|M\.?E\.?|Master of Engineering|M\.?S\.?|Master of Science|MBA)',
            r'(Ph\.?D\.?|Doctor of Philosophy)'
        ]

        for pattern in degree_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                degree = match.group(0)

                # Try to find the institution (usually following the degree)
                context = text[match.start():match.end() + 200]
                institution = self._extract_institution(context)

                # Try to find year
                year = self._extract_year(context)

                education_list.append({
                    "degree": degree,
                    "institution": institution,
                    "year": year
                })

        logger.debug(f"Extracted {len(education_list)} education entries")
        return education_list

    def extract_certifications(self, text: str) -> List[str]:
        """Extract certifications."""
        certifications = []

        # Pattern to find certifications section
        cert_pattern = r'(?:certifications?|certificates?)[\s:]+([^\n]+(?:\n[^\n]+)*?)(?:\n\n|\n[A-Z]|$)'
        cert_match = re.search(cert_pattern, text, re.IGNORECASE)

        if cert_match:
            cert_text = cert_match.group(1)
            # Split by newlines and common delimiters
            for line in cert_text.split('\n'):
                line = line.strip()
                if line and len(line) > 5:
                    # Remove bullets and clean up
                    line = re.sub(r'^[•\-\*]\s*', '', line)
                    certifications.append(line)

        # Common certifications
        common_certs = [
            'AWS Certified', 'Azure Certified', 'PMP', 'CISSP', 'Scrum Master',
            'Google Cloud', 'CompTIA', 'ITIL'
        ]

        for cert in common_certs:
            if cert.lower() in text.lower() and cert not in certifications:
                certifications.append(cert)

        logger.debug(f"Extracted {len(certifications)} certifications")
        return certifications

    def _extract_duration(self, text: str) -> str:
        """Extract duration from experience text."""
        # Pattern: "2020 - 2023", "Jan 2020 - Present", etc.
        duration_pattern = r'(\d{4}|[A-Za-z]{3,9}\s+\d{4})\s*[-–]\s*(Present|\d{4}|[A-Za-z]{3,9}\s+\d{4})'
        match = re.search(duration_pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)
        return "Duration not specified"

    def _extract_institution(self, text: str) -> str:
        """Extract institution name from education context."""
        # Look for university/college/institute
        inst_pattern = r'(?:from|at)\s+([A-Z][A-Za-z\s,&]+(?:University|College|Institute|School))'
        match = re.search(inst_pattern, text)
        if match:
            return match.group(1).strip()
        return "Institution not specified"

    def _extract_year(self, text: str) -> Optional[int]:
        """Extract year from text."""
        year_pattern = r'\b(19|20)\d{2}\b'
        matches = re.findall(year_pattern, text)
        if matches:
            years = [int(y) for y in matches]
            return max(years)  # Return most recent year
        return None

    def _calculate_total_experience(self, experience_list: List[Dict]) -> float:
        """Calculate total years of experience."""
        if not experience_list:
            return 0.0

        # Simple estimation: count unique companies
        # In reality, you'd parse dates and calculate properly
        total_years = len(experience_list) * 2.5  # Rough estimate

        return round(total_years, 1)

    def _generate_summary(self, skills: List[str], experience: List[Dict], education: List[Dict]) -> str:
        """Generate a brief summary of the candidate."""
        summary_parts = []

        if experience:
            summary_parts.append(f"{len(experience)} previous roles")

        if skills:
            top_skills = ', '.join(skills[:5])
            summary_parts.append(f"Skills: {top_skills}")

        if education:
            summary_parts.append(f"{len(education)} degrees")

        return " | ".join(summary_parts) if summary_parts else "No summary available"
