# patch - mock django get_database function (simulating the database being available and not being available)
from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    # What happens when we call the command and the database is already available
    def test_wait_for_db_ready(self):
        """test waiting for db when db is available"""
        # simulate the behavior of django when db is available
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    def test_wait_for_db(self):
        """Test wait for db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
