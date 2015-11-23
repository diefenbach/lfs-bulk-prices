import pytest
from selenium import webdriver


@pytest.fixture
def browser(request):
    def fin():
        driver.close()
    request.addfinalizer(fin)

    driver = webdriver.Chrome()
    return driver
