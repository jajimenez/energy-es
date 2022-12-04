"""Energy-ES - User Interface - Chart."""

from io import BytesIO

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from tkinter.ttk import Widget, Label

from energy_es.data import get_prices


def get_chart_image() -> Image.Image:
    """Return the chart image."""
    # Get prices
    prices = get_prices()

    # Get current day
    d = prices[0]["datetime"].strftime("%Y-%m-%d")

    # Create X axis values
    x = list(map(lambda x: x["datetime"].strftime("%H:%M"), prices))
    x = np.array(x)

    # Create Y axis values
    y = list(map(lambda x: x["value"], prices))
    y = np.array(y)

    # Get minimum price
    min_y = y.min()
    min_x = x[y.argmin()]

    # Get maximum price
    max_y = y.max()
    max_x = x[y.argmax()]

    # Create chart
    fig, ax = plt.subplots(figsize=(7, 3))

    ax.plot(x, y, marker="o")
    ax.scatter([min_x], [min_y], c="#00d800", zorder=2)
    ax.scatter([max_x], [max_y], c="#ff0000", zorder=2)

    ax.set(
        title=f"Spot market price in €/MWh in Spain for {d}",
        xlabel="Hour",
        ylabel="€/MWh"
    )

    ax.grid()

    plt.xticks(rotation=45, ha="right", rotation_mode="anchor")
    plt.tight_layout()

    # Convert the figure to a PIL image
    buf = BytesIO()
    fig.savefig(buf)
    buf.seek(0)

    return Image.open(buf)


def get_chart_widget(root: Widget = None) -> Widget:
    """Return the chart widget."""
    img = get_chart_image()
    img = ImageTk.PhotoImage(img)
    chart = Label(root, image=img)

    # Keep a reference to the image in order to avoid that the garbage
    # collector deletes it.
    chart.image = img

    return chart
