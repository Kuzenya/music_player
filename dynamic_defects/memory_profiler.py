"""Запуск сценария с анализом памяти через tracemalloc."""

import argparse
import tracemalloc

from analysis_runner import run_scenario


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scenario",
        choices=("baseline", "memory", "performance"),
        default="baseline",
    )
    parser.add_argument("--iterations", type=int, default=20_000)
    args = parser.parse_args()

    tracemalloc.start()
    before = tracemalloc.take_snapshot()
    _scenario_result = run_scenario(args.scenario, args.iterations)
    current, peak = tracemalloc.get_traced_memory()
    after = tracemalloc.take_snapshot()

    print(f"Текущая отслеживаемая память: {current / 1024:.1f} КиБ")
    print(f"Пиковая отслеживаемая память: {peak / 1024:.1f} КиБ")
    print("\nНаибольшие различия по распределению памяти:")
    for stat in after.compare_to(before, "lineno")[:10]:
        print(stat)
    tracemalloc.stop()


if __name__ == "__main__":
    main()
