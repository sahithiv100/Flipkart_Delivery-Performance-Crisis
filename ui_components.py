"""
Reusable UI Components, Themes, and Visual Styling for Flipkart Delivery Operations Prototype.
Features dark navy/charcoal styling with purple/indigo accents.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


CUSTOM_CSS = """
<style>
/* Main Dark Navy / Charcoal Theme */
.stApp {
    background-color: #0B0F19;
    color: #E2E8F0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #1F2937;
}

/* Metric Cards */
.metric-container {
    background: linear-gradient(135deg, #161E2E 0%, #1F293D 100%);
    border: 1px solid #374151;
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 14px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2);
    transition: transform 0.2s ease, border-color 0.2s ease;
}
.metric-container:hover {
    border-color: #8B5CF6;
    transform: translateY(-2px);
}
.metric-title {
    color: #94A3B8;
    font-size: 0.82rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 6px;
}
.metric-value {
    color: #F8FAFC;
    font-size: 1.85rem;
    font-weight: 700;
    line-height: 1.2;
}
.metric-sub {
    font-size: 0.78rem;
    margin-top: 5px;
}
.metric-sub.good { color: #10B981; }
.metric-sub.warning { color: #F59E0B; }
.metric-sub.danger { color: #EF4444; }
.metric-sub.neutral { color: #94A3B8; }

/* Synthetic Data Banner */
.synthetic-banner {
    background: linear-gradient(90deg, #1E1B4B 0%, #311042 100%);
    border: 1px solid #7C3AED;
    border-radius: 8px;
    padding: 10px 18px;
    margin-bottom: 22px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.synthetic-text {
    color: #E9D5FF;
    font-size: 0.88rem;
    font-weight: 600;
    letter-spacing: 0.02em;
}
.synthetic-pill {
    background-color: #7C3AED;
    color: #FFFFFF;
    font-size: 0.72rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 12px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Section Header Cards */
.section-card {
    background-color: #111827;
    border-left: 4px solid #8B5CF6;
    border-radius: 0 8px 8px 0;
    padding: 14px 20px;
    margin: 18px 0 16px 0;
    border-top: 1px solid #1F2937;
    border-right: 1px solid #1F2937;
    border-bottom: 1px solid #1F2937;
}

/* Priority & Status Badges */
.badge-p0 {
    background-color: rgba(239, 68, 68, 0.2);
    color: #F87171;
    border: 1px solid #EF4444;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 700;
}
.badge-p1 {
    background-color: rgba(245, 158, 11, 0.2);
    color: #FBBF24;
    border: 1px solid #F59E0B;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 700;
}
.badge-p2 {
    background-color: rgba(139, 92, 246, 0.2);
    color: #C4B5FD;
    border: 1px solid #8B5CF6;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 700;
}

/* Table styling override */
div[data-testid="stDataFrame"] {
    border: 1px solid #374151;
    border-radius: 8px;
    overflow: hidden;
}

/* Custom button accents */
div.stButton > button:first-child {
    background-color: #6D28D9;
    color: white;
    border: 1px solid #7C3AED;
    border-radius: 6px;
    font-weight: 600;
    transition: all 0.2s ease;
}
div.stButton > button:first-child:hover {
    background-color: #5B21B6;
    border-color: #8B5CF6;
    box-shadow: 0 0 10px rgba(139, 92, 246, 0.4);
}
</style>
"""


def apply_custom_css():
    """Inject custom dark navy styling into the Streamlit session."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_synthetic_banner():
    """Render mandatory synthetic data disclaimer banner."""
    st.markdown(
        """
        <div class="synthetic-banner">
            <div class="synthetic-text">
                ⚠️ <b>SYNTHETIC DEMO DATA — NOT REAL COMPANY DATA</b> | Illustrative Flipkart Operations Prototype. Fictional timestamps & records.
            </div>
            <div class="synthetic-pill">Synthetic Demo</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_kpi_card(title: str, value: str, subtext: str = "", status: str = "neutral"):
    """
    Render a styled KPI metric card.
    status options: 'good', 'warning', 'danger', 'neutral'
    """
    card_html = f"""
    <div class="metric-container">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-sub {status}">{subtext}</div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


def get_plotly_theme_layout():
    """Returns standardized dark layout dictionary for Plotly charts."""
    return dict(
        paper_bgcolor="#111827",
        plot_bgcolor="#161E2E",
        font=dict(color="#CBD5E1", family="Segoe UI, sans-serif"),
        title_font=dict(color="#F8FAFC", size=15),
        legend=dict(
            bgcolor="rgba(17, 24, 39, 0.7)",
            bordercolor="#374151",
            borderwidth=1,
            font=dict(color="#CBD5E1")
        ),
        xaxis=dict(
            gridcolor="#1F2937",
            linecolor="#374151",
            tickfont=dict(color="#94A3B8")
        ),
        yaxis=dict(
            gridcolor="#1F2937",
            linecolor="#374151",
            tickfont=dict(color="#94A3B8")
        ),
        margin=dict(l=40, r=30, t=50, b=40)
    )


def render_algorithm_flowchart():
    """
    Create a connected, interactive flowchart of the delivery diagnostic & optimization pipeline.
    """
    fig = go.Figure()

    # Step Nodes coordinates
    steps = [
        {"x": 1.0, "y": 3.0, "label": "<b>Step 1: Order Ingestion & Chronology</b><br>Validates 9 sequential milestones<br>(Pick -> Pack -> Dock -> Transit -> Attempt)", "color": "#6366F1"},
        {"x": 2.5, "y": 3.0, "label": "<b>Step 2: SLA & Stage Deconstruction</b><br>Measures pick, staging, transit & last-mile<br>against category SLA budgets", "color": "#8B5CF6"},
        {"x": 4.0, "y": 3.0, "label": "<b>Step 3: Root-Cause Attribution</b><br>Isolates bottleneck stage:<br>Shift Staffing | Congestion | Transit | Last-Mile", "color": "#A855F7"},
        {"x": 4.0, "y": 1.4, "label": "<b>Step 4: Pre-Delivery Late Risk ML</b><br>Random Forest trained on pre-delivery signals<br>(Staffing, Pick Hrs, Category, Distance)", "color": "#EC4899"},
        {"x": 2.5, "y": 1.4, "label": "<b>Step 5: Prescriptive Actions</b><br>Targeted interventions:<br>Shift Roster | Reroute Carrier | Wave Picking", "color": "#F59E0B"},
        {"x": 1.0, "y": 1.4, "label": "<b>Step 6: What-If Pilot Simulation</b><br>Recalculates OTD uplift, FADR & ROI<br>against cost ledger with human review", "color": "#10B981"}
    ]

    # Add connecting arrows
    arrows = [
        (1.0, 3.0, 2.5, 3.0),
        (2.5, 3.0, 4.0, 3.0),
        (4.0, 3.0, 4.0, 1.4),
        (4.0, 1.4, 2.5, 1.4),
        (2.5, 1.4, 1.0, 1.4)
    ]

    for x0, y0, x1, y1 in arrows:
        fig.add_annotation(
            x=x1, y=y1,
            ax=x0, ay=y0,
            xref="x", yref="y",
            axref="x", ayref="y",
            showarrow=True,
            arrowhead=3,
            arrowsize=1.5,
            arrowwidth=2.5,
            arrowcolor="#64748B"
        )

    for step in steps:
        fig.add_trace(go.Scatter(
            x=[step["x"]],
            y=[step["y"]],
            mode="markers+text",
            marker=dict(size=42, color=step["color"], line=dict(color="#FFFFFF", width=1.5)),
            text=[step["label"]],
            textposition="top center" if step["y"] > 2.0 else "bottom center",
            textfont=dict(size=11, color="#E2E8F0"),
            hoverinfo="text",
            hovertext=step["label"].replace("<br>", " "),
            showlegend=False
        ))

    fig.update_layout(
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0.2, 4.8]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0.4, 4.0]),
        height=380,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    return fig


def get_data_dictionary() -> pd.DataFrame:
    """Return comprehensive data dictionary for documentation and explorer."""
    dictionary_data = [
        {"Column": "order_id", "Type": "String", "Description": "Unique Flipkart synthetic order identifier (e.g. OD-FK-1002341).", "Operational Role": "Primary Key"},
        {"Column": "order_placed_at", "Type": "Datetime", "Description": "Customer checkout completion timestamp.", "Operational Role": "Journey Origin"},
        {"Column": "promised_delivery_date", "Type": "Datetime", "Description": "Committed SLA delivery deadline presented to customer at checkout.", "Operational Role": "SLA Benchmark"},
        {"Column": "final_delivery_at", "Type": "Datetime", "Description": "Actual doorstep delivery confirmation scan timestamp.", "Operational Role": "Terminal Milestone"},
        {"Column": "promised_delivery_hours", "Type": "Float", "Description": "Promised delivery duration budget in hours (24h to 96h).", "Operational Role": "Target SLA"},
        {"Column": "actual_total_duration_hours", "Type": "Float", "Description": "Elapsed hours from order placement to final delivery.", "Operational Role": "Performance Metric"},
        {"Column": "delivery_delay_hours", "Type": "Float", "Description": "Actual duration minus promised duration (negative = early, positive = late).", "Operational Role": "Variance KPI"},
        {"Column": "delay_status", "Type": "Categorical", "Description": "Binary compliance indicator: 'On-Time' vs 'Delayed'.", "Operational Role": "Primary Target"},
        {"Column": "warehouse_id", "Type": "String", "Description": "Origin fulfillment center code (e.g., BOM_Bhiwandi_FC, BLR_Malur_FC).", "Operational Role": "Fulfillment Node"},
        {"Column": "shift_name", "Type": "String", "Description": "FC operating shift during order processing (Shift-A, Shift-B, Shift-C Night).", "Operational Role": "Capacity Schedule"},
        {"Column": "shift_staffing_ratio", "Type": "Float", "Description": "Actual staffed workers divided by planned labor requirement (0.55 - 1.15).", "Operational Role": "Pre-delivery Signal"},
        {"Column": "stock_bin_location", "Type": "Categorical", "Description": "SKU storage zone (Primary Fast-Pick Bin, High-Bay Remote Bin, Cross-Dock).", "Operational Role": "Pick Difficulty"},
        {"Column": "carrier_id", "Type": "String", "Description": "Linehaul & last-mile logistics provider (Ekart, Delhivery, Shadowfax, etc.).", "Operational Role": "Logistics Partner"},
        {"Column": "product_category", "Type": "Categorical", "Description": "Merchandise vertical (Smartphones, Fashion, Home, Grocery, Appliances).", "Operational Role": "Handling Profile"},
        {"Column": "customer_region", "Type": "Categorical", "Description": "Destination geographic region (North, South, West, East, Central, North-East).", "Operational Role": "Territory Group"},
        {"Column": "customer_city_tier", "Type": "Categorical", "Description": "Market tier: Tier 1 (Metro), Tier 2 (Urban), Tier 3+ (Semi-Urban/Rural).", "Operational Role": "Infrastructure Context"},
        {"Column": "is_cross_region_split", "Type": "Boolean", "Description": "True if order had to be fulfilled from a non-local FC due to stockout.", "Operational Role": "Inventory Inefficiency"},
        {"Column": "route_distance_km", "Type": "Float", "Description": "Total linehaul overland transit distance from origin FC to delivery hub.", "Operational Role": "Transit Complexity"},
        {"Column": "pick_hours", "Type": "Float", "Description": "Duration from order receipt to pick & packing completion scan.", "Operational Role": "Warehouse Stage"},
        {"Column": "staging_hours", "Type": "Float", "Description": "Duration from packing completion to carrier truck dispatch scan.", "Operational Role": "Dock Stage"},
        {"Column": "transit_hours", "Type": "Float", "Description": "Duration from FC dock departure to destination city delivery hub scan.", "Operational Role": "Linehaul Stage"},
        {"Column": "lastmile_hours", "Type": "Float", "Description": "Duration from destination hub scan to customer doorstep delivery.", "Operational Role": "Last-Mile Stage"},
        {"Column": "bottleneck_stage", "Type": "Categorical", "Description": "Calculated primary operational stage causing the SLA breach.", "Operational Role": "Attribution Logic"},
        {"Column": "delivery_attempts", "Type": "Integer", "Description": "Total doorstep delivery attempts required (1, 2, or 3).", "Operational Role": "Fulfillment Friction"},
        {"Column": "first_attempt_success", "Type": "Boolean", "Description": "True if successfully delivered on the initial doorstep attempt (FADR).", "Operational Role": "Last-Mile Quality"},
        {"Column": "first_attempt_fail_reason", "Type": "String", "Description": "Logged cause when initial delivery attempt fails.", "Operational Role": "Failure Root Cause"},
        {"Column": "has_complaint", "Type": "Boolean", "Description": "True if customer logged a formal escalation or grievance.", "Operational Role": "Customer Impact"},
        {"Column": "complaint_category", "Type": "String", "Description": "Classification of customer grievance (e.g. Late Delivery Escalation).", "Operational Role": "Sentiment Impact"},
        {"Column": "cost_impact_inr", "Type": "Float", "Description": "Calculated monetary penalty, concession voucher, and reattempt overhead.", "Operational Role": "Financial Impact"},
        {"Column": "data_origin", "Type": "String", "Description": "Explicit synthetic demo flag: 'SYNTHETIC_DATA_DEMO'.", "Operational Role": "Compliance Label"}
    ]
    return pd.DataFrame(dictionary_data)
