import re
import logging
from typing import Dict, Any, Set, List, Optional

logger = logging.getLogger("MERCURIO_TOPIC_MANAGER")

class TopicMetadata:
    def __init__(self, name: str, description: str = "", priority: str = "medium", rate_limit: int = 0, require_auth: bool = False):
        self.name = name
        self.description = description
        self.priority = priority  # critical, high, medium, low
        self.rate_limit = rate_limit  # max messages per second, 0 = unlimited
        self.require_auth = require_auth

class TopicManager:
    def __init__(self):
        self._topics: Dict[str, TopicMetadata] = {}
        self._allowed_prefixes: Set[str] = {"metrics", "telemetry", "commands", "alerts", "system"}
        self._initialize_default_topics()

    def _initialize_default_topics(self):
        """Pre-registers default critical topics for the PentaIA ecosystem."""
        defaults = [
            TopicMetadata("system:health", "System health and heartbeat status", "high"),
            TopicMetadata("metrics:perf", "High-performance processing metrics", "medium"),
            TopicMetadata("telemetry:radar", "Real-time AI telemetry data", "high"),
            TopicMetadata("commands:critical", "Critical operational commands", "critical", require_auth=True),
            TopicMetadata("alerts:security", "Security warnings and anomalies", "critical"),
        ]
        for t in defaults:
            self.register_topic(t)

    def register_topic(self, metadata: TopicMetadata) -> bool:
        """Registers a new topic structure after validation."""
        if not self.is_valid_format(metadata.name):
            logger.warning(f"Invalid topic format: {metadata.name}")
            return False
        
        self._topics[metadata.name] = metadata
        logger.info(f"Topic registered successfully: {metadata.name} (Priority: {metadata.priority})")
        return True

    def get_topic_metadata(self, topic: str) -> Optional[TopicMetadata]:
        return self._topics.get(topic)

    def is_valid_format(self, topic: str) -> bool:
        """Validates if the topic name matches the format prefix:name."""
        if not topic or not isinstance(topic, str):
            return False
        
        parts = topic.split(":")
        if len(parts) != 2:
            return False
        
        prefix, name = parts
        if prefix not in self._allowed_prefixes:
            return False
        
        # Name should be alphanumeric with dots, dashes or underscores
        return bool(re.match(r"^[a-zA-Z0-9_\-\.\*]+$", name))

    def match_topic(self, pattern: str, topic: str) -> bool:
        """Matches a subscription pattern (potentially containing wildcards) with a concrete topic.
        
        Supported patterns:
        - Exact match: 'metrics:cpu' matches 'metrics:cpu'
        - Wildcard match: 'metrics:*' matches 'metrics:cpu', 'metrics:memory', etc.
        - Global wildcard: '*' or '*:*' matches any valid topic.
        """
        if pattern == "*" or pattern == "*:*":
            return True
            
        if pattern == topic:
            return True
            
        if "*" in pattern:
            # Escape regex characters and replace * with .*
            regex_pattern = "^" + re.escape(pattern).replace(r"\*", r".*") + "$"
            return bool(re.match(regex_pattern, topic))
            
        return False

    def list_topics(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": t.name,
                "description": t.description,
                "priority": t.priority,
                "rate_limit": t.rate_limit,
                "require_auth": t.require_auth
            }
            for t in self._topics.values()
        ]
