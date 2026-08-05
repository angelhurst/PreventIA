import re
from pathlib import Path

import pytest

TOKENS = Path(__file__).resolve().parents[1] / "preventia" / "dashboard" / "static" / "tokens.css"

AA_TEXT = 4.5
AA_NON_TEXT = 3.0

TEXT_PAIRS = [
    ("--sem-red-ink", "--sem-red-bg"),
    ("--sem-yellow-ink", "--sem-yellow-bg"),
    ("--sem-green-ink", "--sem-green-bg"),
    ("--accent-ink", "--accent-bg"),
    ("--ink", "--surface"),
    ("--ink", "--surface-sunken"),
    ("--ink-muted", "--surface"),
    ("--ink-faint", "--surface"),
    ("--link", "--surface"),
    ("--brand-ink", "--brand"),
    ("--brand-ink-muted", "--brand"),
    ("--ink", "--state-pending-bg"),
    ("--ink", "--state-review-bg"),
    ("--ink", "--state-contacted-bg"),
    ("--ink-muted", "--state-closed-bg"),
]

NON_TEXT_PAIRS = [
    ("--line-strong", "--surface"),
    ("--focus", "--surface"),
    ("--focus-halo", "--brand"),
]

THEMES = ["light", "contrast"]


def _block(css, selector):
    match = re.search(re.escape(selector) + r"\s*\{(.*?)\}", css, re.S)
    if match is None:
        raise AssertionError(f"{selector} not found in tokens.css")
    return dict(re.findall(r"(--[a-z0-9-]+)\s*:\s*(#[0-9a-fA-F]{3,6})\s*;", match.group(1)))


def _themes():
    css = TOKENS.read_text(encoding="utf-8")
    light = _block(css, ":root")
    contrast = dict(light)
    contrast.update(_block(css, "html.contrast-high"))
    return {"light": light, "contrast": contrast}


def _luminance(value):
    value = value.lstrip("#")
    if len(value) == 3:
        value = "".join(channel * 2 for channel in value)
    channels = [int(value[index : index + 2], 16) / 255 for index in (0, 2, 4)]
    linear = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast_ratio(foreground, background):
    first, second = _luminance(foreground), _luminance(background)
    lighter, darker = max(first, second), min(first, second)
    return (lighter + 0.05) / (darker + 0.05)


@pytest.fixture(scope="module")
def themes():
    return _themes()


@pytest.mark.parametrize("theme", THEMES)
@pytest.mark.parametrize("foreground,background", TEXT_PAIRS)
def test_text_meets_aa(themes, theme, foreground, background):
    tokens = themes[theme]
    ratio = contrast_ratio(tokens[foreground], tokens[background])
    assert ratio >= AA_TEXT, (
        f"{theme}: {foreground} {tokens[foreground]} on {background} {tokens[background]} "
        f"is {ratio:.2f}:1, below the {AA_TEXT}:1 required by WCAG 2.2 AA"
    )


@pytest.mark.parametrize("theme", THEMES)
@pytest.mark.parametrize("foreground,background", NON_TEXT_PAIRS)
def test_non_text_meets_aa(themes, theme, foreground, background):
    tokens = themes[theme]
    ratio = contrast_ratio(tokens[foreground], tokens[background])
    assert ratio >= AA_NON_TEXT, (
        f"{theme}: {foreground} {tokens[foreground]} on {background} {tokens[background]} "
        f"is {ratio:.2f}:1, below the {AA_NON_TEXT}:1 required by WCAG 2.2 AA"
    )


@pytest.mark.parametrize("theme", THEMES)
def test_semaforo_colors_are_never_used_as_text_on_the_page(themes, theme):
    tokens = themes[theme]
    for token in ("--sem-red", "--sem-yellow", "--sem-green"):
        assert tokens[token] == tokens[f"{token}-bg"], (
            f"{theme}: {token} must stay identical to its fill, because the government palette "
            "fails AA as text and is only ever used as a fill"
        )


def test_font_size_theme_has_three_steps():
    css = TOKENS.read_text(encoding="utf-8")
    steps = re.findall(r"html\.letra-(\d)\s*\{\s*--font-scale:\s*([0-9.]+)", css)
    assert [step for step, _ in steps] == ["0", "1", "2"]
    assert [float(scale) for _, scale in steps] == [1.0, 1.25, 1.5]
