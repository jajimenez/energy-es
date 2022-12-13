"""Energy-ES - User Interface - Chart."""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from userconf import UserConf

from energy_es.data.prices import PricesManager
from energy_es.data.tools import get_time


APP_ID = "energy_es"
UNIT_LABELS = {"k": "€/KWh", "m": "€/MWh"}


def _write_chart(unit: str, path: str):
    """Generate and write the chart HTML page with updated data.

    :param unit: Prices unit. It must be "k" to have the prices in €/KWh or "m"
    to have them in €/MWh.
    :param path: Destination file path.
    """
    unit = unit.lower()

    # Check units
    if unit not in ("k", "m"):
        raise Exception('Invalid unit. It must be "k" (€/KWh) or "m" (€/MWh)')

    unit_label = UNIT_LABELS[unit]

    # Get data
    pm = PricesManager()
    spot = pm.get_spot_market_prices(unit)
    pvpc = pm.get_pvpc_prices(unit)

    # Transform data
    prices = []

    for i in (spot, pvpc):
        i2 = list(map(
            lambda x: {
                "time": get_time(x["datetime"]),
                "value": x["value"]
            },
            i
        ))

        prices.append(i2)

    spot_2, pvpc_2 = prices

    # Title and source
    dt = spot[0]["datetime"]
    dt = dt.strftime(f"%A {dt.day} %B %Y (%Z)")

    title = f"Electricity price ({unit_label}) in Spain (peninsula) for {dt}"
    source = "Data source: Red Eléctrica de España"

    # Create dataframes
    spot_df = pd.DataFrame(spot_2)
    pvpc_df = pd.DataFrame(pvpc_2)

    text = ["<b>MIN</b>", "<b>MAX</b>"]
    text_pos = ["bottom center", "top center"]

    for df in (spot_df, pvpc_df):
        cond = [
            df["value"] == df["value"].min(),
            df["value"] == df["value"].max()
        ]

        df["text"] = np.select(cond, text, default=None)
        df["text_position"] = np.select(cond, text_pos, default="top center")

    # Create chart
    fig = go.Figure()

    fig.update_layout(
        title={
            "text":
                f'{title}<br><span style="font-size: 14px">{source}</span>',
            "yref": "paper",
            "y": 1,
            "yanchor": "bottom",
            "pad": {"l": 77, "b": 40},
            "x": 0,
            "xanchor": "left"
        },
        plot_bgcolor="white",
        xaxis={
            "title": "Time",
            "fixedrange": True,
            "showline": True,
            "mirror": True,
            "linecolor": "black",
            "gridcolor": "lightgrey",
            "ticks": "outside",
            "tickangle": 45
        },
        yaxis={
            "title": unit_label,
            "fixedrange": True,
            "showline": True,
            "mirror": True,
            "linecolor": "black",
            "gridcolor": "lightgrey",
            "ticks": "outside"
        },
        legend={"itemdoubleclick": False},
        margin={"t": 65}
    )

    hover_tem = "Time: &nbsp;%{x}<br>Price: &nbsp;%{y} " + unit_label
    spot_hover_tem = "<b>Spot Market</b><br>" + hover_tem
    pvpc_hover_tem = "<b>PVPC</b><br>" + hover_tem

    # Spot market prices
    spot_sca = go.Scatter(
        x=spot_df["time"],
        y=spot_df["value"],
        mode="lines+markers+text",
        text=spot_df["text"],
        line={"width": 3, "color": "#2077b4"},
        marker={"size": 12, "color": "#2077b4"},
        textposition=spot_df["text_position"],
        textfont={"color": "#2077b4"},
        name="Spot Market price",
        hovertemplate=spot_hover_tem,
        hoverlabel={"namelength": 0}
    )

    # PVPC prices
    pvpc_sca = go.Scatter(
        x=pvpc_df["time"],
        y=pvpc_df["value"],
        mode="lines+markers+text",
        text=pvpc_df["text"],
        line={"width": 3, "color": "#ff8c00"},
        marker={"size": 12, "color": "#ff8c00"},
        textposition=pvpc_df["text_position"],
        textfont={"color": "#ff8c00"},
        name="PVPC price",
        hovertemplate=pvpc_hover_tem,
        hoverlabel={"namelength": 0}
    )

    fig.add_traces([pvpc_sca, spot_sca])
    conf = {"displayModeBar": False}

    # Write chart
    fig.write_html(path, config=conf)


def get_chart_path(unit: str = "m") -> str:
    """Generate and write the chart HTML page with updated data and get its
    path.

    :param unit: Prices unit. It must be "k" to have the prices in €/KWh or "m"
    (default) to have them in €/MWh.
    :return: Absolute path of the chart file.
    """
    uc = UserConf(APP_ID)

    path = uc.files.get_path("chart.html")
    _write_chart(unit, path)

    return path
