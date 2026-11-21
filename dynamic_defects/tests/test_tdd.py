import unittest

from music_player import MusicPlayer


class MusicPlayerTDDTests(unittest.TestCase):
    """Юнит-тесты, написанные до реализации класса MusicPlayer."""

    def setUp(self):
        self.player = MusicPlayer(["Track A", "Track B", "Track C"])

    def test_initial_state(self):
        self.assertEqual(self.player.state, "stopped")
        self.assertEqual(self.player.current_track, "Track A")

    def test_play_starts_current_track(self):
        self.player.play()
        self.assertEqual(self.player.state, "playing")
        self.assertEqual(self.player.current_track, "Track A")

    def test_pause_changes_state(self):
        self.player.play()
        self.player.pause()
        self.assertEqual(self.player.state, "paused")
        self.assertEqual(self.player.current_track, "Track A")

    def test_resume_after_pause(self):
        self.player.play()
        self.player.pause()
        self.player.play()
        self.assertEqual(self.player.state, "playing")

    def test_pause_is_rejected_when_not_playing(self):
        with self.assertRaisesRegex(RuntimeError, "только во время"):
            self.player.pause()

    def test_play_is_rejected_for_empty_playlist(self):
        player = MusicPlayer()
        with self.assertRaisesRegex(RuntimeError, "список треков пуст"):
            player.play()

    def test_next_track_selects_next_and_keeps_playing(self):
        self.player.play()
        self.player.next_track()
        self.assertEqual(self.player.current_track, "Track B")
        self.assertEqual(self.player.state, "playing")

    def test_next_track_wraps_to_first(self):
        self.player.next_track()
        self.player.next_track()
        self.player.next_track()
        self.assertEqual(self.player.current_track, "Track A")

    def test_previous_track_wraps_to_last(self):
        self.player.previous_track()
        self.assertEqual(self.player.current_track, "Track C")
        self.assertEqual(self.player.state, "stopped")

    def test_switching_is_rejected_for_empty_playlist(self):
        player = MusicPlayer()
        with self.assertRaisesRegex(RuntimeError, "список треков пуст"):
            player.next_track()

    def test_add_first_track_selects_it(self):
        player = MusicPlayer()
        player.add_track("New track")
        self.assertEqual(player.current_track, "New track")
        self.assertEqual(player.state, "stopped")

    def test_blank_track_title_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "не может быть пустым"):
            self.player.add_track("   ")

    def test_stop_stops_playback_without_changing_track(self):
        self.player.play()
        self.player.next_track()
        self.player.stop()
        self.assertEqual(self.player.state, "stopped")
        self.assertEqual(self.player.current_track, "Track B")


if __name__ == "__main__":
    unittest.main()
