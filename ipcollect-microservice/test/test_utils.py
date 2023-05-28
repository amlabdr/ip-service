import unittest
from unittest.mock import patch

from utils.common import xml_preprocessing
from utils.common import flatten_nested_list

class TestUtils(unittest.TestCase):
    
    def test_xml_preprocessing(self):
        # Define the test XML string
        xml_string = '''
            <ns0:rpc-reply xmlns:ns0="http://example.com">
                <data>
                    <foo>Foo Value</foo>
                    <bar>Bar Value</bar>
                </data>
            </ns0:rpc-reply>
        '''
        result = xml_preprocessing(xml_string)

        # Define the expected output
        expected_result = {
            'foo': 'Foo Value',
            'bar': 'Bar Value'
        }

        self.assertEqual(result, expected_result)

    def test_flatten_nested_list(self):
        test_list = [1, [2, 3, [4, 5]], 6, [7, [8, [9, 10]]]]
        result = flatten_nested_list(test_list)
        expected_result = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
