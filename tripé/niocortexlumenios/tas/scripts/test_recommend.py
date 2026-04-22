import requests

URL = "http://127.0.0.1:8000/api/v1/recommend/"

def run():
    print("\n🔍 Testando Recomendação (Feed Personalizado)...")
    payload = {"user_id": "ian_master", "context": "YOURLIFE_FEED"}
    try:
        r = requests.post(URL, json=payload)
        if r.status_code == 200:
            print(f"🎯 Feed Gerado: {r.json().get('items')}")
        else:
            print(f"❌ Erro no Feed: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"❗ Erro: {e}")

if __name__ == "__main__":
    run()