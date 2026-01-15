import typing

from stockfish import Stockfish


def get_side_to_move(fen: str) -> str:
    fen_splitted = fen.split()
    return fen_splitted[1]


def calculate_delta(
    eval_before: dict[str, typing.Any], eval_after: dict[str, typing.Any], side_to_move: str
) -> int | None:
    # Note: mate evaluations are handled at the classification layer
    if eval_before["type"] == "cp" and eval_after["type"] == "cp":
        delta = eval_after["value"] - eval_before["value"]
        return int(delta) if side_to_move == "w" else int(-delta)
    else:
        return None


# TODO: inject engine instance (avoid reinitialization per call)
def analyze_post_move(fen_before: str, move_uci: str) -> dict[str, typing.Any]:
    """
    Post-move deterministic analysis.
    Contract:
        - Input: fen_before, move_uci
        - Output: before, after, delta
        - Evaluation is mover-relative.
    """

    engine = Stockfish("/usr/games/stockfish")

    if not engine.is_fen_valid(fen_before):
        raise ValueError("Invalid Fen!")

    side_to_move = get_side_to_move(fen_before)

    engine.set_fen_position(fen_before)
    evaluation_before = engine.get_evaluation()
    engine.make_moves_from_current_position([move_uci])
    evaluation_after = engine.get_evaluation()

    delta = calculate_delta(evaluation_before, evaluation_after, side_to_move)

    return {"before": evaluation_before, "after": evaluation_after, "delta": delta}


if __name__ == "__main__":
    print(
        analyze_post_move(
            "rnbqkb1r/pppp1ppp/5n2/4p3/4P3/P6P/1PPP1PP1/RNBQKBNR b KQkq - 0 3", "b8c6"
        )
    )
