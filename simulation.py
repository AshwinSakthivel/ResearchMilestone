"""Deterministic mock federated-learning results for the research prototype."""

from dataclasses import dataclass


@dataclass(frozen=True)
class RoundResult:
    round_number: int
    accuracy: float
    loss: float


@dataclass(frozen=True)
class SimulationResult:
    display_name: str
    hospital_count: int
    rounds: tuple[RoundResult, ...]
    hospital_statuses: tuple[tuple[str, str], ...]

    @property
    def final_accuracy(self) -> float:
        return self.rounds[-1].accuracy

    @property
    def final_loss(self) -> float:
        return self.rounds[-1].loss


def run_mock_simulation(
    display_name: str, hospital_count: int, training_rounds: int, simulate_dropout: bool
) -> SimulationResult:
    """Create repeatable results that react to the user's selected settings."""
    active_hospitals = hospital_count - int(simulate_dropout)
    base_accuracy = 0.61 + (hospital_count - 3) * 0.015 - int(simulate_dropout) * 0.025
    base_loss = 0.78 + int(simulate_dropout) * 0.08

    rounds = tuple(
        RoundResult(
            round_number=round_number,
            accuracy=min(0.94, base_accuracy + round_number * 0.024),
            loss=max(0.12, base_loss - round_number * 0.062),
        )
        for round_number in range(1, training_rounds + 1)
    )

    statuses = []
    for index in range(1, hospital_count + 1):
        dropped_out = simulate_dropout and index == hospital_count
        status = "Dropped out (simulated)" if dropped_out else "Participated"
        statuses.append((f"Hospital {index}", status))

    assert active_hospitals >= 2
    return SimulationResult(
        display_name=display_name,
        hospital_count=hospital_count,
        rounds=rounds,
        hospital_statuses=tuple(statuses),
    )

