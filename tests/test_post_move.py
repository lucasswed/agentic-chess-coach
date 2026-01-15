from unittest.mock import Mock, patch

import pytest

from src.pipelines.post_move import analyze_post_move, calculate_delta, get_side_to_move


class TestGetSideToMove:
    def test_white_to_move(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        assert get_side_to_move(fen) == "w"

    def test_black_to_move(self):
        fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
        assert get_side_to_move(fen) == "b"


class TestCalculateDelta:
    def test_delta_white_to_move_improvement(self):
        eval_before = {"type": "cp", "value": 50}
        eval_after = {"type": "cp", "value": 100}
        delta = calculate_delta(eval_before, eval_after, "w")
        assert delta == 50

    def test_delta_white_to_move_decline(self):
        eval_before = {"type": "cp", "value": 100}
        eval_after = {"type": "cp", "value": 50}
        delta = calculate_delta(eval_before, eval_after, "w")
        assert delta == -50

    def test_delta_black_to_move_improvement(self):
        eval_before = {"type": "cp", "value": 50}
        eval_after = {"type": "cp", "value": 100}
        delta = calculate_delta(eval_before, eval_after, "b")
        assert delta == -50

    def test_delta_black_to_move_decline(self):
        eval_before = {"type": "cp", "value": 100}
        eval_after = {"type": "cp", "value": 50}
        delta = calculate_delta(eval_before, eval_after, "b")
        assert delta == 50

    def test_delta_with_mate_before(self):
        eval_before = {"type": "mate", "value": 1}
        eval_after = {"type": "cp", "value": 100}
        delta = calculate_delta(eval_before, eval_after, "w")
        assert delta is None

    def test_delta_with_mate_after(self):
        eval_before = {"type": "cp", "value": 100}
        eval_after = {"type": "mate", "value": 3}
        delta = calculate_delta(eval_before, eval_after, "w")
        assert delta is None

    def test_delta_with_mate_both(self):
        eval_before = {"type": "mate", "value": 5}
        eval_after = {"type": "mate", "value": 3}
        delta = calculate_delta(eval_before, eval_after, "w")
        assert delta is None


class TestAnalyzePostMove:
    @patch("src.pipelines.post_move.Stockfish")
    def test_analyze_valid_move_white(self, mock_stockfish_class):
        # Setup mock
        mock_engine = Mock()
        mock_stockfish_class.return_value = mock_engine
        mock_engine.is_fen_valid.return_value = True
        mock_engine.get_evaluation.side_effect = [
            {"type": "cp", "value": 50},
            {"type": "cp", "value": 100},
        ]

        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        move = "e2e4"

        result = analyze_post_move(fen, move)

        assert result["before"] == {"type": "cp", "value": 50}
        assert result["after"] == {"type": "cp", "value": 100}
        assert result["delta"] == 50
        mock_engine.set_fen_position.assert_called_once_with(fen)
        mock_engine.make_moves_from_current_position.assert_called_once_with([move])

    @patch("src.pipelines.post_move.Stockfish")
    def test_analyze_valid_move_black(self, mock_stockfish_class):
        # Setup mock
        mock_engine = Mock()
        mock_stockfish_class.return_value = mock_engine
        mock_engine.is_fen_valid.return_value = True
        mock_engine.get_evaluation.side_effect = [
            {"type": "cp", "value": 50},
            {"type": "cp", "value": 100},
        ]

        fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
        move = "e7e5"

        result = analyze_post_move(fen, move)

        assert result["before"] == {"type": "cp", "value": 50}
        assert result["after"] == {"type": "cp", "value": 100}
        assert result["delta"] == -50  # Negative because black to move

    @patch("src.pipelines.post_move.Stockfish")
    def test_analyze_invalid_fen(self, mock_stockfish_class):
        # Setup mock
        mock_engine = Mock()
        mock_stockfish_class.return_value = mock_engine
        mock_engine.is_fen_valid.return_value = False

        fen = "invalid_fen"
        move = "e2e4"

        with pytest.raises(ValueError, match="Invalid Fen!"):
            analyze_post_move(fen, move)

    @patch("src.pipelines.post_move.Stockfish")
    def test_analyze_move_with_mate_evaluation(self, mock_stockfish_class):
        # Setup mock
        mock_engine = Mock()
        mock_stockfish_class.return_value = mock_engine
        mock_engine.is_fen_valid.return_value = True
        mock_engine.get_evaluation.side_effect = [
            {"type": "cp", "value": 300},
            {"type": "mate", "value": 1},
        ]

        fen = "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4"
        move = "d1f3"

        result = analyze_post_move(fen, move)

        assert result["before"] == {"type": "cp", "value": 300}
        assert result["after"] == {"type": "mate", "value": 1}
        assert result["delta"] is None

    @patch("src.pipelines.post_move.Stockfish")
    def test_analyze_neutral_move(self, mock_stockfish_class):
        # Setup mock
        mock_engine = Mock()
        mock_stockfish_class.return_value = mock_engine
        mock_engine.is_fen_valid.return_value = True
        mock_engine.get_evaluation.side_effect = [
            {"type": "cp", "value": 50},
            {"type": "cp", "value": 50},
        ]

        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        move = "b1c3"

        result = analyze_post_move(fen, move)

        assert result["delta"] == 0

    @patch("src.pipelines.post_move.Stockfish")
    def test_analyze_blunder_move(self, mock_stockfish_class):
        # Setup mock
        mock_engine = Mock()
        mock_stockfish_class.return_value = mock_engine
        mock_engine.is_fen_valid.return_value = True
        mock_engine.get_evaluation.side_effect = [
            {"type": "cp", "value": 100},
            {"type": "cp", "value": -200},
        ]

        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        move = "f2f3"  # Weak opening move

        result = analyze_post_move(fen, move)

        assert result["delta"] == -300  # Significant decline
