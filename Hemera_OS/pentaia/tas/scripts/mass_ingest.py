import requests
import time

BASE_URL = "http://127.0.0.1:8000/api/v1/events/ingest"

TEST_DATA = [
    {"title": "Operação Policial: Realidade nua e crua", "tags": ["real_life", "police"], "author_id": "rep_01", "safety_label": "restricted"},
    {"title": "Geopolítica Nacional e o STF", "tags": ["politics", "law"], "author_id": "analyst_v", "safety_label": "safe"},
    {"title": "Cena de Acidente na BR-101", "tags": ["real_life", "accident"], "author_id": "user_cam", "safety_label": "nsfw_soft"},
    {"title": "IA e Automação de Sistemas", "tags": ["tech", "coding"], "author_id": "dev_master", "safety_label": "safe"}
]

def run():
    print("📥 Injetando dados de teste...")
    for item in TEST_DATA:
        try:
            r = requests.post(BASE_URL, json=item)
            if r.status_code == 200:
                print(f"✅ Ingerido: {item['title']}")
            else:
                print(f"❌ Erro em '{item['title']}': {r.status_code} - {r.text}")
        except Exception as e:
            print(f"❗ Servidor offline? Erro: {e}")
            break
        time.sleep(0.3)

if __name__ == "__main__":
    run()