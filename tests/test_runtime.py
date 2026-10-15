import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import bot


class RuntimeTests(unittest.IsolatedAsyncioTestCase):
    async def test_start_displays_menu_and_preserves_user(self):
        message = SimpleNamespace(
            from_user=SimpleNamespace(id=247126354, username="sinov"),
            answer=AsyncMock(),
        )
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(bot, "DB", Path(directory) / "test.db"):
                await bot.start(message)
                await bot.start(message)
                with bot.db() as connection:
                    users = connection.execute("SELECT id FROM users").fetchall()
                self.assertEqual([row["id"] for row in users], [247126354])

        answer = message.answer.call_args
        self.assertIn("Sizga nima kerak?", answer.args[0])
        labels = [button.text for row in answer.kwargs["reply_markup"].keyboard for button in row]
        self.assertIn("🆓 Bepul materiallar", labels)
        self.assertIn("📝 Test ishlash", labels)

    async def test_unconfigured_mini_app_does_not_send_invalid_button(self):
        for url in ("", "http://localhost:8000", "https://"):
            with self.subTest(url=url), patch.object(bot, "WEBAPP_URL", url):
                message = SimpleNamespace(answer=AsyncMock())
                await bot.tests(message)
                self.assertIn("tayyorlanmoqda", message.answer.call_args.args[0])
                self.assertNotIn("reply_markup", message.answer.call_args.kwargs)

    async def test_https_mini_app_sends_configured_url(self):
        with patch.object(bot, "WEBAPP_URL", "https://example.com/test"):
            message = SimpleNamespace(answer=AsyncMock())
            await bot.tests(message)
        markup = message.answer.call_args.kwargs["reply_markup"]
        self.assertEqual(markup.inline_keyboard[0][0].web_app.url, "https://example.com/test")

    async def test_missing_token_stops_before_polling(self):
        with patch.object(bot, "TOKEN", ""), patch.object(bot.dp, "start_polling", new_callable=AsyncMock) as polling:
            with self.assertRaisesRegex(RuntimeError, "BOT_TOKEN"):
                await bot.main()
            polling.assert_not_called()


if __name__ == "__main__":
    unittest.main()
