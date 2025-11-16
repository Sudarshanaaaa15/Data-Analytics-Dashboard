import dash
import os
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from analysis import get_total_sales, get_monthly_sales, get_top_categories, get_customer_segmentation, get_top_states, \
    get_top_cities

# -----------------------------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.title = "Amazon Sales Dashboard"

# -----------------------------
# Load data for plots
total_revenue, total_orders, avg_order_value = get_total_sales()
monthly_sales = get_monthly_sales()
by_qty, by_revenue = get_top_categories()
customer_seg = get_customer_segmentation()
top_states = get_top_states()
top_cities = get_top_cities()

# -----------------------------
# Layout
app.layout = dbc.Container([
    html.H1("📊 Amazon Sales Dashboard", style={'textAlign': 'center', 'marginBottom': 20}),

    # ----- Cards for Total Metrics -----
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Total Revenue", className="card-title"),
                html.H3(f"₹{total_revenue:,.2f}", className="card-text")
            ])
        ], color="primary", inverse=True), width=4),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Total Orders", className="card-title"),
                html.H3(f"{total_orders:,}", className="card-text")
            ])
        ], color="success", inverse=True), width=4),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Average Order Value", className="card-title"),
                html.H3(f"₹{avg_order_value:,.2f}", className="card-text")
            ])
        ], color="info", inverse=True), width=4),
    ], className="mb-4"),

    # ----- Monthly Sales Trend -----
    dbc.Card([
        dbc.CardHeader(html.H5("Monthly Sales Trend")),
        dbc.CardBody([
            dcc.DatePickerRange(
                id='date-range',
                min_date_allowed=monthly_sales['Date'].min(),
                max_date_allowed=monthly_sales['Date'].max(),
                start_date=monthly_sales['Date'].min(),
                end_date=monthly_sales['Date'].max(),
            ),
            dcc.Graph(id='monthly-sales-graph')
        ])
    ], className="mb-4"),

    # ----- Top-Selling Categories -----
    dbc.Card([
        dbc.CardHeader(html.H5("Top-Selling Categories")),
        dbc.CardBody([
            dbc.Row([
                dbc.Col(dcc.Dropdown(
                    id='category-type',
                    options=[
                        {'label': 'By Quantity', 'value': 'qty'},
                        {'label': 'By Revenue', 'value': 'revenue'}
                    ],
                    value='qty'
                ), width=4),
                dbc.Col(dcc.Dropdown(
                    id='category-filter',
                    options=[{'label': c, 'value': c} for c in sorted(by_qty['Category'].unique())],
                    multi=True,
                    placeholder="Filter Categories"
                ), width=8)
            ]),
            dcc.Graph(id='top-categories-graph')
        ])
    ], className="mb-4"),

    # ----- Customer Segmentation -----
    dbc.Card([
        dbc.CardHeader(html.H5("Customer Segmentation (B2B vs Individual)")),
        dbc.CardBody([
            dcc.Graph(
                figure=px.pie(customer_seg, values='TotalRevenue', names='Label',
                              color_discrete_sequence=px.colors.sequential.RdBu, title="Revenue Share")
            )
        ])
    ], className="mb-4"),

    # ----- Geographical Analysis -----
    dbc.Card([
        dbc.CardHeader(html.H5("Geographical Analysis")),
        dbc.CardBody([
            dbc.Tabs([
                dbc.Tab(label='Top States', tab_id='tab-states'),
                dbc.Tab(label='Top Cities', tab_id='tab-cities'),
            ], id='geo-tabs', active_tab='tab-states'),
            html.Div(id='geo-graph-container')
        ])
    ])
], fluid=True)


# -----------------------------
# Callbacks

# Monthly sales update by date range
@app.callback(
    Output('monthly-sales-graph', 'figure'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date')
)
def update_monthly_sales(start, end):
    filtered = monthly_sales[(monthly_sales['Date'] >= start) & (monthly_sales['Date'] <= end)]
    fig = px.line(filtered, x='Date', y='Amount', markers=True, title="Monthly Revenue",
                  color_discrete_sequence=['lime'])
    fig.update_yaxes(tickprefix="₹", tickformat=",")
    fig.update_layout(plot_bgcolor='#1e1e2f', paper_bgcolor='#1e1e2f', font_color='white')
    return fig


# Top categories update
@app.callback(
    Output('top-categories-graph', 'figure'),
    Input('category-type', 'value'),
    Input('category-filter', 'value')
)
def update_top_categories(cat_type, selected_cats):
    if cat_type == 'qty':
        df_plot = by_qty.copy()
        y_col = 'Qty'
    else:
        df_plot = by_revenue.copy()
        y_col = 'Amount'
    if selected_cats:
        df_plot = df_plot[df_plot['Category'].isin(selected_cats)]

    if cat_type == 'revenue':
        fig = px.bar(df_plot, x='Category', y=y_col,
                     title="Top Categories by Revenue",
                     color=y_col,
                     color_continuous_scale='Viridis',
                     labels={y_col: "Amount (INR)"},
                     hover_data={y_col: ':.0f'})  # Hover shows full number
        fig.update_coloraxes(colorbar_tickprefix="₹", colorbar_tickformat=",")  # Format colorbar as INR
    else:
        fig = px.bar(df_plot, x='Category', y=y_col,
                     title="Top Categories by Quantity",
                     color=y_col,
                     color_continuous_scale='Viridis',
                     labels={y_col: "Quantity"})

    if y_col == 'Amount':
        fig.update_yaxes(tickprefix="₹", tickformat=",")
    fig.update_layout(plot_bgcolor='#1e1e2f', paper_bgcolor='#1e1e2f', font_color='white')
    return fig


# Geographical tabs
@app.callback(
    Output('geo-graph-container', 'children'),
    Input('geo-tabs', 'active_tab')
)
def update_geo_graph(tab):
    if tab == 'tab-states':
        fig = px.bar(top_states, x='ship-state', y='Amount', title='Top States by Revenue', color='Amount',
                     color_continuous_scale='Plasma')
        fig.update_coloraxes(colorbar_tickprefix="₹", colorbar_tickformat=",")
    else:
        fig = px.bar(top_cities, x='ship-city', y='Amount', title='Top Cities by Revenue', color='Amount',
                     color_continuous_scale='Plasma')
        fig.update_coloraxes(colorbar_tickprefix="₹", colorbar_tickformat=",")
    fig.update_yaxes(tickprefix="₹", tickformat=",")
    fig.update_layout(plot_bgcolor='#1e1e2f', paper_bgcolor='#1e1e2f', font_color='white')
    return dcc.Graph(figure=fig)


# -----------------------------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run(host='0.0.0.0', port=port, debug=False)

