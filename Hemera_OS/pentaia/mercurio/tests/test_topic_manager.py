from core.topic_manager import TopicManager, TopicMetadata

def test_default_topics():
    manager = TopicManager()
    topics = manager.list_topics()
    names = [t["name"] for t in topics]
    assert "system:health" in names
    assert "metrics:perf" in names

def test_is_valid_format():
    manager = TopicManager()
    assert manager.is_valid_format("metrics:cpu") is True
    assert manager.is_valid_format("telemetry:radar") is True
    assert manager.is_valid_format("invalid_topic") is False
    assert manager.is_valid_format("metrics:") is False
    assert manager.is_valid_format("other:cpu") is False  # 'other' not in allowed prefixes

def test_register_topic():
    manager = TopicManager()
    meta = TopicMetadata("metrics:disk", "Disk performance", "low")
    assert manager.register_topic(meta) is True
    assert "metrics:disk" in [t["name"] for t in manager.list_topics()]

def test_match_topic():
    manager = TopicManager()
    # Exact
    assert manager.match_topic("metrics:cpu", "metrics:cpu") is True
    assert manager.match_topic("metrics:cpu", "metrics:mem") is False
    
    # Wildcard
    assert manager.match_topic("metrics:*", "metrics:cpu") is True
    assert manager.match_topic("metrics:*", "metrics:mem") is True
    assert manager.match_topic("metrics:*", "telemetry:radar") is False
    
    # Global wildcard
    assert manager.match_topic("*", "metrics:cpu") is True
    assert manager.match_topic("*:*", "telemetry:radar") is True
