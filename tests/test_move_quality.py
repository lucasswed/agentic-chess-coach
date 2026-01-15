from src.classification.move_quality import (
    MoveQuality,
    classify_mate,
    classify_move,
    classify_move_by_delta,
    mate_favors_side,
)


class TestMateFavorsSide:
    def test_positive_mate_favors_white(self):
        assert mate_favors_side(3, "w") is True

    def test_negative_mate_favors_black(self):
        assert mate_favors_side(-3, "b") is True

    def test_positive_mate_does_not_favor_black(self):
        assert mate_favors_side(3, "b") is False

    def test_negative_mate_does_not_favor_white(self):
        assert mate_favors_side(-3, "w") is False

    def test_mate_in_one_white(self):
        assert mate_favors_side(1, "w") is True

    def test_mate_in_one_black(self):
        assert mate_favors_side(-1, "b") is True


class TestClassifyMate:
    def test_no_mate_involved(self):
        eval_before = {"type": "cp", "value": 100}
        eval_after = {"type": "cp", "value": 150}
        result = classify_mate(eval_before, eval_after, "w")
        assert result is None

    def test_escaped_mate_best_move(self):
        # White was getting mated, escaped
        eval_before = {"type": "mate", "value": -2}
        eval_after = {"type": "cp", "value": -50}
        result = classify_mate(eval_before, eval_after, "w")
        assert result == MoveQuality.BEST

    def test_threw_away_own_mate_blunder(self):
        # White had mate, threw it away
        eval_before = {"type": "mate", "value": 2}
        eval_after = {"type": "cp", "value": 100}
        result = classify_mate(eval_before, eval_after, "w")
        assert result == MoveQuality.BLUNDER

    def test_black_escaped_mate_best_move(self):
        # Black was getting mated, escaped
        eval_before = {"type": "mate", "value": 2}
        eval_after = {"type": "cp", "value": 50}
        result = classify_mate(eval_before, eval_after, "b")
        assert result == MoveQuality.BEST

    def test_black_threw_away_mate_blunder(self):
        # Black had mate, threw it away
        eval_before = {"type": "mate", "value": -2}
        eval_after = {"type": "cp", "value": -100}
        result = classify_mate(eval_before, eval_after, "b")
        assert result == MoveQuality.BLUNDER

    def test_entered_winning_mate_best_move(self):
        # White entered a winning mate
        eval_before = {"type": "cp", "value": 300}
        eval_after = {"type": "mate", "value": 3}
        result = classify_mate(eval_before, eval_after, "w")
        assert result == MoveQuality.BEST

    def test_entered_losing_mate_blunder(self):
        # White entered a losing mate
        eval_before = {"type": "cp", "value": 100}
        eval_after = {"type": "mate", "value": -2}
        result = classify_mate(eval_before, eval_after, "w")
        assert result == MoveQuality.BLUNDER

    def test_black_entered_winning_mate_best_move(self):
        # Black entered a winning mate
        eval_before = {"type": "cp", "value": -300}
        eval_after = {"type": "mate", "value": -3}
        result = classify_mate(eval_before, eval_after, "b")
        assert result == MoveQuality.BEST

    def test_black_entered_losing_mate_blunder(self):
        # Black entered a losing mate
        eval_before = {"type": "cp", "value": -100}
        eval_after = {"type": "mate", "value": 2}
        result = classify_mate(eval_before, eval_after, "b")
        assert result == MoveQuality.BLUNDER

    def test_still_winning_mate_best_move(self):
        # White still has winning mate
        eval_before = {"type": "mate", "value": 5}
        eval_after = {"type": "mate", "value": 3}
        result = classify_mate(eval_before, eval_after, "w")
        assert result == MoveQuality.BEST

    def test_lost_winning_mate_blunder(self):
        # White lost winning mate
        eval_before = {"type": "mate", "value": 3}
        eval_after = {"type": "mate", "value": -2}
        result = classify_mate(eval_before, eval_after, "w")
        assert result == MoveQuality.BLUNDER

    def test_still_getting_mated_blunder(self):
        # White still getting mated
        eval_before = {"type": "mate", "value": -5}
        eval_after = {"type": "mate", "value": -3}
        result = classify_mate(eval_before, eval_after, "w")
        assert result == MoveQuality.BLUNDER

    def test_switched_from_losing_to_winning_mate_best(self):
        # White switched from getting mated to mating
        eval_before = {"type": "mate", "value": -3}
        eval_after = {"type": "mate", "value": 2}
        result = classify_mate(eval_before, eval_after, "w")
        assert result == MoveQuality.BEST

    def test_black_still_winning_mate(self):
        # Black still has winning mate
        eval_before = {"type": "mate", "value": -5}
        eval_after = {"type": "mate", "value": -3}
        result = classify_mate(eval_before, eval_after, "b")
        assert result == MoveQuality.BEST

    def test_black_lost_winning_mate(self):
        # Black lost winning mate
        eval_before = {"type": "mate", "value": -3}
        eval_after = {"type": "mate", "value": 2}
        result = classify_mate(eval_before, eval_after, "b")
        assert result == MoveQuality.BLUNDER

    def test_black_still_getting_mated(self):
        # Black still getting mated
        eval_before = {"type": "mate", "value": 5}
        eval_after = {"type": "mate", "value": 3}
        result = classify_mate(eval_before, eval_after, "b")
        assert result == MoveQuality.BLUNDER


class TestClassifyMoveByDelta:
    def test_none_delta_is_blunder(self):
        assert classify_move_by_delta(None) == MoveQuality.BLUNDER

    def test_large_positive_delta_is_good(self):
        assert classify_move_by_delta(50) == MoveQuality.GOOD
        assert classify_move_by_delta(100) == MoveQuality.GOOD
        assert classify_move_by_delta(200) == MoveQuality.GOOD

    def test_small_negative_delta_is_inaccuracy(self):
        assert classify_move_by_delta(-20) == MoveQuality.INACCURACY
        assert classify_move_by_delta(-10) == MoveQuality.INACCURACY
        assert classify_move_by_delta(0) == MoveQuality.INACCURACY
        assert classify_move_by_delta(10) == MoveQuality.INACCURACY

    def test_medium_negative_delta_is_mistake(self):
        assert classify_move_by_delta(-21) == MoveQuality.MISTAKE
        assert classify_move_by_delta(-50) == MoveQuality.MISTAKE
        assert classify_move_by_delta(-100) == MoveQuality.MISTAKE

    def test_large_negative_delta_is_blunder(self):
        assert classify_move_by_delta(-101) == MoveQuality.BLUNDER
        assert classify_move_by_delta(-200) == MoveQuality.BLUNDER
        assert classify_move_by_delta(-500) == MoveQuality.BLUNDER

    def test_boundary_values(self):
        # Test exact boundary values
        assert classify_move_by_delta(50) == MoveQuality.GOOD
        assert classify_move_by_delta(49) == MoveQuality.INACCURACY
        assert classify_move_by_delta(-20) == MoveQuality.INACCURACY
        assert classify_move_by_delta(-21) == MoveQuality.MISTAKE
        assert classify_move_by_delta(-100) == MoveQuality.MISTAKE
        assert classify_move_by_delta(-101) == MoveQuality.BLUNDER


class TestClassifyMove:
    def test_mate_scenario_overrides_delta(self):
        # When mate is involved, delta should be ignored
        analysis = {
            "before": {"type": "mate", "value": 2},
            "after": {"type": "cp", "value": 100},
            "delta": 50,  # Would be GOOD, but this is a blunder
        }
        result = classify_move(analysis, "w")
        assert result == MoveQuality.BLUNDER

    def test_no_mate_uses_delta_good(self):
        analysis = {
            "before": {"type": "cp", "value": 50},
            "after": {"type": "cp", "value": 150},
            "delta": 100,
        }
        result = classify_move(analysis, "w")
        assert result == MoveQuality.GOOD

    def test_no_mate_uses_delta_inaccuracy(self):
        analysis = {
            "before": {"type": "cp", "value": 100},
            "after": {"type": "cp", "value": 90},
            "delta": -10,
        }
        result = classify_move(analysis, "w")
        assert result == MoveQuality.INACCURACY

    def test_no_mate_uses_delta_mistake(self):
        analysis = {
            "before": {"type": "cp", "value": 100},
            "after": {"type": "cp", "value": 0},
            "delta": -100,
        }
        result = classify_move(analysis, "w")
        assert result == MoveQuality.MISTAKE

    def test_no_mate_uses_delta_blunder(self):
        analysis = {
            "before": {"type": "cp", "value": 100},
            "after": {"type": "cp", "value": -50},
            "delta": -150,
        }
        result = classify_move(analysis, "w")
        assert result == MoveQuality.BLUNDER

    def test_escaped_mate_is_best(self):
        analysis = {
            "before": {"type": "mate", "value": -2},
            "after": {"type": "cp", "value": -50},
            "delta": None,
        }
        result = classify_move(analysis, "w")
        assert result == MoveQuality.BEST

    def test_found_mate_is_best(self):
        analysis = {
            "before": {"type": "cp", "value": 300},
            "after": {"type": "mate", "value": 3},
            "delta": None,
        }
        result = classify_move(analysis, "w")
        assert result == MoveQuality.BEST

    def test_black_good_move(self):
        analysis = {
            "before": {"type": "cp", "value": -50},
            "after": {"type": "cp", "value": -150},
            "delta": 100,  # Delta already adjusted for black perspective
        }
        result = classify_move(analysis, "b")
        assert result == MoveQuality.GOOD

    def test_black_found_mate_is_best(self):
        analysis = {
            "before": {"type": "cp", "value": -300},
            "after": {"type": "mate", "value": -3},
            "delta": None,
        }
        result = classify_move(analysis, "b")
        assert result == MoveQuality.BEST
