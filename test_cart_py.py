import unittest
from cart import ShoppingCart

class test_add_item_function(unittest.TestCase):
    def test_add_item_normal_case(self):
        cart = ShoppingCart()
        cart.add_item("apple", 1.0, 1)
        self.assertEqual(cart._items["apple"], {"price": 1.0, "quantity": 1})

    def test_add_item_edge_cases_negative_price(self):
        cart = ShoppingCart()
        with self.assertRaises(ValueError):
            cart.add_item("pear", -1.0, 1)

    def test_add_item_edge_case_zero_price(self):
        cart = ShoppingCart()
        cart.add_item("banana", 0.0, 1)
        self.assertEqual(cart._items["banana"], {"price": 0.0, "quantity": 1})

    def test_add_item_edge_cases_negative_quantity(self):
        cart = ShoppingCart()
        with self.assertRaises(ValueError):
            cart.add_item("grape", 1.0, -1)

    def test_add_item_edge_cases_zero_quantity(self):
        cart = ShoppingCart()
        with self.assertRaises(ValueError):
            cart.add_item("orange", 1.0, 0)

    def test_add_item_cumulative_case(self):
        cart = ShoppingCart()
        cart.add_item("apple", 1.0, 1)
        cart.add_item("apple", 1.0, 2)
        self.assertEqual(cart._items["apple"], {"price": 1.0, "quantity": 2})

if __name__ == '__main__':
    unittest.main()

class test_remove_item_function(unittest.TestCase):
    def test_remove_item_normal_case(self):
        cart = ShoppingCart()
        cart.add_item("apple", 1.0, 1)
        cart.remove_item("apple")
        self.assertEqual(cart._items, {})

    def test_remove_item_edge_case_item_not_in_cart(self):
        cart = ShoppingCart()
        with self.assertRaises(KeyError):
            cart.remove_item("apple")

    def test_remove_item_edge_case_empty_cart(self):
        cart = ShoppingCart()
        with self.assertRaises(KeyError):
            cart.remove_item("apple")

    def test_remove_item_cumulative_case_remove_twice(self):
        cart = ShoppingCart()
        cart.add_item("apple", 1.0, 1)
        cart.remove_item("apple")
        with self.assertRaises(KeyError):
            cart.remove_item("apple")

if __name__ == '__main__':
    unittest.main()

class test_apply_discount_function(unittest.TestCase):
    def test_apply_discount_normal_case_percentage(self):
        cart = ShoppingCart()
        cart.add_item("apple", 1.0, 100)
        cart.apply_discount("SAVE10")
        self.assertEqual(cart._discount, {"type": "percent", "value": 10, "min_order": 0.0})

    def test_apply_discount_normal_case_fixed(self):
        cart = ShoppingCart()
        cart.add_item("apple", 1.0, 100)
        cart.apply_discount("FLAT5")
        self.assertEqual(cart._discount, {"type": "fixed", "value": 5.0, "min_order": 30.0})

    def test_apply_discount_edge_case_invalid_code(self):
        cart = ShoppingCart()
        cart.add_item("apple", 1.0, 100)
        with self.assertRaises(ValueError):
            cart.apply_discount("ROFLCOPTER2005_THIS_CODE_IS_INVALID")
    def test_apply_discount_edge_case_zero_oder(self):
        cart = ShoppingCart()
        with self.assertRaises(ValueError):
            cart.apply_discount("SAVE10")

    def test_apply_discount_cumulative_case_two_codes(self):
        cart = ShoppingCart()
        cart.add_item("apple", 1.0, 100)
        cart.apply_discount("SAVE10")
        cart.apply_discount("SAVE20")
        self.assertEqual(cart._discount, {"type": "percent", "value": 20, "min_order": 50.0})

    def test_apply_discount_boundary_case(self):
        cart = ShoppingCart()
        cart.add_item("apple", 1.0, 50)
        with self.assertRaises(ValueError):
            cart.apply_discount("SAVE20")

if __name__ == '__main__':
    unittest.main()

class test_get_total_function(unittest.TestCase):
    def test_get_total_normal_case(self):
        cart = ShoppingCart()
        cart.add_item("apple", 1.0, 10)
        cart.add_item("banana", 2.0, 4)
        cart.get_total()
        self.assertEqual(cart.get_total(), 18.0)

    def test_get_total_normal_case_remove(self):
        cart = ShoppingCart()
        cart.add_item("apple", 1.0, 10)
        cart.add_item("banana", 2.0, 4)
        cart.remove_item("banana")
        cart.get_total()
        self.assertEqual(cart.get_total(), 10.0)

    def test_get_total_edge_case_cart_empty(self):
        cart = ShoppingCart()
        cart.get_total()
        self.assertEqual(cart.get_total(), 0.0)

    def test_get_total_cumulative_case(self):
        cart = ShoppingCart()
        cart.add_item("grape", 2.0, 5)
        cart.get_total()
        cart.add_item("banana", 3.0, 4)
        cart.get_total()
        self.assertEqual(cart.get_total(), 22.0)

if __name__ == '__main__':
    unittest.main()

class test_clear_function(unittest.TestCase):
    def test_clear_normal_case_single_item(self):
        cart = ShoppingCart()
        cart.add_item("apple", 1.0, 1)
        cart.clear()
        self.assertEqual(cart._items, {})

    def test_clear_normal_case_multiple_items(self):
        cart = ShoppingCart()
        cart.add_item("apple", 1.0, 1)
        cart.add_item("banana", 2.0, 2)
        cart.clear()
        self.assertEqual(cart._items, {})

    def test_clear_edge_case_empty_cart(self):
        cart = ShoppingCart()
        cart.clear()
        self.assertEqual(cart._items, {})

    def test_clear_cumulative_case(self):
        cart = ShoppingCart()
        cart.add_item("apple", 1.0, 1)
        cart.clear()
        cart.add_item("banana", 2.0, 2)
        cart.clear()
        self.assertEqual(cart._items, {})

if __name__ == '__main__':
    unittest.main()

class test_get_item_count_function(unittest.TestCase):
    def test_get_item_count_normal_case_single_item(self):
        cart = ShoppingCart()
        cart.add_item("apple", 1.0, 1)
        cart.get_item_count()
        self.assertEqual(cart.get_item_count(), 1)

    def test_get_item_count_normal_case_single_item_multiple(self):
        cart = ShoppingCart()
        cart.add_item("apple", 1.0, 2)
        cart.get_item_count()
        self.assertEqual(cart.get_item_count(), 2)

    def test_get_item_count_normal_case_multiple_items(self):
        cart = ShoppingCart()
        cart.add_item("apple", 1.0, 1)
        cart.add_item("banana", 2.0, 2)
        cart.get_item_count()
        self.assertEqual(cart.get_item_count(), 3)

    def test_get_item_count_edge_case_empty_cart(self):
        cart = ShoppingCart()
        cart.get_item_count()
        self.assertEqual(cart.get_item_count(), 0)

    def test_get_item_count_cumulative_case(self):
        cart = ShoppingCart()
        cart.add_item("apple", 1.0, 1)
        cart.get_item_count()
        cart.add_item("banana", 2.0, 2)
        cart.get_item_count()
        self.assertEqual(cart.get_item_count(), 3)

if __name__ == '__main__':
    unittest.main()

class test_subtotal_function(unittest.TestCase):
    def test_subtotal_normal_case_single_item(self):
        cart = ShoppingCart()
        cart.add_item("apple", 1.0, 1)
        cart._subtotal()
        self.assertEqual(cart._subtotal(), 1.0)

    def test_subtotal_normal_case_multiple_item(self):
        cart = ShoppingCart()
        cart.add_item("apple", 1.0, 1)
        cart.add_item("banana", 2.0, 2)
        cart._subtotal()
        self.assertEqual(cart._subtotal(), 5.0)

    def test_subtotal_edge_case_empty_cart(self):
        cart = ShoppingCart()

        cart._subtotal()
        self.assertEqual(cart._subtotal(), 0.0)

    def test_subtotal_cumulative_case(self):
        cart = ShoppingCart()
        cart.add_item("apple", 1.0, 1)
        cart._subtotal()
        cart.add_item("banana", 2.0, 2)
        cart._subtotal()
        self.assertEqual(cart._subtotal(), 5.0)

if __name__ == '__main__':
    unittest.main()
