"""
Browser Session Manager
"""
import json
from pathlib import Path
from typing import Dict, Optional
from config.settings import SESSIONS_DIR
from utils.logger import get_logger
from utils.helpers import get_domain

logger = get_logger(__name__)


class SessionManager:
    """Manages persistent browser sessions"""

    def __init__(self, sessions_dir: Path = SESSIONS_DIR):
        """
        Initialize session manager.

        Args:
            sessions_dir: Directory to store session data
        """
        self.sessions_dir = sessions_dir
        self.sessions_dir.mkdir(exist_ok=True)

    def _get_session_file(self, url: str) -> Path:
        """Get session file path for domain"""
        domain = get_domain(url).replace(".", "_")
        return self.sessions_dir / f"{domain}.json"

    def save_session(self, url: str, session_data: Dict):
        """
        Save session data for domain.

        Args:
            url: Target URL
            session_data: Session information (cookies, storage, etc.)
        """
        session_file = self._get_session_file(url)

        try:
            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            logger.info(f"Saved session for {get_domain(url)}")
        except Exception as e:
            logger.error(f"Error saving session: {e}")

    def load_session(self, url: str) -> Optional[Dict]:
        """
        Load session data for domain.

        Args:
            url: Target URL

        Returns:
            Session data dictionary or None
        """
        session_file = self._get_session_file(url)

        if session_file.exists():
            try:
                with open(session_file, 'r') as f:
                    session_data = json.load(f)
                logger.info(f"Loaded session for {get_domain(url)}")
                return session_data
            except Exception as e:
                logger.error(f"Error loading session: {e}")

        return None

    def has_session(self, url: str) -> bool:
        """Check if we have saved session for domain"""
        return self._get_session_file(url).exists()

    def delete_session(self, url: str):
        """Delete saved session for domain"""
        session_file = self._get_session_file(url)
        if session_file.exists():
            session_file.unlink()
            logger.info(f"Deleted session for {get_domain(url)}")