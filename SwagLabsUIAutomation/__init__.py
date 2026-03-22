"""
🔐 1. Login Module (High Priority)
        - Positive Scenarios
            Login with valid standard_user credentials
            Login with problem_user credentials
            Login with performance_glitch_user credentials
            Verify user is redirected to inventory page after successful login
            Verify session persists on page refresh

        - Negative Scenarios
            Login with invalid username
            Login with invalid password
            Login with empty username & password
            Login with empty username only
            Login with empty password only
            Verify error message text and UI styling
            Verify error disappears after correcting input

🛒 2. Inventory / Products Page
         - UI & Data Validation
             Verify product list is displayed
             Verify each product has: Name, Price, Description, Image, Add to Cart button
             Verify product count matches expected inventory

        - Sorting
            Sort products by Name (A → Z)
            Sort products by Name (Z → A)
            Sort products by Price (Low → High)
            Sort products by Price (High → Low)

🧺 3. Cart Functionality
        - Add/Remove
            Add single product to cart
            Add multiple products to cart
            Remove product from inventory page
            Remove product from cart page
            Verify cart badge count updates correctly

        - Persistence
            Verify cart items persist after page refresh
            Verify cart items persist after navigating back and forth

💳 4. Checkout Flow (End-to-End)
        - Checkout Step One
            Proceed to checkout with items in cart
            Checkout with valid user information
            Checkout with empty first name
            Checkout with empty last name
            Checkout with empty postal code
            Verify proper error messages for each field

        - Checkout Overview
            Verify selected products appear in checkout overview
            Verify item total calculation
            Verify tax calculation
            Verify total price calculation

        - Completion
            Complete checkout successfully
            Verify success message after order completion
            Verify user is redirected to confirmation page

🔁 5. Navigation & Menu
            Logout from application
            Verify user is redirected to login page after logout
            Verify restricted pages are not accessible after logout
            Reset app state from menu
            Verify cart is cleared after reset

🔒 6. Security & Access Control
            Access inventory page without login
            Access cart page without login
            Verify user is redirected to login page for unauthorized access

⚡ 7. Performance & Reliability (Bonus – SDET-II Level)
            Measure login response time (performance_glitch_user)
            Verify UI is usable during slow loading
            Verify no console errors on page load
"""