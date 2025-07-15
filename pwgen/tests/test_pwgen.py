import unittest
import string
from pwgen import pwgen

class TestPwgen(unittest.TestCase):
    def test_generate_password_length(self):
        """Test if the generated password has the correct length."""
        length = 12
        char_groups = (string.ascii_lowercase, string.digits)
        password = pwgen.generate_password(length, char_groups)
        self.assertEqual(len(password), length)

    def test_generate_password_char_groups(self):
        """Test if the generated password contains at least one character from each specified character group."""
        length = 12
        char_groups = (string.ascii_lowercase, string.ascii_uppercase, string.digits)
        password = pwgen.generate_password(length, char_groups)
        for group in char_groups:
            self.assertTrue(any(c in group for c in password))

    def test_generate_and_print_passwords_value_error(self):
        """Test if it raises a `ValueError` when the requested password length is less than the number of character groups."""
        length = 2
        char_groups = (string.ascii_lowercase, string.ascii_uppercase, string.digits)
        count = 1
        with self.assertRaises(ValueError):
            pwgen.generate_and_print_passwords(length, char_groups, count)

    def test_generate_and_print_passwords_count(self):
        """Test if it prints the correct number of passwords."""
        import io
        from contextlib import redirect_stdout

        length = 12
        char_groups = (string.ascii_lowercase, string.digits)
        count = 5

        f = io.StringIO()
        with redirect_stdout(f):
            pwgen.generate_and_print_passwords(length, char_groups, count)

        output = f.getvalue()
        self.assertEqual(len(output.strip().split('\n')), count)

    def test_main_function(self):
        """Test if it calls `generate_and_print_passwords` with the correct arguments based on the command-line arguments."""
        import sys
        from unittest import mock

        with mock.patch('pwgen.pwgen.generate_and_print_passwords') as mock_generate:
            sys.argv = ['pwgen.py', '-t', 'simple', '-l', '8', '-c', '3']
            pwgen.main()
            mock_generate.assert_called_once_with(8, (string.ascii_lowercase,), 3)

if __name__ == '__main__':
    unittest.main()
