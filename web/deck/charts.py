"""Chart.js config helpers for WebDeck slides."""

from __future__ import annotations

from typing import Any


def line_chart(
    labels: list[str],
    datasets: list[dict[str, Any]],
    *,
    ymin: float = 45,
    ymax: float = 70,
) -> dict[str, Any]:
    return {
        "type": "line",
        "data": {"labels": labels, "datasets": datasets},
        "options": {
            "responsive": True,
            "maintainAspectRatio": False,
            "plugins": {"legend": {"labels": {"font": {"size": 10}}}},
            "scales": {"y": {"min": ymin, "max": ymax}},
        },
    }


def bar_vertical(
    labels: list[str],
    values: list[float],
    *,
    colors: list[str] | None = None,
    ymin: float = 35,
    ymax: float = 70,
) -> dict[str, Any]:
    color = colors or ["#2563eb"] * len(values)
    if len(color) == 1 and len(values) > 1:
        color = color * len(values)
    return {
        "type": "bar",
        "data": {
            "labels": labels,
            "datasets": [{"data": values, "backgroundColor": color}],
        },
        "options": {
            "responsive": True,
            "maintainAspectRatio": False,
            "plugins": {"legend": {"display": False}},
            "scales": {"y": {"min": ymin, "max": ymax}},
        },
    }


def scatter_line(
    xs: list[float],
    ys: list[float],
    *,
    color: str = "#2563eb",
    label: str = "",
    x_title: str = "",
    ymin: float | None = None,
    ymax: float | None = None,
) -> dict[str, Any]:
    y_scale: dict[str, Any] = {}
    if ymin is not None:
        y_scale["min"] = ymin
    if ymax is not None:
        y_scale["max"] = ymax
    return {
        "type": "scatter",
        "data": {
            "datasets": [
                {
                    "label": label,
                    "data": [{"x": x, "y": y} for x, y in zip(xs, ys)],
                    "borderColor": color,
                    "backgroundColor": color,
                    "showLine": True,
                    "tension": 0.1,
                    "pointRadius": 5,
                }
            ]
        },
        "options": {
            "responsive": True,
            "maintainAspectRatio": False,
            "plugins": {"legend": {"display": bool(label)}},
            "scales": {
                "x": {
                    "type": "linear",
                    "title": {"display": bool(x_title), "text": x_title, "font": {"size": 10}},
                },
                "y": y_scale,
            },
        },
    }


def pie_chart(
    labels: list[str],
    values: list[float],
    *,
    colors: list[str] | None = None,
) -> dict[str, Any]:
    palette = colors or [
        "#2563eb",
        "#059669",
        "#0d9488",
        "#7c3aed",
        "#dc2626",
        "#d97706",
        "#64748b",
    ]
    bg = palette[: len(values)]
    if len(bg) < len(values):
        bg = bg + ["#64748b"] * (len(values) - len(bg))
    return {
        "type": "pie",
        "data": {
            "labels": labels,
            "datasets": [{"data": values, "backgroundColor": bg, "borderWidth": 1}],
        },
        "options": {
            "responsive": True,
            "maintainAspectRatio": False,
            "plugins": {
                "legend": {"position": "right", "labels": {"font": {"size": 10}}},
                "tooltip": {
                    "callbacks": {},
                },
            },
        },
    }


def bar_horizontal(
    labels: list[str],
    values: list[float],
    *,
    color: str = "#2563eb",
    colors: list[str] | None = None,
    xmin: float = 35,
    xmax: float = 70,
) -> dict[str, Any]:
    bg = colors or [color] * len(values)
    if len(bg) == 1 and len(values) > 1:
        bg = bg * len(values)
    return {
        "type": "bar",
        "data": {
            "labels": labels,
            "datasets": [{"data": values, "backgroundColor": bg}],
        },
        "options": {
            "indexAxis": "y",
            "responsive": True,
            "maintainAspectRatio": False,
            "plugins": {"legend": {"display": False}},
            "scales": {
                "x": {"min": xmin, "max": xmax},
                "y": {"ticks": {"font": {"size": 9}}},
            },
        },
    }
