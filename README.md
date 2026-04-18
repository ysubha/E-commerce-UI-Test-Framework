# E-commerce UI Test Framework

End-to-end UI automation framework for e-commerce flows using 
Playwright and pytest.

## Stack
- Python, Playwright, pytest
- Page Object Model (POM)
- HTML/Allure reporting

## Structure
pages/       → Page Object classes  
tests/       → Test files  
utils/       → Helpers and config  
conftest.py  → Fixtures (setup/teardown)

## How to Run
pip install -r requirements.txt
playwright install
pytest tests/
