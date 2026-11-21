import unittest

from music_player import MusicPlayer


class MusicPlayerAcceptanceTests(unittest.TestCase):
    """Приёмочные сценарии с точки зрения пользователя плеера."""

    def test_user_can_start_playback(self):
        """Даны загруженные треки; Play; ожидается первый трек и playing."""
        player = MusicPlayer(["Morning", "Rain", "Night"])
        player.play()
        self.assertEqual(player.state, "playing")
        self.assertEqual(player.current_track, "Morning")

    def test_user_can_pause_and_resume(self):
        """Во время воспроизведения пользователь ставит паузу и продолжает."""
        player = MusicPlayer(["Morning", "Rain"])
        player.play()
        player.pause()
        self.assertEqual(player.state, "paused")
        self.assertEqual(player.current_track, "Morning")
        player.play()
        self.assertEqual(player.state, "playing")

    def test_user_can_switch_and_wrap_tracks(self):
        """Пользователь последовательно листает треки и возвращается к первому."""
        player = MusicPlayer(["Morning", "Rain", "Night"])
        player.play()
        player.next_track()
        self.assertEqual(player.current_track, "Rain")
        player.next_track()
        self.assertEqual(player.current_track, "Night")
        player.next_track()
        self.assertEqual(player.current_track, "Morning")
        self.assertEqual(player.state, "playing")

    def test_user_gets_clear_error_for_empty_playlist(self):
        """При пустом списке пользователь получает понятное сообщение."""
        player = MusicPlayer([])
        with self.assertRaisesRegex(RuntimeError, "список треков пуст"):
            player.play()
        self.assertIsNone(player.current_track)
        self.assertEqual(player.state, "stopped")


if __name__ == "__main__":
    unittest.main()
