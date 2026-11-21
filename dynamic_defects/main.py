"""Простой консольный интерфейс учебного музыкального плеера."""

import sys

from music_player import MusicPlayer


HELP = """Команды:
  list             — показать список треков
  play             — начать или продолжить воспроизведение
  pause            — поставить на паузу
  next             — следующий трек
  prev             — предыдущий трек
  stop             — остановить воспроизведение
  add <название>   — добавить трек
  status           — показать состояние
  help             — показать справку
  quit             — выйти
"""


def show_status(player: MusicPlayer) -> None:
    print(f"Состояние: {player.state}; текущий трек: {player.current_track or '—'}")


def show_tracks(player: MusicPlayer) -> None:
    if not player.tracks:
        print("Список треков пуст.")
        return
    for number, title in enumerate(player.tracks, start=1):
        marker = "→" if title == player.current_track else " "
        print(f"{marker} {number}. {title}")


def run_demo() -> None:
    """Небольшой невзаимодействующий пример для проверки программы."""
    player = MusicPlayer(["Track A", "Track B", "Track C"])
    show_tracks(player)
    for action in (player.play, player.next_track, player.pause, player.play):
        action()
        show_status(player)


def main() -> None:
    player = MusicPlayer(["Track A", "Track B", "Track C"])
    print("Учебный музыкальный плеер. Введите help для списка команд.")
    show_status(player)

    while True:
        try:
            command = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nВыход.")
            break

        if not command:
            continue
        name, _, argument = command.partition(" ")
        name = name.lower()

        try:
            if name == "quit":
                print("Выход.")
                break
            if name == "help":
                print(HELP)
            elif name == "list":
                show_tracks(player)
            elif name == "play":
                player.play()
                show_status(player)
            elif name == "pause":
                player.pause()
                show_status(player)
            elif name == "next":
                player.next_track()
                show_status(player)
            elif name == "prev":
                player.previous_track()
                show_status(player)
            elif name == "stop":
                player.stop()
                show_status(player)
            elif name == "add":
                player.add_track(argument)
                print(f"Добавлен трек: {argument.strip()}")
            elif name == "status":
                show_status(player)
            else:
                print("Неизвестная команда. Введите help.")
        except (RuntimeError, ValueError) as error:
            print(f"Ошибка: {error}")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        run_demo()
    else:
        main()
