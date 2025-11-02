def save_plot(fig, filename):
    """
    Save a matplotlib figure to a file in high resolution.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure object to be saved.
    filename : str
        The name (and optionally path) of the file to save the figure as.

    Notes
    -----
    - The figure is saved with a DPI of 300 for high-quality output.
    """
    import matplotlib.pyplot as plt

    # Save the figure with high DPI and tight bounding box
    fig.savefig(f'{filename}', dpi=300,)

    # Confirm successful save
    print(f"\n✅ '{filename}' has been saved successfully.")
