class Stock(object):
    def __init__(self):
        self.orders_chain = []

    # Add or Remove order
    def manage_order(self, action_type, order='-', price=-1.0, quantity=-1, index=-1):
        if action_type == 'Remove' and self.orders_chain:
            if next((element for element in self.orders_chain if element["Id"] == index), None):
                order = {
                    'Id': index,
                    'Order': self.orders_chain[index-1]['Order'],
                    'Type': 'Remove',
                    'Price': self.orders_chain[index-1]['Price'],
                    'Quantity': self.orders_chain[index-1]['Quantity'],
                }
                self.orders_chain.append(order)
                self.display_best()
        elif action_type == 'Add':
            order = {
                'Id': len(self.orders_chain) + 1,
                'Order': order,
                'Type': action_type,
                'Price': price,
                'Quantity': quantity,
            }
            self.orders_chain.append(order)
            self.display_best()

        return order

    # Display current best sell and buy orders
    def display_best(self):
        """
        1) find highest buy order(s) and lowest sell order(s) and separate them
        2) sum Quantity** of those orders, buy and sell separately
        3) Display both sums
        **take into account Remove Type.
        """
        best_sell, best_buy = {}, {}
        sorted_lists = self.sort_orders()
        best_buy_quantity, best_sell_quantity = self.sum_orders(sorted_lists)
        if sorted_lists[0]:
            best_buy = {
                "Price": sorted_lists[0][0]['Price'],
                "Quantity": best_buy_quantity,
            }
            print("Current best buy order price: " + str(best_buy['Price']))
            print("Current best buy order quantity: " + str(best_buy['Quantity']))
        if sorted_lists[1]:
            best_sell = {
                "Price": sorted_lists[1][0]['Price'],
                "Quantity": best_sell_quantity,
            }
            print("Current best sell order price: " + str(best_sell['Price']))
            print("Current best sell order quantity: " + str(best_sell['Quantity']))

        print()
        return [best_buy, best_sell]

    # find best sell and buy order
    def sort_orders(self):
        buy_orders = [buy_order for count, buy_order in enumerate(self.orders_chain) if
                      self.orders_chain[count]['Order'] == 'Buy']
        sell_orders = [sell_order for count, sell_order in enumerate(self.orders_chain) if
                      self.orders_chain[count]['Order'] == 'Sell']

        sorted_buy = sorted(buy_orders, key=lambda x: x["Price"], reverse=True)
        sorted_sell = sorted(sell_orders, key=lambda x: x["Price"])

        return [sorted_buy, sorted_sell]

    # Calculate sum of given best buy and sell orders
    @staticmethod
    def sum_orders(sorted_lists):
        summed_orders = []

        best_buy_list = [max_buy for max_buy in sorted_lists[0] if max_buy['Price'] == sorted_lists[0][0]['Price']]
        best_sell_list = [min_sell for min_sell in sorted_lists[1] if min_sell['Price'] == sorted_lists[1][0]['Price']]

        sorted_lists = [best_buy_list, best_sell_list]

        for sorted_list in sorted_lists:
            orders_sum = 0
            for x in sorted_list:
                if x['Type'] == "Remove":
                    orders_sum = orders_sum - x['Quantity']
                elif x['Type'] == "Add":
                    orders_sum = orders_sum + x['Quantity']
            summed_orders.append(orders_sum)

        return summed_orders


stock = Stock()

stock.manage_order(action_type="Remove", index=1)
stock.manage_order(order='Buy', action_type="Add", price=50.0, quantity=100)
stock.manage_order(order='Buy', action_type="Add", price=150.0, quantity=200)
stock.manage_order(order='Buy', action_type="Add", price=150.0, quantity=200)
stock.manage_order(order='Sell', action_type="Add", price=50.0, quantity=100)
stock.manage_order(order='Sell', action_type="Add", price=50.0, quantity=300)
stock.manage_order(order='Sell', action_type="Add", price=650.0, quantity=100)
stock.manage_order(action_type="Remove", index=1)
stock.manage_order(action_type="Remove", index=2)

# Display history of order management
if stock.orders_chain:
    print("    ".join(stock.orders_chain[0].keys()))
    for order in stock.orders_chain:
        print(*order.values(), sep="     ")
