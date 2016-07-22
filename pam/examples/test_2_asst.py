import unittest
import pep8  # from the current directory

# It is necessary to import the student files this way.
try:
    import asstfile
except Exception:
    pass

class TestRemoveDigits(unittest.TestCase):
    def test_empty_string(self):
        '''Testing remove_digits() with an empty string.
        '''

        self.assertEqual(asstfile.remove_digits(''),
                         '', 
                         'Removing digits from the empty string should result in the empty string.')

    def test_no_digits(self):
        '''Testing remove_digits() with a string containing no digits.
        '''

        self.assertEqual(asstfile.remove_digits('nope, there really aren\'t any digits here.'), 
                         'nope, there really aren\'t any digits here.', 
                         'Removing digits from a string with no digits should result in the identical string.')

    def test_several_digits(self):
        '''Testing remove_digits() with a string containing multiple digits.
        '''

        self.assertEqual(asstfile.remove_digits('m435345u34534lti543543pl345e3 45d345i3g4534i5ts345'),
                         'multiple digits', 
                         'Removing digits from a string with multiple digits should result in a string with every digit removed.')


class TestStyleAndDocstrings(unittest.TestCase):
    def test_pep8(self):
        ''' Testing for style (PEP-8) conformity.
        '''

        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(['asstfile.py'])

        report_output = "Found code style errors (and warnings):"

        for code in result.messages:
            message = result.messages[code]
            count = result.counters[code]

            report_output += "\n" + code + ": " + message + " (" + str(count) + ")"

        self.assertEqual(result.total_errors, 0, report_output)

if __name__ == '__main__':
    unittest.main()
