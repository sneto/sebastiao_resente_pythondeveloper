import io
import unittest
import unittest.mock

from src import main


class TestGetLineIntegerListMethod(unittest.TestCase):
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_none_input(self, mock_stdout):
        """
        Test if none input is correctly validated
        """
        data = None
        result = main.get_line_integer_list(data)
        self.assertIsNone(result)
        self.assertEqual(mock_stdout.getvalue(), 'Line must not be empty\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_not_list_input(self, mock_stdout):
        """
        Test if an input of type different of list is correctly validated
        """
        data = 10
        result = main.get_line_integer_list(data)
        self.assertIsNone(result)
        self.assertEqual(mock_stdout.getvalue(), 'Line must be two integers list\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_empty_list_input(self, mock_stdout):
        """
        Test if an input of empty lists is correctly validated
        """
        data = []
        result = main.get_line_integer_list(data)
        self.assertIsNone(result)
        self.assertEqual(mock_stdout.getvalue(), 'Line must have two values coma separated\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_one_item_list_input(self, mock_stdout):
        """
        Test if an input of list with only one item is correctly validated
        """
        data = ['10']
        result = main.get_line_integer_list(data)
        self.assertIsNone(result)
        self.assertEqual(mock_stdout.getvalue(), 'Line must have two values coma separated\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_three_item_list_input(self, mock_stdout):
        """
        Test if an input of list with three items is correctly validated
        """
        data = ['10', '5', '6']
        result = main.get_line_integer_list(data)
        self.assertIsNone(result)
        self.assertEqual(mock_stdout.getvalue(), 'Line must have two values coma separated\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_equal_items_input(self, mock_stdout):
        """
        Test if an input of equal items is correctly validated
        """
        data = ['10', '10']
        result = main.get_line_integer_list(data)
        self.assertIsNone(result)
        self.assertEqual(mock_stdout.getvalue(), 'Line must have two different integer values\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_two_items_not_integer_input(self, mock_stdout):
        """
        Test if an input of two not integer items is correctly validated
        """
        data = ['10', 'a10']
        result = main.get_line_integer_list(data)
        self.assertIsNone(result)
        self.assertEqual(mock_stdout.getvalue(), 'All values in line must be valid integers\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_two_unsorted_items_input(self, mock_stdout):
        """
        Test if an input of two unsorted items is returned ordered and converted to integer
        """
        data = ['15', '10']
        result = main.get_line_integer_list(data)
        self.assertEqual(result, [10, 15])
        self.assertEqual(mock_stdout.getvalue(), '')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_two_sorted_items_input(self, mock_stdout):
        """
        Test if an input of two sorted items is returned correctly (ordered and converted to integer)
        """
        data = ['10', '15']
        result = main.get_line_integer_list(data)
        self.assertEqual(result, [10, 15])
        self.assertEqual(mock_stdout.getvalue(), '')


class TestValidateAndConvertInputMethod(unittest.TestCase):
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_none_input(self, mock_stdout):
        """
        Test if None input is correctly validated
        """
        data = None
        result = main.validate_and_convert_input(data)
        self.assertIsNone(result)
        self.assertEqual(mock_stdout.getvalue(), 'Input lines must not be null\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_empty_array(self, mock_stdout):
        """
        Test if empty array input is correctly validated
        """
        data = []
        result = main.validate_and_convert_input(data)
        self.assertIsNone(result)
        self.assertEqual(mock_stdout.getvalue(), 'Input lines must not be empty array\n')

    def test_invalid_item_in_array(self):
        """
        Test if invalid item in input is correctly validated
        """
        data = ["12", "10,5"]
        result = main.validate_and_convert_input(data)
        self.assertFalse(result)

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_empty_item_in_array(self, mock_stdout):
        """
        Test if empty item in array input is correctly validated
        """
        data = ["12,6", None]
        result = main.validate_and_convert_input(data)
        self.assertFalse(result)
        self.assertEqual(mock_stdout.getvalue(), 'Lines must not be empty\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_valid_input(self, mock_stdout):
        """
        Test if empty item in array input is correctly validated
        """
        data = ["12,6", "5,6"]
        result = main.validate_and_convert_input(data)
        self.assertEqual(result, [[6, 12], [5, 6]])
        self.assertEqual(mock_stdout.getvalue(), '')


class TestCheckOverlappingMethod(unittest.TestCase):
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_first_and_second_none_input(self, mock_stdout):
        """
        Test if None input is correctly validated for two lines
        """
        result = main.check_overlapping(None, None)
        self.assertFalse(result)
        self.assertEqual(mock_stdout.getvalue(), 'First and second line must not be None\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_first_none_input(self, mock_stdout):
        """
        Test if None input is correctly validated for first line
        """
        result = main.check_overlapping(None, [10, 5])
        self.assertFalse(result)
        self.assertEqual(mock_stdout.getvalue(), 'First and second line must not be None\n')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_second_none_input(self, mock_stdout):
        """
        Test if None input is correctly validated for second line
        """
        result = main.check_overlapping([10, 5], None)
        self.assertFalse(result)
        self.assertEqual(mock_stdout.getvalue(), 'First and second line must not be None\n')

    def test_overlap(self):
        """
        Test two lines that must overlap
        """
        result = main.check_overlapping([1, 5], [2, 6])
        self.assertTrue(result)

    def test_not_overlap(self):
        """
        Test two lines that must not overlap
        """
        result = main.check_overlapping([1, 5], [6, 8])
        self.assertFalse(result)

    def test_overlap_negative(self):
        """
        Test two lines that must overlap
        """
        result = main.check_overlapping([-5, -1], [-6, -2])
        self.assertTrue(result)

    def test_not_overlap_negative(self):
        """
        Test two lines that must not overlap
        """
        result = main.check_overlapping([-1, -5], [-6, -8])
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()