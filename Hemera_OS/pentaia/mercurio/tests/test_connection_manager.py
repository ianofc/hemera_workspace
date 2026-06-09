import asyncio
from core.topic_manager import TopicManager
from core.event_bus import InMemoryEventBus
from core.connection_manager import ConnectionManager

class MockWebSocket:
    def __init__(self):
        self.sent_messages = []
        self.closed = False
        self.close_code = None
        self.close_reason = None
        
    async def accept(self):
        pass
        
    async def send_json(self, data):
        if self.closed:
            raise Exception("Connection closed")
        self.sent_messages.append(data)
        
    async def close(self, code=1000, reason=""):
        self.closed = True
        self.close_code = code
        self.close_reason = reason

def test_connection_manager_connect_disconnect():
    async def run_test():
        tm = TopicManager()
        eb = InMemoryEventBus(tm)
        await eb.start()
        
        cm = ConnectionManager(eb, tm)
        await cm.start()
        
        ws = MockWebSocket()
        client_id = "client_123"
        
        # Connect
        success = await cm.connect(ws, client_id, ["metrics:cpu"])
        assert success is True
        assert client_id in cm._connections
        
        # Update subscription
        update_success = await cm.update_subscriptions(client_id, ["metrics:cpu", "metrics:mem"])
        assert update_success is True
        assert cm._connections[client_id].subscribed_patterns == ["metrics:cpu", "metrics:mem"]
        
        # Disconnect
        await cm.disconnect(ws)
        assert client_id not in cm._connections
        
        await cm.stop()
        await eb.stop()
        
    asyncio.run(run_test())

def test_connection_manager_routing():
    async def run_test():
        tm = TopicManager()
        eb = InMemoryEventBus(tm)
        await eb.start()
        
        cm = ConnectionManager(eb, tm)
        await cm.start()
        
        ws1 = MockWebSocket()
        ws2 = MockWebSocket()
        
        # Connect client 1 interested in metrics
        await cm.connect(ws1, "c1", ["metrics:*"])
        # Connect client 2 interested only in security alerts
        await cm.connect(ws2, "c2", ["alerts:security"])
        
        # Publish metrics event to Event Bus
        await eb.publish("metrics:cpu", {"load": 99.0})
        await asyncio.sleep(0.02) # let routing task run
        
        assert len(ws1.sent_messages) == 1
        assert ws1.sent_messages[0]["load"] == 99.0
        assert len(ws2.sent_messages) == 0
        
        # Publish alerts event
        await eb.publish("alerts:security", {"threat": "high"})
        await asyncio.sleep(0.02)
        
        assert len(ws1.sent_messages) == 1 # still 1
        assert len(ws2.sent_messages) == 1
        assert ws2.sent_messages[0]["threat"] == "high"
        
        await cm.stop()
        await eb.stop()
        
    asyncio.run(run_test())
