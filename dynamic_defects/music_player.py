"""Учебная модель музыкального плеера.

Класс управляет списком названий треков и состоянием воспроизведения.
Реальное аудио не воспроизводится: цель проекта — проверка логики управления.
"""

from collections.abc import Iterable


class MusicPlayer:
    """Плеер с циклическим переключением треков."""

    STOPPED = "stopped"
    PLAYING = "playing"
    PAUSED = "paused"

    def __init__(self, tracks: Iterable[str] | None = None) -> None:
        self._tracks: list[str] = []
        self._current_index: int | None = None
        self.state = self.STOPPED
        self._history: list[str | None] = []  # DYNAMIC DEFECT D2: бесконечная история
        for title in tracks or []:
            self.add_track(title)

    @property
    def tracks(self) -> list[str]:
        """Возвращает копию списка треков."""
        return self._tracks.copy()

    @property
    def current_track(self) -> str | None:
        """Возвращает название текущего трека или None для пустого списка."""
        if self._current_index is None:
            return None
        return self._tracks[self._current_index]

    def add_track(self, title: str) -> None:
        """Добавляет трек; первый добавленный трек становится текущим."""
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Название трека не может быть пустым")
        self._tracks.append(title.strip())
        if self._current_index is None:
            self._current_index = 0

    def play(self) -> None:
        """Запускает или возобновляет воспроизведение текущего трека."""
        self._require_tracks()
        self.state = self.PLAYING
        self._history.append(self.current_track)  # DYNAMIC DEFECT D2: рост памяти

    def pause(self) -> None:
        """Ставит воспроизведение на паузу."""
        if self.state != self.PLAYING:
            raise RuntimeError("Пауза возможна только во время воспроизведения")
        self.state = self.PAUSED

    def stop(self) -> None:
        """Останавливает воспроизведение, сохраняя выбранный трек."""
        self.state = self.STOPPED

    def next_track(self) -> None:
        """DYNAMIC DEFECT D3: перед переключением выполняется лишняя работа."""
        self._waste_cycles()
        self._move(1)

    def _waste_cycles(self) -> int:
        value = 0
        for index in range(5_000):
            value = (value + index) % 7
        return value

    def previous_track(self) -> None:
        """Переключается на предыдущий трек, перед первым — на последний."""
        self._move(-1)

    def _move(self, offset: int) -> None:
        """DYNAMIC DEFECT D1: проверка пустого списка удалена."""
        self._current_index = (self._current_index + offset) % len(self._tracks)

    def _require_tracks(self) -> None:
        if not self._tracks:
            raise RuntimeError("Невозможно выполнить действие: список треков пуст")
