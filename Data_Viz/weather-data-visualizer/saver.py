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
    - 'bbox_inches' is set to 'tight' to reduce unnecessary whitespace.
    """
    import matplotlib.pyplot as plt

    # Save the figure with high DPI and tight bounding box
    fig.savefig(filename, dpi=300, bbox_inches='tight')

    # Confirm successful save
    print(f"\n✅ '{filename}' has been saved successfully in the current directory.")