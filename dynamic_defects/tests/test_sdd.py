import unittest

from music_player import MusicPlayer


class MusicPlayerSpecificationTests(unittest.TestCase):
    """Автоматизация таблицы примеров Specification by Example."""

    def test_examples_from_specification_table(self):
        examples = [
            {
                "name": "запуск первого трека",
                "tracks": ["A", "B", "C"],
                "actions": ["play"],
                "track": "A",
                "state": "playing",
            },
            {
                "name": "переход ко второму треку",
                "tracks": ["A", "B", "C"],
                "actions": ["play", "next"],
                "track": "B",
                "state": "playing",
            },
            {
                "name": "циклический переход к первому треку",
                "tracks": ["A", "B", "C"],
                "actions": ["play", "next", "next", "next"],
                "track": "A",
                "state": "playing",
            },
            {
                "name": "пауза сохраняется при переключении",
                "tracks": ["A", "B", "C"],
                "actions": ["play", "pause", "next"],
                "track": "B",
                "state": "paused",
            },
            {
                "name": "переход назад с первого на последний",
                "tracks": ["A", "B", "C"],
                "actions": ["previous"],
                "track": "C",
                "state": "stopped",
            },
        ]

        for example in examples:
            with self.subTest(example=example["name"]):
                player = MusicPlayer(example["tracks"])
                for action in example["actions"]:
                    if action == "play":
                        player.play()
                    elif action == "pause":
                        player.pause()
                    elif action == "next":
                        player.next_track()
                    elif action == "previous":
                        player.previous_track()
                    else:
                        self.fail(f"Неизвестное действие: {action}")
                self.assertEqual(player.current_track, example["track"])
                self.assertEqual(player.state, example["state"])

    def test_empty_playlist_examples(self):
        for action in ("play", "next", "previous"):
            with self.subTest(action=action):
                player = MusicPlayer([])
                with self.assertRaisesRegex(RuntimeError, "список треков пуст"):
                    getattr(player, {"next": "next_track", "previous": "previous_track"}.get(action, action))()
                self.assertEqual(player.state, "stopped")
                self.assertIsNone(player.current_track)


if __name__ == "__main__":
    unittest.main()
