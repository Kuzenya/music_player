"""Сценарии нагрузки для динамического анализа Music Player."""

import argparse

from music_player import MusicPlayer


def run_scenario(scenario: str, iterations: int) -> MusicPlayer | None:
    if scenario == "exception":
        # В исходной версии здесь корректно возникает RuntimeError.
        # В dynamic_defects из-за удалённой проверки возникает TypeError.
        MusicPlayer().next_track()
        return

    player = MusicPlayer(["Track A", "Track B", "Track C"])

    if scenario == "baseline":
        for index in range(iterations):
            player.play()
            if index % 2 == 0:
                player.pause()
            player.next_track()
            if index % 3 == 0:
                player.previous_track()
    elif scenario == "memory":
        for _ in range(iterations):
            player.play()
    elif scenario == "performance":
        for _ in range(iterations):
            player.next_track()
    else:
        raise ValueError(f"Неизвестный сценарий: {scenario}")

    print(
        f"Сценарий: {scenario}; итераций: {iterations}; "
        f"состояние: {player.state}; трек: {player.current_track}"
    )
    return player


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scenario",
        choices=("baseline", "exception", "memory", "performance"),
        default="baseline",
    )
    parser.add_argument("--iterations", type=int, default=20_000)
    args = parser.parse_args()
    if args.iterations < 1:
        parser.error("--iterations должно быть положительным")
    run_scenario(args.scenario, args.iterations)


if __name__ == "__main__":
    main()
