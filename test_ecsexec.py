import unittest
from unittest.mock import patch, MagicMock
import sys

# Import the module; ensure the module is named ecsexec.py and is in the PYTHONPATH.
import ecsexec

class TestEcsExec(unittest.TestCase):
    @patch("ecsexec.subprocess.run")
    def test_get_aws_profiles(self, mock_run):
        mock_run.return_value.stdout = "default\nprod\n"
        profiles = ecsexec.get_aws_profiles()
        self.assertEqual(profiles, ["default", "prod"])

    @patch("ecsexec.interactive_selection", return_value="default")
    @patch("ecsexec.get_aws_profiles", return_value=["default", "prod"])
    def test_profile_selection(self, mock_get_profiles, mock_interactive):
        profiles = ecsexec.get_aws_profiles()
        selected = ecsexec.interactive_selection(profiles, "Choose an AWS profile:")
        self.assertEqual(selected, "default")

    @patch("ecsexec.boto3.Session")
    def test_get_boto3_session_success(self, mock_session):
        session_instance = MagicMock()
        mock_session.return_value = session_instance
        session = ecsexec.get_boto3_session("default", "us-west-2")
        self.assertEqual(session, session_instance)

    @patch("ecsexec.which", return_value=None)
    def test_check_session_manager_plugin_missing(self, mock_which):
        with self.assertRaises(SystemExit):
            ecsexec.check_session_manager_plugin()

    @patch("ecsexec.which", return_value="/usr/local/bin/session-manager-plugin")
    def test_check_session_manager_plugin_present(self, mock_which):
        # Should not exit
        ecsexec.check_session_manager_plugin()

if __name__ == "__main__":
    unittest.main()
