from analise_fundos_imobiliarios.series import (
    fbm_negative,
    fbm_none,
    fbm_positive,
    logistic_map,
    random,
    sine_map,
)


def test_logistic_map_working():
    result = logistic_map(4)
    assert result.size == 4


def test_sine_map_working():
    result = sine_map(4)
    assert result.size == 4


def test_fbm_negative_working():
    result = fbm_negative(4)
    assert result.size == 4


def test_fbm_positive_working():
    result = fbm_positive(4)
    assert result.size == 4


def test_fbm_none_working():
    result = fbm_none(4)
    assert result.size == 4


def test_random_working():
    result = random(4)
    assert result.size == 4
