"""Energy-ES - User Interface - Chart."""

from io import BytesIO

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from tkinter.ttk import Widget, Label

from energy_es.data import get_prices


ChartImage = tuple[Image.Image, str, float, str, float]
ChartWidget = tuple[Widget, str, float, str, float]


def get_chart_image() -> tuple[Image.Image, str, str]:
    """Return the chart image.

    :return: Tuple containing the image, information about the minimum value
    and information about the maximum value.
    """
    # Get prices
    prices = get_prices()

    # Get current day
    d = prices[0]["datetime"]
    d = d.strftime(f"%a, {d.day} %b %Y")

    # Create X axis values
    x = list(map(lambda x: x["datetime"].strftime("%H:%M"), prices))
    x = np.array(x)

    # Create Y axis values
    y = list(map(lambda x: x["value"], prices))
    y = np.array(y)

    # Get minimum price
    min_y = y.min()
    min_x = x[y.argmin()]
    min_text = f"{min_x}, {min_y} €/MWh"

    # Get maximum price
    max_y = y.max()
    max_x = x[y.argmax()]
    max_text = f"{max_x}, {max_y} €/MWh"

    # Create chart
    fig, ax = plt.subplots(figsize=(7, 3))
    fig.suptitle(f"Spot market price in €/MWh in Spain for {d}", y=0.94)

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

    return Image.open(buf), min_text, max_text


def get_chart_widget(root: Widget = None) -> tuple[Widget, str, str]:
    """Return the chart widget.

    :return: Tuple containing the widget, information about the minimum value
    and information about the maximum value.
    """
    img, min_text, max_text = get_chart_image()
    img = ImageTk.PhotoImage(img)
    chart = Label(root, image=img)

    # Keep a reference to the image in order to avoid that the garbage
    # collector deletes it.
    chart.image = img

    return chart, min_text, max_text
