"""Energy-ES - User Interface - Chart."""

from io import BytesIO
from datetime import date

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from tkinter.ttk import Widget, Label


def _get_chart_image(dt: date, prices: list[dict]) -> Image.Image:
    """Return the chart image.

    :param dt: Date of the prices.
    :param prices: List of dictionaries, where each dictionary contains the
    "hour" (string) and "value" (float) keys.
    :return: Chart image.
    """
    # Format date
    dt = dt.strftime(f"%a {dt.day} %b %Y")

    # Create X axis values
    x = list(map(lambda x: x["hour"], prices))
    x = np.array(x)

    # Create Y axis values
    y = list(map(lambda x: x["value"], prices))
    y = np.array(y)

    # Minimum price
    min_price = min(prices, key=lambda x: x["value"])
    min_x = min_price["hour"]
    min_y = min_price["value"]

    # Maximum price
    max_price = max(prices, key=lambda x: x["value"])
    max_x = max_price["hour"]
    max_y = max_price["value"]

    # Create chart
    fig, ax = plt.subplots(figsize=(7, 3))
    fig.suptitle(f"Spot market price in €/MWh in Spain for {dt}", y=0.94)

    ax.set_title("Source: Red Electrica", fontdict={"fontsize": 10})
    ax.plot(x, y, marker="o")
    ax.scatter([min_x], [min_y], c="#00d800", zorder=2)
    ax.scatter([max_x], [max_y], c="#ff0000", zorder=2)

    ax.set(xlabel="Hour (PM)", ylabel="€/MWh")
    ax.grid()

    plt.xticks(rotation=45, ha="right", rotation_mode="anchor")
    plt.tight_layout()

    # Convert the figure to a PIL image
    buf = BytesIO()
    fig.savefig(buf)
    buf.seek(0)

    return Image.open(buf)


def get_chart_widget(
    dt: date, prices: list[dict], root: Widget = None
) -> Widget:
    """Return the chart widget.

    :param dt: Date of the prices.
    :param prices: List of dictionaries, where each dictionary contains the
    "hour" (string) and "value" (float) keys.
    :param root: Root widget.
    :return: Chart widget.
    """
    img = _get_chart_image(dt, prices)
    img = ImageTk.PhotoImage(img)
    chart = Label(root, image=img)

    # Keep a reference to the image in order to avoid that the garbage
    # collector deletes it.
    chart.image = img

    return chart
