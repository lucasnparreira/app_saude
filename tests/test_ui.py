from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest
import time

@pytest.fixture
def driver():
    driver = webdriver.Chrome()  # Certifique-se de que o chromedriver está no PATH
    yield driver
    driver.quit()

def test_exibir_medidas_ui(driver):
    driver.get('http://localhost:5000/exibir_medidas')
    assert "Historico de medidas" in driver.page_source

    # Testar se os dados são exibidos corretamente (ajuste conforme necessário)
    medidas = driver.find_elements(By.TAG_NAME, "li")
    assert len(medidas) > 0
    assert "Peso" in medidas[0].text

def test_excluir_medidas_ui(driver):
    driver.get('http://localhost:5000/exibir_medidas')
    delete_buttons = driver.find_elements(By.ID, "button-excluir-medidas")
    
    if delete_buttons:
        delete_buttons[0].click()
        time.sleep(2)  # Aguarda a exclusão ser processada
        medidas = driver.find_elements(By.TAG_NAME, "li")
        assert len(medidas) == 0  # Verifique se a lista de medidas está vazia após exclusão
