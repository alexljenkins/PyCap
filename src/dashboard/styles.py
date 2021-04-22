class Styles:
    """CSS stylings for specific elements"""

    side_nav = {
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "16rem",
        "padding": "2rem 1rem",
        "background-color": "#f8f9fa",
    }

    stock_price_graph = {"margin": {"l": 0, "r": 0, "t": 20, "b": 30}, "width": "800"}

    content = {
        "margin-left": "18rem",
        "margin-right": "2rem",
        "padding": "2rem 1rem",
    }

    button = {"margin-bottom": "15px", "position": "relative", "left": "50%", "transform": "translate(-50%, 0)"}

    # TODO: not sure why 100% doesn't work for width, need to check how big the container size is :/
    table = {
        "width": "800px",
        # 'minWidth': '100%',
    }
