from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import logging

logger = logging.getLogger(__name__)

class IrisEye:
    def __init__(self):
        self.options = Options()
        self.options.add_argument("--headless") # Roda sem abrir janela
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        # Mascarar como usuário real para evitar bloqueios simples
        self.options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")

    def scrape_headlines(self, url):
        """
        Acessa um site de jornal e raspa as manchetes principais (H1, H2, H3)
        """
        driver = None
        data = {"url": url, "headlines": []}
        
        try:
            logger.info(f"Iris observando: {url}")
            driver = webdriver.Chrome(options=self.options)
            driver.get(url)
            
            # Estratégia genérica: pegar todos h1 e h2 com texto
            elements = driver.find_elements(By.CSS_SELECTOR, "h1, h2, h3")
            
            for el in elements:
                text = el.text.strip()
                if text and len(text) > 10: # Ignora textos curtos
                    data["headlines"].append(text)
            
        except Exception as e:
            logger.error(f"Iris falhou ao ver {url}: {e}")
            data["error"] = str(e)
        finally:
            if driver:
                driver.quit()
        
        return data