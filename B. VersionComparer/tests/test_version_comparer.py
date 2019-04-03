import io
import unittest
import unittest.mock

from src import version_comparer


class TestValidateVersionFormatMethod(unittest.TestCase):
    def test_none_input(self):
        """
        Test None version
        """
        data = None
        with self.assertRaises(ValueError) as context:
            version_comparer.validate_version_format(data)

        self.assertEqual('Version must not be None', str(context.exception))

    def test_invalid_type_input(self):
        """
        Test invalid type input
        """
        data = 1

        with self.assertRaises(ValueError) as context:
            version_comparer.validate_version_format(data)

        self.assertEqual('Version must be string', str(context.exception))

    def test_invalid_input(self):
        """
        Test invalid versions
        """
        invalid_versions = [
            'asdf',
            '...',
            '.',
            '.1.3',
            '1.3.',
            '1.3.A',
            'a1.3',
            '1.3.5.a',
        ]

        for invalid_version in invalid_versions:
            result = version_comparer.validate_version_format(invalid_version)
            self.assertFalse(result)

    def test_valid_input(self):
        """
        Test valid versions
        """
        valid_versions = [
            '1',
            '01',
            '000109238',
            '1.2',
            '110.2',
            '088687.12332432',
            '1.2342',
            '1.1234.2.5.7.890.1',
            '123.2.23435',
            '234.23423.3',
            '23234.234234.2342342',
        ]

        for valid_version in valid_versions:
            result = version_comparer.validate_version_format(valid_version)
            self.assertTrue(result)


class TestValidateAndSplitVersionsMethod(unittest.TestCase):
    def test_none_input(self):
        """
        Test None input
        """
        data = None
        with self.assertRaises(ValueError) as context:
            version_comparer.validate_and_split_versions(None, None)

        self.assertEqual('Both versions must not be empty', str(context.exception))

    def test_empty_string_input(self):
        """
        Test empty string input
        """
        with self.assertRaises(ValueError) as context:
            version_comparer.validate_and_split_versions('', '')

        self.assertEqual('Both versions must not be empty', str(context.exception))

    def test_invalid_version_input(self):
        """
        Test invalid version input
        """
        data = ["01.00", "01.01."]
        with self.assertRaises(ValueError) as context:
            version_comparer.validate_and_split_versions(data[0], data[1])

        self.assertEqual('Version "{}" is not valid'.format(data[1]), str(context.exception))

    def test_different_mask(self):
        """
        Test valid input
        """
        data = ["01.00", "01.01.00"]
        with self.assertRaises(ValueError) as context:
            version_comparer.validate_and_split_versions(data[0], data[1])

        self.assertEqual('Versions must have the same format mask', str(context.exception))

    def test_valid_input(self):
        """
        Test valid input
        """
        data = ["01.00", "01.01"]
        result = version_comparer.validate_and_split_versions(data[0], data[1])
        expected_result = [['01','00'],['01','01']]
        self.assertEqual(result, expected_result)


class TestCompareVersionsMethod(unittest.TestCase):
    def test_equals_input(self):
        """
        Test equals version for both versions
        """
        data = [('01.00.00', '01.00.00'),
                ('1', '1'),
                ('01.100.00', '01.100.00'),
                ('1.2', '1.2'),
                ('1.2', '1.02'),
                ('1.02', '1.02'),
                ('20.10.40.203985', '20.10.40.203985')]
        for versions in data:
            first, second = versions
            result = version_comparer.compare_versions(first, second)
            self.assertEqual(result, 0)

    def test_first_greater(self):
        """
        Test when the first version is greater than the second one
        """
        data = [('02.00.00', '01.00.00'),
                ('2', '1'),
                ('01.100.00', '01.99.00'),
                ('1.20', '1.19'),
                ('1.02.08.100', '1.02.07.99'),
                ('20.10.40.203985', '20.10.40.203984')]

        for versions in data:
            first, second = versions
            result = version_comparer.compare_versions(first, second)
            self.assertEqual(result, 1)

    def test_second_greater(self):
        """
        Test when the second version is greater than the first one
        """
        data = [('01.00.00', '02.00.00'),
                ('1', '2'),
                ('01.99.00', '01.100.00'),
                ('1.19', '1.20'),
                ('1.02.07.99', '1.02.08.100'),
                ('20.10.40.203984', '20.10.40.203985')]

        for versions in data:
            first, second = versions
            result = version_comparer.compare_versions(first, second)
            self.assertEqual(result, 2)


if __name__ == '__main__':
    unittest.main()