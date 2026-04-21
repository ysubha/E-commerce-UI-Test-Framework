class PriceCalculator:
    TAX_RATE = 0.08

    def calculate_tax(self, net_price: float) -> float:
        # returns tax rounded to 2 decimal places
        return round(net_price * self.TAX_RATE, 2)

    def calculate_total(self, net_price: float) -> float:
        # returns net_price + tax rounded to 2 decimal places
        return round(self.calculate_tax(net_price) + net_price, 2)

    def calculate_net_price(self, products: list) -> float:
        # takes list of dicts with 'price' key
        # returns sum of all prices alone without tax
        total_price = 0.00
        for product in products:
            total_price += product['price']
        return round(total_price, 2)
