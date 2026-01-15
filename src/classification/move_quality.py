import typing
from enum import Enum

"""
Move quality classification.
Rules:
    - Mate evaluations dominate centipawn logic.
    - Stockfish evaluations are White-relative.
    - Returned quality is relative to the mover.
"""


class MoveQuality(str, Enum):
    BEST = "best"
    GOOD = "good"
    INACCURACY = "inaccuracy"
    MISTAKE = "mistake"
    BLUNDER = "blunder"


def mate_favors_side(mate_value: int, side: typing.Literal["w", "b"]) -> bool:
    """
    Returns True if the mate favors the given side.
    Stockfish mate is always White-relative.
    """
    if side == "w":
        return mate_value > 0
    else:
        return mate_value < 0


def classify_mate(
    eval_before: dict[str, typing.Any],
    eval_after: dict[str, typing.Any],
    side_to_move: typing.Literal["w", "b"],
) -> MoveQuality | None:
    before_is_mate = eval_before["type"] == "mate"
    after_is_mate = eval_after["type"] == "mate"

    # Case 1: No mate involved at all
    if not before_is_mate and not after_is_mate:
        return None

    # Case 2: Escaped mate
    if before_is_mate and not after_is_mate:
        # We were getting mated and escaped
        if not mate_favors_side(eval_before["value"], side_to_move):
            return MoveQuality.BEST
        # We threw away our own mate
        return MoveQuality.BLUNDER

    # Case 3: Entered mate
    if not before_is_mate and after_is_mate:
        if mate_favors_side(eval_after["value"], side_to_move):
            return MoveQuality.BEST
        return MoveQuality.BLUNDER

    # Case 4: Mate before and after
    before_favors = mate_favors_side(eval_before["value"], side_to_move)
    after_favors = mate_favors_side(eval_after["value"], side_to_move)

    # Still winning mate
    if before_favors and after_favors:
        return MoveQuality.BEST

    # Lost winning mate
    if before_favors and not after_favors:
        return MoveQuality.BLUNDER

    # Still getting mated
    if not before_favors and not after_favors:
        return MoveQuality.BLUNDER

    # Switched from getting mated to mating
    return MoveQuality.BEST


def classify_cp_delta(delta: int | None) -> MoveQuality:
    # delta is None only when mate logic applies (handled above)
    if delta is None:
        return MoveQuality.BLUNDER

    if delta >= 50:
        return MoveQuality.GOOD
    elif delta >= -20:
        return MoveQuality.INACCURACY
    elif delta >= -100:
        return MoveQuality.MISTAKE
    else:
        return MoveQuality.BLUNDER


def classify_move(
    analysis: dict[str, typing.Any], side_to_move: typing.Literal["w", "b"]
) -> MoveQuality:
    mate_result = classify_mate(analysis["before"], analysis["after"], side_to_move)
    if mate_result:
        return mate_result

    return classify_cp_delta(analysis["delta"])
