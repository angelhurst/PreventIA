import pytest

from preventia.clinical.semaforo import (
    Color,
    EmptyRuleTable,
    UnknownFlag,
    classify,
)

PLACEHOLDER_TABLE = {
    "flag_a": Color.YELLOW,
    "flag_b": Color.RED,
    "flag_c": Color.GREEN,
}


def test_colors_are_ordered_green_below_yellow_below_red():
    assert Color.GREEN < Color.YELLOW < Color.RED


def test_raising_to_a_higher_color_returns_the_higher_color():
    assert Color.GREEN.raised_to(Color.RED) is Color.RED


def test_raising_to_a_lower_color_returns_the_original_color():
    assert Color.RED.raised_to(Color.GREEN) is Color.RED


def test_raising_to_the_same_color_is_a_no_op():
    assert Color.YELLOW.raised_to(Color.YELLOW) is Color.YELLOW


def test_color_parses_the_values_the_schema_stores():
    assert Color.parse("green") is Color.GREEN
    assert Color.parse("yellow") is Color.YELLOW
    assert Color.parse("red") is Color.RED


def test_color_serialises_back_to_the_value_the_schema_stores():
    assert Color.RED.value == "red"


def test_parsing_an_unknown_color_is_an_error():
    with pytest.raises(ValueError):
        Color.parse("orange")


def test_there_is_no_operation_that_lowers_a_color():
    lowering = [name for name in dir(Color) if "lower" in name or "downgrade" in name]
    assert lowering == []


def test_no_flags_leaves_the_floor_green():
    result = classify(flags=[], table=PLACEHOLDER_TABLE, model_color=Color.GREEN)
    assert result.rules_color is Color.GREEN


def test_a_flag_sets_the_floor_the_table_gives_it():
    result = classify(flags=["flag_b"], table=PLACEHOLDER_TABLE, model_color=Color.GREEN)
    assert result.rules_color is Color.RED


def test_the_highest_floor_wins_when_several_flags_fire():
    result = classify(
        flags=["flag_c", "flag_b", "flag_a"], table=PLACEHOLDER_TABLE, model_color=Color.GREEN
    )
    assert result.rules_color is Color.RED


def test_the_model_can_never_lower_a_color_the_rules_set():
    result = classify(flags=["flag_b"], table=PLACEHOLDER_TABLE, model_color=Color.GREEN)
    assert result.final_color is Color.RED


def test_the_model_may_raise_the_color_above_the_floor():
    result = classify(flags=[], table=PLACEHOLDER_TABLE, model_color=Color.RED)
    assert result.final_color is Color.RED


def test_the_rules_color_survives_the_model_raising_it():
    result = classify(flags=[], table=PLACEHOLDER_TABLE, model_color=Color.RED)
    assert result.rules_color is Color.GREEN
    assert result.final_color is Color.RED


def test_the_final_color_is_never_below_either_input():
    for flags, model in (
        ([], Color.GREEN),
        (["flag_a"], Color.GREEN),
        (["flag_b"], Color.YELLOW),
        ([], Color.RED),
        (["flag_b"], Color.RED),
    ):
        result = classify(flags=flags, table=PLACEHOLDER_TABLE, model_color=model)
        assert result.final_color >= result.rules_color
        assert result.final_color >= result.model_color


def test_the_flags_that_set_the_floor_are_reported():
    result = classify(flags=["flag_b", "flag_a"], table=PLACEHOLDER_TABLE, model_color=Color.GREEN)
    assert result.fired == ["flag_b"]


def test_a_flag_the_table_does_not_know_is_an_error_rather_than_ignored():
    with pytest.raises(UnknownFlag):
        classify(flags=["flag_z"], table=PLACEHOLDER_TABLE, model_color=Color.GREEN)


def test_an_empty_rule_table_is_an_error_rather_than_a_green_light():
    with pytest.raises(EmptyRuleTable):
        classify(flags=[], table={}, model_color=Color.GREEN)
