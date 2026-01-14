import typing

import chess
from stockfish import Stockfish


def analyze_post_move(fen_before: str, move_uci: str) -> dict[str, typing.Any]:
    """
    Deterministic post-move analysis.
    No LLM.
    """
    engine = Stockfish("/usr/games/stockfish")

    if not engine.is_fen_valid(fen_before):
        raise KeyError("Invalid Fen!")

    engine.set_fen_position(fen_before)
    evaluation_before = engine.get_evaluation()
    engine.make_moves_from_current_position([move_uci])
    evaluation_after = engine.get_evaluation()
    return {"before": evaluation_before, "after": evaluation_after}


if __name__ == "__main__":
    print(chess.STARTING_FEN)
    print(analyze_post_move(chess.STARTING_FEN, "e2e4"))
