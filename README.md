# E-commerce UI Test Framework

A production-grade UI test automation framework for e-commerce flows, built with **Playwright + pytest** against the [SauceDemo](https://www.saucedemo.com) application. It demonstrates a full test pyramid (unit → integration → E2E), the Page Object Model, parallel execution, data-driven parametrization, external-dependency mocking, and CI/CD via GitHub Actions.

![CI](https://github.com/ysubha/E-commerce-UI-Test-Framework/actions/workflows/ci.yml/badge.svg)

---

## Why this project exists

This framework is a working demonstration of *how* to structure a UI automation suite the way a test engineer would in a real product team — not just a collection of scripts. Each layer answers a specific question:

- **Unit layer** — *Can I test logic without a browser or a network?* Proves isolation technique: pure business logic and mocked external calls.
- **Integration layer** — *Does each page of the app behave correctly on its own?* Exercises every page's real UI flows through Page Objects against the live app.
- **E2E layer** — *Does the whole journey hold together?* One realistic end-to-end purchase, start to finish, on dynamic data.

If you are reading this to understand the project quickly: start with the **Test Suite** section below — it lists what each file tests and, more importantly, *why*.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.11 | Core language |
| Playwright (sync API) | Browser automation |
| pytest | Test runner and fixture management |
| pytest-xdist | Parallel test execution |
| Faker | Dynamic test data generation (E2E) |
| unittest.mock | External dependency mocking (unit) |
| Allure + pytest-html | Test reporting |
| GitHub Actions | CI/CD pipeline |

---

## Test Suite at a Glance

The suite contains **28 test functions**, which pytest expands to **45 collected test cases** through parametrization.

| Layer | Files | Test functions | Collected cases | Marker |
|---|---|---|---|---|
| Unit | 2 | 6 | 10 | `unit_test` |
| Integration | 7 | 21 | 34 | `integration` |
| E2E | 1 | 1 | 1 | `e2e` |
| **Total** | **10** | **28** | **45** | |

> **Why the two numbers differ:** several tests use `@pytest.mark.parametrize`, so one function runs as many cases. Example: `test_no_access_to_app_pages_without_login` is a single function but runs 5 times (once per protected route). "45" is what `pytest --collect-only` reports; "28" is the number of test *definitions*.

```
        /\
       /E2E \        1 case  — full purchase journey (login → cart → checkout → logout → security)
      /------\
     / Integ  \      34 cases (21 funcs) — page-level flows: login, inventory, cart, checkout, nav, security
    /----------\
   /   Unit     \    10 cases (6 funcs)  — PriceCalculator logic + payment API mock (no browser, no network)
  /--------------\
```

> **Note on shape:** this is an intentionally UI-heavy portfolio suite, so the integration layer carries the most cases. In a full product codebase the unit base would be the widest layer; here the unit tests exist to demonstrate isolation *technique* rather than exhaustive logic coverage.

---

## Project Structure

```
SwagLabsUIAutomationProject/
├── SwagLabsUIAutomation/
│   ├── pageObjects/          # One Page Object class per page
│   │   ├── login.py
│   │   ├── dashboard.py
│   │   ├── cart.py
│   │   ├── checkout_overview1.py
│   │   ├── checkout_overview2.py
│   │   └── order_success_page.py
│   ├── tests/
│   │   ├── conftest.py               # Shared fixtures, hooks, screenshot-on-failure
│   │   ├── integration_tests/        # Page-level integration tests (7 files)
│   │   │   ├── test_page1_login_page_flow.py
│   │   │   ├── test_page2_dashboard_page_flow.py
│   │   │   ├── test_page3_cart_page_flow.py
│   │   │   ├── test_page4_checkout_overview1_page_flow.py
│   │   │   ├── test_page5_checkout_overview2_page_flow.py
│   │   │   ├── test_page6_order_success_page_flow.py
│   │   │   └── test_page7_post_logout_verifications.py
│   │   ├── e2e_tests/
│   │   │   └── test_e2e_full_purchase_flow.py
│   │   └── unit_tests/
│   │       ├── test_price_calculator.py
│   │       └── test_mock_payment_processor.py
│   ├── utils/
│   │   └── price_calculator.py       # Business logic under unit test (tax, total, net price)
│   └── data/
│       ├── login_credentials.json    # Drives login parametrization
│       ├── checkout_user_details.json# Drives checkout error-validation parametrization
│       └── product_details.json      # Expected inventory (names, prices, descriptions)
├── .github/workflows/ci.yml          # GitHub Actions pipeline
├── pytest.ini                        # Markers + parallel config
├── requirements.txt
└── .gitignore
```

---

## The Test Suite in Detail

### Unit tests — `unit_tests/` (6 functions → 10 cases)

Pure logic, run in complete isolation. No browser, no HTTP. These are the fastest tests and the ones that would run on every commit.

**`test_price_calculator.py`** — validates the `PriceCalculator` business logic across parametrized inputs:
- `calculate_tax` — tax on an amount (8% model), checked at whole and fractional values.
- `calculate_total` — net-of-tax total.
- `calculate_net_price` — sum of a product list, including the empty-cart edge case (`[] → 0.00`).

**`test_mock_payment_processor.py`** — demonstrates mocking an external HTTP dependency with `unittest.mock.patch('requests.post')`, so the payment logic is tested without ever hitting a real payment API. Covers three verification depths:
- **Success path** — asserts the returned status/body.
- **Failure path** — asserts correct handling of a `400` / failed response.
- **Payload verification** — `assert_called_once_with(...)` proves the function called the API with the *exact* URL and JSON body, not just that it was called.

*This file is the reference example for the mock-vs-stub-vs-spy distinction: it verifies both the return value and the call itself.*

### Integration tests — `integration_tests/` (21 functions → 34 cases)

Each file maps to one page of the app and tests that page's real UI behaviour through Page Objects against the live site. A shared browser session is reused for speed; each test starts from a clean cookie state.

| File | Page / Concern | What it verifies |
|---|---|---|
| `test_page1_login_page_flow.py` | Login (entry point) | Valid login across 3 user types (standard, performance_glitch, problem_user); invalid credentials; missing username/password; locked-out user; error clears after correction; session persists on refresh |
| `test_page2_dashboard_page_flow.py` | Inventory / Products | Product list rendered with correct name/price/description/image; product count; sorting by all 4 strategies (name A–Z, Z–A, price low–high, high–low); add/remove items; cart badge count |
| `test_page3_cart_page_flow.py` | Cart | Cart contents persist across page refresh and across back-and-forth navigation (state management) |
| `test_page4_checkout_overview1_page_flow.py` | Checkout — Step 1 (info) | Valid personal-info submission; field-level error validation for empty first name / last name / postal code (data-driven from JSON) |
| `test_page5_checkout_overview2_page_flow.py` | Checkout — Step 2 (overview) | All selected items appear; item total, tax, and grand-total math on the real page; order completes and confirms |
| `test_page6_order_success_page_flow.py` | Order success + Navigation | Logout after order; reset-app-state clears the cart |
| `test_page7_post_logout_verifications.py` | Security / Access control | Direct-URL access to 5 protected routes without login is blocked with the correct error; back-navigation after logout is blocked |

### E2E test — `e2e_tests/` (1 function → 1 case)

**`test_e2e_full_purchase_flow.py`** — the apex of the pyramid. A single test that stitches the entire user journey into one flow:

`clear cookies → login (standard_user) → add two items → verify cart → checkout → fill details with Faker-generated data → complete order → verify success → logout → verify protected pages are inaccessible.`

Kept deliberately as **one** test: E2E flows are the slowest and most brittle, so the suite invests in many cheap integration tests and only one full journey to confirm the pieces work together.

---

## Running the tests

### Setup

```bash
pip install -r requirements.txt
playwright install --with-deps
```

### Run everything

```bash
pytest SwagLabsUIAutomation/tests/ -v
```

### Run one layer (via markers)

```bash
pytest -m unit_test -v     # 10 cases, no browser
pytest -m integration -v   # 34 cases
pytest -m e2e -v           # 1 case
```

### Run in parallel

```bash
pytest SwagLabsUIAutomation/tests/ -v -n 4      # explicit workers
pytest SwagLabsUIAutomation/tests/ -v -n auto   # match CPU cores
```

### Reports

```bash
# Allure
pytest SwagLabsUIAutomation/tests/ -v
allure serve reports/allure-results

# HTML report auto-generated at reports/report.html after every run
```

---

## Key Design Decisions

- **Page Object Model** — each page class owns its locators and actions; tests call page methods and never touch Playwright directly. A locator change is a one-class edit, not a suite-wide find-and-replace.

- **Session-scoped browser, function-scoped state** — one browser instance is shared across the whole suite for performance, while each test resets to a clean state via `context.clear_cookies()`, preventing session bleed.

- **Data-driven parametrization** — login credentials and checkout error cases are loaded from JSON in `data/`, so adding a new case is a data edit, not a code change. This is why 28 functions expand to 45 cases.

- **Custom markers for teardown control** — markers like `no_reset` and `no_dashboard_teardown` let individual tests opt out of the default reset/teardown when a test needs to observe post-logout or error-persistence behaviour.

- **Faker for dynamic E2E data** — the E2E checkout uses freshly generated user details each run, avoiding hardcoded data and staying resilient to input-validation changes.

- **External isolation with `unittest.mock`** — the payment unit tests mock `requests.post`, so they test only the core logic and never fail on network flakiness or API downtime.

- **Screenshot on failure** — a `pytest_runtest_makereport` hook captures a screenshot on any failure and attaches it to the Allure report; it is browser-aware and skips cleanly for unit tests that have no browser.

- **Parallel-ready** — `pytest-xdist` (`-n auto`) is configured for parallel execution, cutting full-suite runtime.
