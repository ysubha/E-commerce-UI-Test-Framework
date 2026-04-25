# E-commerce UI Test Framework

A production-grade UI test automation framework for e-commerce flows, built with Playwright and pytest. Demonstrates Page Object Model, multi-layer test pyramid, parallel execution, dynamic test data, API mocking, and CI/CD integration.

![CI](https://github.com/ysubha/E-commerce-UI-Test-Framework/actions/workflows/ci.yml/badge.svg)

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.11 | Core language |
| Playwright | Browser automation |
| pytest | Test runner and fixture management |
| pytest-xdist | Parallel test execution |
| Faker | Dynamic test data generation |
| unittest.mock | External dependency mocking |
| Allure + pytest-html | Test reporting |
| GitHub Actions | CI/CD pipeline |

---

## Project Structure

```
SwagLabsUIAutomationProject/
├── SwagLabsUIAutomation/
│   ├── pageObjects/          # Page Object classes (one class per page)
│   │   ├── login.py
│   │   ├── dashboard.py
│   │   ├── cart.py
│   │   ├── checkout_overview1.py
│   │   ├── checkout_overview2.py
│   │   └── order_success_page.py
│   ├── tests/
│   │   ├── conftest.py               # Shared fixtures and hooks
│   │   ├── integration_tests/        # Page-level integration tests
│   │   │   ├── test_page1_login_page_flow.py
│   │   │   ├── test_page2_dashboard_page_flow.py
│   │   │   ├── test_page3_cart_page_flow.py
│   │   │   ├── test_page4_checkout_overview1_page_flow.py
│   │   │   ├── test_page5_checkout_overview2_page_flow.py
│   │   │   ├── test_page6_order_success_page_flow.py
│   │   │   └── test_page7_post_logout_verifications.py
│   │   ├── e2e_tests/                # Full user journey tests
│   │   │   └── test_e2e_full_purchase_flow.py
│   │   └── unit_tests/               # Business logic and mock tests
│   │       ├── test_price_calculator.py
│   │       └── test_mock_payment_processor.py
│   ├── utils/
│   │   └── price_calculator.py       # Business logic (tax, total, net price)
│   └── data/
│       ├── login_credentials.json
│       ├── checkout_user_details.json
│       └── product_details.json
├── .github/
│   └── workflows/
│       └── ci.yml                    # GitHub Actions pipeline
├── pytest.ini                        # Test configuration
├── requirements.txt                  # Pinned dependencies
└── .gitignore
```

---

## Test Pyramid

```
        /\
       /E2E\         1 test — full purchase flow (login → cart → checkout → logout)
      /------\
     /  Integ  \     28 tests — page-level flows (login, cart, checkout, security)
    /------------\
   /    Unit      \  9 tests — PriceCalculator logic + API mock (unittest.mock)
  /--------------/
```

### Unit Tests (`unit_tests/`)
Tests pure business logic in complete isolation — no browser, no network.
- `test_price_calculator.py` — validates tax calculation, total calculation, and net price across parametrized inputs
- `test_mock_payment_processor.py` — demonstrates `unittest.mock.patch` to mock `requests.post`, isolating the payment processor from real HTTP calls. Tests success, failure, and payload verification.

### Integration Tests (`integration_tests/`)
Tests each page's UI flows end-to-end against the real application using a shared browser session.
- Login: valid credentials, invalid credentials, locked-out user, missing fields
- Dashboard: product listing, sorting (4 strategies), cart add/remove
- Cart: persistence on refresh, persistence on navigation
- Checkout Step 1: valid flow, error validations (empty fields)
- Checkout Step 2: order overview validation, order completion
- Navigation: logout, reset app state
- Security: direct URL access without login (5 protected routes)

### E2E Tests (`e2e_tests/`)
Tests the complete purchase journey in a single flow: cookie clear → login → add items → cart → checkout with Faker-generated user details → order completion → logout → security verification.

---

## How to Run

### Setup

```bash
pip install -r requirements.txt
playwright install --with-deps
```

### Run all tests

```bash
pytest SwagLabsUIAutomation/tests/ -v
```

### Run by layer

```bash
# Unit tests only
pytest -m unit_test -v

# Integration tests only
pytest -m integration -v

# E2E tests only
pytest -m e2e -v
```

### Run with parallel workers

```bash
pytest SwagLabsUIAutomation/tests/ -v -n 4
```

### Run with Allure report

```bash
pytest SwagLabsUIAutomation/tests/ -v
allure serve reports/allure-results
```

### Run with HTML report

Report auto-generated at `reports/report.html` after every run.

---

## Key Design Decisions

- **Page Object Model** — each page class encapsulates its own locators and actions. Tests never interact with Playwright directly; they call page methods. This means a locator change requires updating one class, not every test.

- **Session-scoped browser, function-scoped fixtures** — a single browser instance is shared across the entire test suite for performance. Each test gets a fresh login state via `context.clear_cookies()`, preventing session bleed between tests.

- **Faker for dynamic test data** — checkout user details (first name, last name, postcode) are generated fresh per test using Faker, avoiding hardcoded data and making tests resilient to input validation changes.

- **unittest.mock for external isolation** — unit tests mock `requests.post` using `unittest.mock.patch`, ensuring they test only the core logic and never fail due to network issues or API unavailability.

- **Allure screenshot on failure** — a `pytest_runtest_makereport` hook captures a screenshot automatically on any test failure and attaches it to the Allure report. The fixture is browser-aware and skips gracefully for unit tests that have no browser.

- **Parallel execution** — `pytest-xdist` with `-n auto` is configured in `pytest.ini` for parallel test execution, reducing full suite runtime significantly.
