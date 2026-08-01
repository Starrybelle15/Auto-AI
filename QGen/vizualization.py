import pandas as pd
import plotly.express as px

def sentiment_chart(sentiments):

    df = pd.DataFrame(sentiments)

    fig = px.pie(
        df,
        names="label",
        title="Sentiment Distribution"
    )

    return fig
