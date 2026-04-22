import requests

def test_ingest():
    url = "http://127.0.0.1:8000/api/v1/events/ingest"
    data = {
        "title": "Operação Policial na Favela - Realidade Nua e Crua",
        "tags": ["real_life", "police", "action"],
        "author_id": "ian_master",
        "safety_label": "restricted"
    }
    try:
        response = requests.post(url, json=data)
        print(f"Status: {response.status_code}, Response: {response.json()}")
    except:
        print("❌ Erro: A API está ligada? Rode 'python -m uvicorn app.main:app --reload'")

if __name__ == "__main__":
    test_ingest()