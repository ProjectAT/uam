import unittest
import pep8  # from the current directory

# It is necessary to import the student files this way.
try:
    import asstfile
except Exception:
    pass

class TestCallHelperModule(unittest.TestCase):
    def test_helper(self):
        ''' Testing function call to student helper module.'''

        self.assertEqual(asstfile.call_helper(), 42, 'I was expecting 42.')

    def test_math(self):
        ''' Testing function call to math module.'''

        self.assertAlmostEqual(asstfile.call_math(), 3.1419, 2, 'I was expecting PI.')


class TestCountLetter(unittest.TestCase):
    def test_empty_string(self):
        ''' Testing count_letter() with an empty string.
        '''

        self.assertEqual(asstfile.count_letter('', 'x'), 0,
                         'Searching for anything (in this case, \'x\') in the empty string should return no matches.')

    def test_several_matches(self):
        ''' Testing count_letter() with multiple occurrences.
        '''

        self.assertEqual(asstfile.count_letter('catastrophic', 'c'), 2,
                         'There are 2 occurrences of \'c\' in \'catastrophic\'.')

    def test_single_match(self):
        ''' Testing count_letter() with a single occurrence.
        '''

        self.assertEqual(asstfile.count_letter('single', 'i'), 1,
                         'There is exactly a single occurrence of \'i\' in \'single\'.')

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
