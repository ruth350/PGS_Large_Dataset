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
    #### Exclusicely for Camborne data (aka to much effort to copy in all the other files)
    """)
    return


@app.cell
def _(mo):

    photo = mo.image(
        src="Camborne_Photo.png", 
        width=600, 
        alt="Photo of Camborne from Google Maps"
    )
    photo
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##Data Cleaning

    ####I have cleaned this data by:
    - ####Replacing 'tr' on the rainfall data with a 0. tr means > 0.05, so 0 is close enough (and, importantly, numeric)
    - ####Ignoring any N/A values so they do not distupt numeric data
    """)
    return


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    def load_and_clean(file):
        file_name = file +'.csv'
        df = pd.read_csv(file_name, skiprows=5, na_values=["N/A", "n/a", " N/A"])

        # Cleaning data
        rain = 'Daily Total Rainfall (0900-0900) (mm)'

        if rain in df.columns:
            df[rain] = df[rain].replace('tr', 0)
            df[rain] = pd.to_numeric(df[rain], errors='coerce')

        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')

        return df

    return load_and_clean, mo, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##Plot Against time (comparing 2015 and 1987)
    """)
    return


@app.cell
def _(load_and_clean, mo):
    dataframes = {'1987': load_and_clean('camborne_1987'), '2015':load_and_clean('camborne_2015')}

    cols_2015 = set(dataframes['2015'].select_dtypes('number').columns.tolist())
    cols_1987 = set(dataframes['1987'].select_dtypes('number').columns.tolist())

    valid_cols = list(cols_2015 & cols_1987)


    dropdown_val = mo.ui.dropdown(
        options=(valid_cols), 
        value='Daily Mean Windspeed (0000-2400) (kn)',  # Initial selection
        label="Choose value to compare"
    )

    dropdown_val
    return dataframes, dropdown_val, valid_cols


@app.cell
def _(alt, dataframes, dropdown_scale, dropdown_val, pd, valid_cols):
    monthly_averages_2015 = dataframes['2015'].groupby(dataframes['2015']['Date'].dt.month)[valid_cols].mean()
    monthly_averages_1987 = dataframes['1987'].groupby(dataframes['1987']['Date'].dt.month)[valid_cols].mean()

    df_1987 = monthly_averages_1987.reset_index()
    df_2015 = monthly_averages_2015.reset_index()

    # 2. Rename the column if it's still called 'Date' to avoid confusion
    df_1987 = df_1987.rename(columns={'Date': 'Month'})
    df_2015 = df_2015.rename(columns={'Date': 'Month'})

    # 3. Add labels and combine
    df_1987['Year'] = '1987'
    df_2015['Year'] = '2015'
    combined = pd.concat([df_1987, df_2015])

    # 4. Plot using 'Month' instead of 'Date'
    alt.Chart(combined).mark_line(point=True).encode(
        x= alt.X('Month:O'),  # This will now show only 1 through 12
        y= alt.Y(dropdown_val.value, scale=alt.Scale(type=dropdown_scale.value, zero=False, padding=10)),
        color='Year:N'
    ).properties(
        width=600,
        height=300
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##Graphical Plot - Choose x axis, y axis, colour, and Scale
    """)
    return


@app.cell
def _(load_and_clean):
    df = load_and_clean("camborne_2015")
    return (df,)


@app.cell
def _(df, mo):

    numerical_cols = df.select_dtypes(include='float64').columns.tolist()

    dropdown_x = mo.ui.dropdown(
        options=(numerical_cols), 
        value='Daily Mean Windspeed (0000-2400) (kn)',  # Initial selection
        label="Choose x axis value"
    )

    dropdown_y = mo.ui.dropdown(
        options=(numerical_cols), 
        value='Daily Maximum Gust (0000-2400) (kn)',  # Initial selection
        label="Choose y axis value"
    )

    dropdown_color = mo.ui.dropdown(
        options=(numerical_cols), 
        value='Daily Total Sunshine (0000-2400) (hrs)',  # Initial selection
        label="Choose color"
    )

    dropdown_scale = mo.ui.dropdown(
        options=['linear', 'log', 'symlog'],
        value="linear",
        label="Choose scale"
    )

    display = mo.vstack([mo.hstack([dropdown_x, dropdown_color], justify="space-between"), mo.hstack([dropdown_y, dropdown_scale], justify="space-between")])

    display

    return (
        dropdown_color,
        dropdown_scale,
        dropdown_x,
        dropdown_y,
        numerical_cols,
    )


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
        value='Daily Mean Total Cloud (oktas)',  # Initial selection
        label="Choose Histogram value"
    )
    dropdown_histogram
    return (dropdown_histogram,)


@app.cell
def _(alt, df, dropdown_histogram):
    histogram = alt.Chart(df).mark_bar().encode(
        alt.X(dropdown_histogram.value, bin=True, title=dropdown_histogram.value),
        alt.Y('count():Q', title='Frequency Density') 
    ).properties(
        width=600, 
        height=400,
        title=f'Frequency Distribution of {dropdown_histogram.value}'
    )

    histogram
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


if __name__ == "__main__":
    app.run()
