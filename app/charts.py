import plotly.graph_objects as go


def bar_chart(x, y, text=None, colors=None, x_title="", y_title="", height=400, y_range=None):
    fig = go.Figure(
        data=[
            go.Bar(
                x=x,
                y=y,
                text=text,
                textposition="outside" if text is not None else None,
                textfont=dict(size=14, color="#1f1f1f"),
                marker_color=colors,
            )
        ]
    )
    fig.update_layout(
        xaxis_title=x_title,
        yaxis_title=y_title,
        height=height,
        margin=dict(l=40, r=40, t=60, b=60),
        showlegend=False,
    )
    if y_range is not None:
        fig.update_yaxes(range=y_range)
    return fig
