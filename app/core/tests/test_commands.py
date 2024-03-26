"""
test_commands.py: Tests for the custom commands I create
"""
from unittest.mock import patch

from psycopg import OperationalError as PsycopgError

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


@patch('core.management.commands.await_db.Command.check')
class TestCommand(TestCase):
    """Unit test for the custom command"""

    def test_command_called_with_DB(self, patched_check):
        patched_check.return_value = True

        call_command('await_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_command_waits_until_DB_ready(self, patched_timer, patched_check):
        patched_check.side_effect = [OperationalError] * 4 \
                                    + [PsycopgError] * 3 + [True]

        call_command('await_db')

        self.assertEqual(patched_check.call_count, 8)
        patched_check.assert_called_with(databases=['default'])
