"""Unit tests for chatbot_assistant; all Gemini calls are mocked."""
import json
import unittest
from types import SimpleNamespace
from unittest.mock import Mock
import sys
from pathlib import Path

backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# pyrefly: ignore[missing-import]
from chatbot_assistant import ChatbotAssistant


def fake_client(plan):
    client = Mock()
    client.models.generate_content.return_value = SimpleNamespace(text=json.dumps(plan))
    return client


class ChatbotAssistantTests(unittest.TestCase):
    def test_missing_api_key_returns_configuration_error(self):
        assistant = ChatbotAssistant(api_key="", client=None)
        assistant.api_key = None
        assistant.client = None
        result = assistant.handle_message("How do I prepare for interviews?")
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"], "not_configured")

    def test_general_question_returns_ai_reply(self):
        assistant = ChatbotAssistant(client=fake_client({
            "reply": "I can help you practice role-specific interview questions.",
            "action": None, "arguments": {}, "needs_confirmation": False,
        }))
        result = assistant.handle_message("Help me prepare for interviews")
        self.assertTrue(result["ok"])
        self.assertIsNone(result["action"])
        self.assertIn("interview", result["reply"].lower())

    def test_sensitive_action_requires_confirmation_then_executes(self):
        handler = Mock(return_value={"application_id": "APP-1"})
        assistant = ChatbotAssistant(
            client=fake_client({
                "reply": "I can submit this application to the selected job.",
                "action": "submit_job_application",
                "arguments": {"job_id": "job-42"}, "needs_confirmation": False,
            }),
            action_handlers={"submit_job_application": handler},
        )
        proposed = assistant.handle_message("Apply to this job", session_id="user-7")
        self.assertTrue(proposed["requires_confirmation"])
        handler.assert_not_called()
        result = assistant.handle_message(
            "yes", session_id="user-7",
            confirmation_token=proposed["confirmation_token"], confirmed=True,
        )
        self.assertTrue(result["executed"])
        handler.assert_called_once_with(job_id="job-42", session_id="user-7")

    def test_sensitive_action_can_be_cancelled(self):
        handler = Mock()
        assistant = ChatbotAssistant(
            client=fake_client({
                "reply": "I can update your resume visibility.",
                "action": "update_resume_privacy",
                "arguments": {"visibility": "private"}, "needs_confirmation": True,
            }),
            action_handlers={"update_resume_privacy": handler},
        )
        proposed = assistant.handle_message("Make my resume private")
        result = assistant.handle_message(
            "no", confirmation_token=proposed["confirmation_token"], confirmed=False,
        )
        self.assertFalse(result["executed"])
        self.assertIn("Cancelled", result["reply"])
        handler.assert_not_called()

    def test_unknown_action_is_not_executed(self):
        assistant = ChatbotAssistant(client=fake_client({
            "reply": "Do an arbitrary operation.", "action": "delete_everything",
            "arguments": {}, "needs_confirmation": False,
        }))
        result = assistant.handle_message("Do it")
        self.assertIsNone(result["action"])
        self.assertIn("can't perform", result["reply"].lower())

    def test_unconfigured_action_is_not_claimed_as_success(self):
        assistant = ChatbotAssistant(client=fake_client({
            "reply": "I will check your applications.", "action": "get_application_status",
            "arguments": {}, "needs_confirmation": False,
        }))
        result = assistant.handle_message("Check my applications")
        self.assertTrue(result["integration_required"])
        self.assertFalse(result["executed"])

    def test_empty_message_is_rejected(self):
        assistant = ChatbotAssistant(client=fake_client({
            "reply": "ok", "action": None, "arguments": {},
        }))
        result = assistant.handle_message("  ")
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"], "empty_message")

    def test_invalid_model_json_is_handled(self):
        client = Mock()
        client.models.generate_content.return_value = SimpleNamespace(text="{bad json")
        assistant = ChatbotAssistant(client=client)
        result = assistant.handle_message("Hello")
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"], "invalid_model_response")


if __name__ == "__main__":
    unittest.main()
