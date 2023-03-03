import unittest
from unittest.mock import patch
from app import Application, MailSystem

class ApplicationTest(unittest.TestCase):
    @patch.object(Application, 'get_names', return_value=(['William', 'Oliver', 'Henry', 'Liam'], ['William', 'Oliver', 'Henry']))
    def setUp(self, _):
        self.application = Application()
    
    @patch.object(Application, 'get_random_person', side_effect=['William', 'Oliver', 'Henry', 'Liam'])
    @patch.object(MailSystem, 'write', side_effect=lambda name: f'Congrats, {name}!')
    @patch.object(MailSystem, 'send', side_effect=lambda _, context: print(context))
    def test_app(self, m_send, m_write, _):
        next = self.application.select_next_person()
        print(next, 'selected')

        self.assertNotIn(next, ['William', 'Oliver', 'Henry'])
        self.assertEqual(next, 'Liam')

        self.application.notify_selected()

        print()
        print(m_write.call_args_list)
        print(m_send.call_args_list)
        
        self.assertEqual(m_write.call_count, m_send.call_count)

if __name__ == '__main__':
    unittest.main()
