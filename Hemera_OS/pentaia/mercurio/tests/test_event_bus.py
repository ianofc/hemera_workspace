import asyncio
from core.topic_manager import TopicManager
from core.event_bus import InMemoryEventBus

def test_in_memory_event_bus_pub_sub():
    async def run_test():
        tm = TopicManager()
        bus = InMemoryEventBus(tm)
        await bus.start()

        received_messages = []
        async def callback(msg):
            received_messages.append(msg)

        sub_id = await bus.subscribe("metrics:cpu", callback)
        
        # Publish matching message
        pub_count = await bus.publish("metrics:cpu", {"value": 75.0})
        assert pub_count == 1
        
        # Give event loop a small tick to process background tasks
        await asyncio.sleep(0.02)
        assert len(received_messages) == 1
        assert received_messages[0]["value"] == 75.0
        assert received_messages[0]["_topic"] == "metrics:cpu"

        # Unsubscribe
        unsub_success = await bus.unsubscribe("metrics:cpu", sub_id)
        assert unsub_success is True

        # Publish again
        pub_count_after = await bus.publish("metrics:cpu", {"value": 80.0})
        assert pub_count_after == 0

        await bus.stop()

    asyncio.run(run_test())

def test_event_bus_wildcard_matching():
    async def run_test():
        tm = TopicManager()
        bus = InMemoryEventBus(tm)
        await bus.start()

        received = []
        async def cb(msg):
            received.append(msg)

        await bus.subscribe("metrics:*", cb)
        
        # Publish matching topics
        await bus.publish("metrics:cpu", {"metric": "cpu"})
        await bus.publish("metrics:memory", {"metric": "mem"})
        
        # Publish non-matching topic
        await bus.publish("telemetry:radar", {"metric": "radar"})
        
        await asyncio.sleep(0.02)
        
        assert len(received) == 2
        metrics = [m["metric"] for m in received]
        assert "cpu" in metrics
        assert "mem" in metrics
        assert "radar" not in metrics

        await bus.stop()

    asyncio.run(run_test())
