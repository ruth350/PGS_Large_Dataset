import marimo

__generated_with = "0.23.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #Large Dataset visualiser
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##Data Cleaning

    I have cleaned this data by:
    - Replacing 'tr' on the rainfall data with a 0. tr means > 0.05, so 0 is close enough (and, importantly, numeric)
    - Replacing any N/A values with spaces (so N/A doesn't become a value in its own right - like 25% of days had N/A windspeed)
    """)
    return


@app.cell
def _():
    import marimo as mo
    import pandas as pd

    df = pd.read_csv("camborne_2015.csv", skiprows=5, na_values=["N/A", "n/a", " N/A"])

    # Cleaning data
    df['Daily Total Rainfall (0900-0900) (mm)'] = df['Daily Total Rainfall (0900-0900) (mm)'].replace('tr', 0)
    df['Daily Total Rainfall (0900-0900) (mm)'] = pd.to_numeric(df['Daily Total Rainfall (0900-0900) (mm)'], errors='coerce')

    return df, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##Graphical Plot - Choose x axis, y axis, colour, and Scale
    """)
    return


@app.cell
def _(df, mo):
    # dropdowns
    numerical_cols = df.select_dtypes(include='float64').columns.tolist()

    dropdown_x = mo.ui.dropdown(
        options=(numerical_cols), 
        value='Daily Mean Windspeed (0000-2400) (kn)',  # Initial selection
        label="Choose y axis value"
    )

    dropdown_x


    return dropdown_x, numerical_cols


@app.cell
def _(mo, numerical_cols):
    dropdown_y = mo.ui.dropdown(
        options=(numerical_cols), 
        value='Daily Maximum Gust (0000-2400) (kn)',  # Initial selection
        label="Choose y axis value"
    )

    dropdown_y
    return (dropdown_y,)


@app.cell
def _(mo, numerical_cols):
    dropdown_color = mo.ui.dropdown(
        options=(numerical_cols), 
        value='Daily Total Sunshine (0000-2400) (hrs)',  # Initial selection
        label="Choose color"
    )

    dropdown_color
    return (dropdown_color,)


@app.cell
def _(mo):
    dropdown_scale = mo.ui.dropdown(
        options=['linear', 'log', 'symlog'],
        value="linear",
        label="Choose scale"
    )

    dropdown_scale
    return (dropdown_scale,)


@app.cell
def _(df, dropdown_color, dropdown_scale, dropdown_x, dropdown_y):
    import altair as alt
    # Add Choice of x and y variables

    # Add Choice of axes

    # Add option to change color (eg color based on month)


    # Choose color scheme (for the lols))

    # Ensure correctly centered


    chart = alt.Chart(df).mark_point(filled=True, size=60).encode(
        x= alt.X(dropdown_x.value, scale=alt.Scale(zero=False, padding=10)),
        y= alt.Y(
            dropdown_y.value,
            scale=alt.Scale(type=dropdown_scale.value, zero=False, padding=10)
        ),
        color=alt.Color(dropdown_color.value).scale(scheme='viridis'),
        tooltip=[dropdown_x.value, dropdown_y.value, dropdown_color.value]
    ).properties(
        width=700,  # Width in pixels
        height=400  # Height in pixels
    ).interactive()

    chart
    return (alt,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    .
    ##Histogram - Chose value to plot
    """)
    return


@app.cell
def _(mo, numerical_cols):
    dropdown_histogram = mo.ui.dropdown(
        options=(numerical_cols), 
        value='Daily Total Sunshine (0000-2400) (hrs)',  # Initial selection
        label="Choose Histogram value"
    )
    dropdown_histogram
    return (dropdown_histogram,)


@app.cell
def _(alt, df, dropdown_histogram):
    histogram = alt.Chart(df).transform_joinaggregate(
        total='count(*)'                     # 1. Calculate total rows in dataset
    ).transform_calculate(
        density='1 / datum.total'            # 2. Create a "density" contribution per row
    ).mark_bar().encode(
        alt.X(dropdown_histogram.value, bin=True, title=dropdown_histogram.value),
        alt.Y('sum(density):Q', title='Frequency Density') # 3. Sum the contributions
    ).properties(
        width=600, 
        height=400
    )

    histogram

    return


@app.cell
def _():
    #Connected chart showing change in monthly average
    return


if __name__ == "__main__":
    app.run()
