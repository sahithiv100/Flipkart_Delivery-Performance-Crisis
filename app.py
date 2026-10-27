"""
Flipkart Delivery Performance Crisis - Interactive Operations Web Application
Author: Senior Operations Data Scientist & Full-Stack Developer
DISCLAIMER: ALL DATA IS 100% SYNTHETIC AND FOR DEMO/ANALYSIS PURPOSES ONLY.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date

# Direct root-level imports (no subdirectories)
from data_generator import generate_synthetic_orders
from analytics_engine import (
    compute_kpis,
    analyze_bottlenecks,
    analyze_warehouse_performance,
    analyze_carrier_performance,
    analyze_shift_performance,
    train_predelivery_risk_model,
    generate_targeted_recommendations,
    simulate_pilot_interventions,
)
from ui_components import (
    apply_custom_css,
    render_synthetic_banner,
    render_kpi_card,
    get_plotly_theme_layout,
    render_algorithm_flowchart,
    get_data_dictionary,
)

# Set page config
st.set_page_config(
    page_title="Flipkart Delivery Crisis Prototype | Synthetic Operations Intelligence",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply custom dark navy design styling
apply_custom_css()

# Session State Initialization for Data Generation
if "random_seed" not in st.session_state:
    st.session_state["random_seed"] = 42

if "sample_size" not in st.session_state:
    st.session_state["sample_size"] = 4000

if "raw_df" not in st.session_state:
    st.session_state["raw_df"] = generate_synthetic_orders(
        num_records=st.session_state["sample_size"],
        random_seed=st.session_state["random_seed"]
    )

# Sidebar: Global Controls & Navigation
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/delivery-box.png", width=64)
    st.title("Flipkart Operations")
    st.caption("Delivery Crisis Diagnostic & Pilot Engine")
    
    st.markdown("---")
    st.subheader("🧭 Navigation")
    pages = [
        "📊 Executive Overview",
        "🔍 Bottleneck Deep-Dive",
        "🚨 Late-Order Risk Queue (ML)",
        "💡 Targeted Recommendations",
        "🎛️ What-If Pilot Simulator",
        "❓ Manager Exploration Suite",
        "🧭 How the Algorithm Works",
        "🗃️ Data Explorer & Dictionary"
    ]
    selected_page = st.radio("Go to Page:", pages, index=0)
    
    st.markdown("---")
    st.subheader("⚙️ Synthetic Data Controls")
    
    seed_input = st.number_input(
        "Random Generator Seed",
        min_value=1,
        max_value=9999,
        value=st.session_state["random_seed"],
        step=1
    )
    
    sample_input = st.slider(
        "Order Sample Size",
        min_value=1500,
        max_value=6000,
        value=st.session_state["sample_size"],
        step=500
    )
    
    if st.button("🔄 Regenerate Synthetic Data", use_container_width=True):
        st.session_state["random_seed"] = seed_input
        st.session_state["sample_size"] = sample_input
        st.session_state["raw_df"] = generate_synthetic_orders(
            num_records=sample_input,
            random_seed=seed_input
        )
        st.success(f"Generated {sample_input} fresh synthetic orders!")
        st.rerun()
        
    st.markdown("---")
    st.subheader("🔎 Operational Filters")
    
    df_raw = st.session_state["raw_df"]
    
    # Date Range Filter
    min_date = df_raw["order_placed_at"].dt.date.min()
    max_date = df_raw["order_placed_at"].dt.date.max()
    date_range = st.date_input(
        "Order Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # FC Filter
    all_fcs = sorted(df_raw["warehouse_id"].unique().tolist())
    selected_fcs = st.multiselect("Origin Fulfillment Center (FC)", all_fcs, default=all_fcs)
    
    # Carrier Filter
    all_carriers = sorted(df_raw["carrier_id"].unique().tolist())
    selected_carriers = st.multiselect("Logistics Carrier", all_carriers, default=all_carriers)
    
    # Region Filter
    all_regions = sorted(df_raw["customer_region"].unique().tolist())
    selected_regions = st.multiselect("Destination Region", all_regions, default=all_regions)
    
    # Category Filter
    all_categories = sorted(df_raw["product_category"].unique().tolist())
    selected_categories = st.multiselect("Product Category", all_categories, default=all_categories)
    
    # Shift Filter
    all_shifts = sorted(df_raw["shift_name"].unique().tolist())
    selected_shifts = st.multiselect("FC Shift", all_shifts, default=all_shifts)
    
    # Delay Status
    delay_filter = st.selectbox("Delivery SLA Status", ["All Orders", "Delayed Only", "On-Time Only"])
    
    if st.button("↺ Reset All Filters", use_container_width=True):
        st.rerun()
        
    st.markdown("---")
    st.caption("🔒 **Prototype Compliance**: All entities, volumes, and metrics are synthetic approximations. No internal Flipkart APIs accessed.")

# Filter Data according to user selections
filtered_df = df_raw.copy()

# Date filter
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_d, end_d = date_range
    filtered_df = filtered_df[
        (filtered_df["order_placed_at"].dt.date >= start_d) &
        (filtered_df["order_placed_at"].dt.date <= end_d)
    ]

# Multi-select filters
if selected_fcs:
    filtered_df = filtered_df[filtered_df["warehouse_id"].isin(selected_fcs)]
if selected_carriers:
    filtered_df = filtered_df[filtered_df["carrier_id"].isin(selected_carriers)]
if selected_regions:
    filtered_df = filtered_df[filtered_df["customer_region"].isin(selected_regions)]
if selected_categories:
    filtered_df = filtered_df[filtered_df["product_category"].isin(selected_categories)]
if selected_shifts:
    filtered_df = filtered_df[filtered_df["shift_name"].isin(selected_shifts)]

if delay_filter == "Delayed Only":
    filtered_df = filtered_df[filtered_df["is_delayed"] == True]
elif delay_filter == "On-Time Only":
    filtered_df = filtered_df[filtered_df["is_delayed"] == False]

# Top Banner
render_synthetic_banner()

# Empty State Warning
if filtered_df.empty:
    st.warning("⚠️ No records match the active filter criteria. Please broaden your sidebar filters or click 'Reset All Filters'.")
    st.stop()

# Compute Global KPIs on filtered data
kpis = compute_kpis(filtered_df)

# ==============================================================================
# PAGE 1: EXECUTIVE OVERVIEW
# ==============================================================================
if selected_page == "📊 Executive Overview":
    st.title("Delivery Performance Crisis: Executive Overview")
    st.markdown(
        """
        **Context:** During high-velocity seasonal sales surges, Flipkart's logistics ecosystem experiences 
        localized delivery delays that degrade customer trust, inflate repeat delivery attempts, and generate customer escalations. 
        This prototype deconstructs the end-to-end order journey to pinpoint root causes across 
        **warehouse staffing, dock staging, carrier linehaul, and doorstep attempts**.
        """
    )
    
    # Executive KPI Cards Row
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        render_kpi_card("Total Orders", f"{kpis['total_orders']:,}", "Filtered volume", "neutral")
    with c2:
        otd_val = kpis['on_time_pct']
        otd_status = "good" if otd_val >= 90.0 else ("warning" if otd_val >= 80.0 else "danger")
        render_kpi_card("On-Time Delivery", f"{otd_val}%", "Target: 92.0%", otd_status)
    with c3:
        fadr_val = kpis['fadr_pct']
        fadr_status = "good" if fadr_val >= 85.0 else ("warning" if fadr_val >= 78.0 else "danger")
        render_kpi_card("First-Attempt Success", f"{fadr_val}%", "Target: 88.0%", fadr_status)
    with c4:
        render_kpi_card("Avg Delay Hours", f"{kpis['avg_delay_hours']} hrs", "For delayed cohort", "warning")
    with c5:
        comp_val = kpis['complaint_pct']
        comp_status = "good" if comp_val <= 3.0 else ("warning" if comp_val <= 6.0 else "danger")
        render_kpi_card("Complaint Rate", f"{comp_val}%", "Target: < 2.5%", comp_status)
    with c6:
        render_kpi_card("Est. Cost Impact", f"₹{kpis['total_cost_impact_lakhs']} L", "Concessions & overhead", "danger")
        
    st.markdown("---")
    
    # Two Columns: Daily Trend and Regional Breakdown
    col_left, col_right = st.columns([6, 5])
    
    with col_left:
        st.subheader("Daily On-Time Delivery Rate & Delay Volume Trend")
        daily_summary = filtered_df.copy()
        daily_summary["order_date"] = daily_summary["order_placed_at"].dt.date
        trend_df = daily_summary.groupby("order_date").agg(
            total=("order_id", "count"),
            delayed=("is_delayed", "sum")
        ).reset_index()
        trend_df["on_time_pct"] = ((trend_df["total"] - trend_df["delayed"]) / trend_df["total"] * 100.0).round(1)
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Bar(
            x=trend_df["order_date"],
            y=trend_df["delayed"],
            name="Delayed Orders (Vol)",
            marker_color="#EF4444",
            opacity=0.6,
            yaxis="y2"
        ))
        fig_trend.add_trace(go.Scatter(
            x=trend_df["order_date"],
            y=trend_df["on_time_pct"],
            name="On-Time Delivery %",
            line=dict(color="#8B5CF6", width=3),
            mode="lines+markers",
            yaxis="y"
        ))
        fig_trend.add_hline(y=92.0, line_dash="dash", line_color="#10B981", annotation_text="92% Target SLA", annotation_position="top left")
        
        layout_dict = get_plotly_theme_layout()
        layout_dict["yaxis"] = dict(title="On-Time Delivery %", range=[60, 100], gridcolor="#1F2937")
        layout_dict["yaxis2"] = dict(title="Delayed Volume", overlaying="y", side="right", showgrid=False)
        layout_dict["legend"] = dict(x=0.01, y=0.05, bgcolor="rgba(17, 24, 39, 0.8)")
        fig_trend.update_layout(**layout_dict)
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with col_right:
        st.subheader("Destination Region Performance Comparison")
        reg_df = filtered_df.groupby("customer_region").agg(
            total=("order_id", "count"),
            delayed=("is_delayed", "sum"),
            avg_delay=("delivery_delay_hours", "mean"),
            cost=("cost_impact_inr", "sum")
        ).reset_index()
        reg_df["on_time_pct"] = ((reg_df["total"] - reg_df["delayed"]) / reg_df["total"] * 100.0).round(1)
        reg_df["cost_lakhs"] = (reg_df["cost"] / 100000.0).round(2)
        reg_df = reg_df.sort_values(by="on_time_pct", ascending=True)
        
        fig_reg = px.bar(
            reg_df,
            x="on_time_pct",
            y="customer_region",
            orientation="h",
            color="on_time_pct",
            color_continuous_scale=["#EF4444", "#F59E0B", "#10B981"],
            text="on_time_pct",
            hover_data=["total", "avg_delay", "cost_lakhs"],
            labels={"on_time_pct": "On-Time %", "customer_region": "Customer Region"}
        )
        fig_reg.update_traces(texttemplate="%{text}%", textposition="outside")
        fig_reg.update_layout(**get_plotly_theme_layout(), height=340)
        st.plotly_chart(fig_reg, use_container_width=True)
        
    # Crisis Summary Callout
    st.markdown(
        """
        <div class="section-card">
            <h4 style="margin: 0 0 6px 0; color: #C4B5FD;">🚨 Executive Briefing Notes</h4>
            <p style="margin: 0; color: #94A3B8; font-size: 0.9rem;">
                • <b>Primary Crisis Driver:</b> Fulfillment Center night shifts (Shift-C) operate at a severe staffing deficit (mean 76% ratio), causing dock staging backlogs that delay linehaul truck departures.<br>
                • <b>Logistics Friction:</b> 3PL carriers Shadowfax and Xpressbees experience high first-attempt delivery failure in Tier-3+ pincodes due to phone unreachable and ambiguous pincodes.<br>
                • <b>Capital Impact:</b> Projected annualized breach concession vouchers and re-attempt fuel surcharges exceed <b>₹2.5 Crore</b> if left unmitigated.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==============================================================================
# PAGE 2: BOTTLENECK DEEP-DIVE
# ==============================================================================
elif selected_page == "🔍 Bottleneck Deep-Dive":
    st.title("Bottleneck Deep-Dive & Journey Breakdown")
    st.markdown("Isolate where order delay budget is consumed: **Warehouse Picking**, **Dock Staging**, **Linehaul Transit**, or **Last-Mile Attempts**.")
    
    bottleneck_df = analyze_bottlenecks(filtered_df)
    
    col1, col2 = st.columns([5, 5])
    with col1:
        st.subheader("Delay Stage Bottleneck Attribution")
        if not bottleneck_df.empty:
            fig_pie = px.pie(
                bottleneck_df,
                names="bottleneck_stage",
                values="count",
                color="bottleneck_stage",
                color_discrete_map={
                    "Warehouse Pick & Pack": "#8B5CF6",
                    "Dock Staging & Manifest": "#EC4899",
                    "Linehaul Transit": "#3B82F6",
                    "Last-Mile & Delivery Attempts": "#F59E0B",
                    "Inventory Split-Shipment": "#10B981"
                },
                hole=0.45
            )
            fig_pie.update_traces(textinfo="percent+label", hoverinfo="label+value+percent")
            fig_pie.update_layout(**get_plotly_theme_layout(), height=360)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No delayed orders in current filter selection.")
            
    with col2:
        st.subheader("Average Delay & Financial Impact by Stage")
        if not bottleneck_df.empty:
            fig_bar = px.bar(
                bottleneck_df,
                x="bottleneck_stage",
                y="avg_delay_hours",
                color="total_cost_lakhs",
                color_continuous_scale="Purples",
                text="avg_delay_hours",
                labels={"avg_delay_hours": "Avg Delay (Hrs)", "bottleneck_stage": "Stage", "total_cost_lakhs": "Cost (₹ Lakhs)"}
            )
            fig_bar.update_traces(texttemplate="%{text} hrs", textposition="outside")
            fig_bar.update_layout(**get_plotly_theme_layout(), height=360)
            st.plotly_chart(fig_bar, use_container_width=True)
            
    st.markdown("---")
    
    # Warehouse and Shift Analysis
    st.subheader("Origin Fulfillment Center Benchmarking")
    wh_df = analyze_warehouse_performance(filtered_df)
    
    col_wh1, col_wh2 = st.columns([6, 4])
    with col_wh1:
        st.dataframe(
            wh_df.style.format({
                "on_time_pct": "{:.1f}%",
                "avg_pick_hours": "{:.2f} hrs",
                "avg_staging_hours": "{:.2f} hrs",
                "avg_staffing_ratio": "{:.2f}",
                "cost_impact_lakhs": "₹{:.2f} L"
            }).background_gradient(subset=["on_time_pct"], cmap="RdYlGn"),
            use_container_width=True,
            hide_index=True
        )
    with col_wh2:
        fig_scatter = px.scatter(
            wh_df,
            x="avg_staffing_ratio",
            y="avg_staging_hours",
            size="total_orders",
            color="warehouse_id",
            text="warehouse_id",
            labels={"avg_staffing_ratio": "Staffing Ratio", "avg_staging_hours": "Staging Delay (hrs)"},
            title="Staffing Ratio vs Dock Staging Delay"
        )
        fig_scatter.update_traces(textposition="top center")
        fig_scatter.update_layout(**get_plotly_theme_layout(), height=320)
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    st.markdown("---")
    
    # Carrier Benchmarking & First-Attempt Failure Pareto
    c_left, c_right = st.columns([5, 5])
    with c_left:
        st.subheader("Logistics Carrier Benchmarking")
        carrier_df = analyze_carrier_performance(filtered_df)
        st.dataframe(
            carrier_df.style.format({
                "on_time_pct": "{:.1f}%",
                "fadr_pct": "{:.1f}%",
                "complaint_rate_pct": "{:.1f}%",
                "avg_transit_hours": "{:.1f} hrs",
                "avg_speed_kmh": "{:.1f} km/h"
            }).background_gradient(subset=["on_time_pct"], cmap="Blues"),
            use_container_width=True,
            hide_index=True
        )
        
    with c_right:
        st.subheader("First-Attempt Failure Reasons (Pareto)")
        failed_attempts = filtered_df[filtered_df["first_attempt_success"] == False]
        if not failed_attempts.empty:
            fail_counts = failed_attempts["first_attempt_fail_reason"].value_counts().reset_index()
            fail_counts.columns = ["reason", "count"]
            fail_counts["pct"] = (fail_counts["count"] / fail_counts["count"].sum() * 100.0).round(1)
            
            fig_fail = px.bar(
                fail_counts,
                x="count",
                y="reason",
                orientation="h",
                text="pct",
                color="count",
                color_continuous_scale="Reds",
                labels={"count": "Failed Attempts", "reason": "Failure Reason"}
            )
            fig_fail.update_traces(texttemplate="%{text}%", textposition="outside")
            fig_fail.update_layout(**get_plotly_theme_layout(), height=320)
            st.plotly_chart(fig_fail, use_container_width=True)
        else:
            st.info("No failed first attempts in the current selection.")

# ==============================================================================
# PAGE 3: LATE-ORDER RISK QUEUE (ML ENGINE)
# ==============================================================================
elif selected_page == "🚨 Late-Order Risk Queue (ML)":
    st.title("Pre-Delivery Late Risk Early Warning Engine")
    st.markdown(
        """
        **Methodology:** A Random Forest Classifier is trained **strictly on pre-delivery signals** 
        (warehouse shift staffing, pick duration, dock staging time, route distance, category, and carrier) 
        before the shipment reaches the destination city. This flags at-risk shipments early enough for proactive dispatch rerouting.
        """
    )
    
    with st.spinner("Training Pre-Delivery Classifier & Scoring Order Queue..."):
        ml_results = train_predelivery_risk_model(filtered_df, random_seed=st.session_state["random_seed"])
        
    if ml_results is None:
        st.warning("⚠️ Insufficient sample size or lack of class variance to train the classifier. Expand your filters.")
    else:
        rf_metrics = ml_results["rf_metrics"]
        dummy_metrics = ml_results["dummy_metrics"]
        
        # Transparent Model Metrics vs Baseline
        st.subheader("Model Diagnostic Metrics vs Transparent Baseline")
        st.caption("ℹ️ Accuracy alone is deceptive for imbalanced operations data. We evaluate Precision, Recall, F1, and ROC-AUC against a zero-rule dummy baseline.")
        
        m1, m2, m3, m4, m5 = st.columns(5)
        with m1:
            render_kpi_card("ROC-AUC Score", f"{rf_metrics['roc_auc']}", "Baseline: 0.500", "good")
        with m2:
            render_kpi_card("Model Recall", f"{round(rf_metrics['recall']*100, 1)}%", "Catches late orders", "good")
        with m3:
            render_kpi_card("Model Precision", f"{round(rf_metrics['precision']*100, 1)}%", "Reliability of alert", "neutral")
        with m4:
            render_kpi_card("Model F1-Score", f"{rf_metrics['f1']}", f"Dummy F1: {dummy_metrics['f1']}", "good")
        with m5:
            render_kpi_card("Test Set Size", f"{rf_metrics['test_size']:,}", f"Train Set: {rf_metrics['train_size']:,}", "neutral")
            
        col_feat, col_cm = st.columns([6, 4])
        with col_feat:
            st.subheader("Key Pre-Delivery Early Warning Features")
            fi_df = ml_results["feature_importance"]
            fig_fi = px.bar(
                fi_df,
                x="importance",
                y="feature",
                orientation="h",
                color="importance",
                color_continuous_scale="Purples",
                labels={"importance": "Gini Feature Importance", "feature": "Pre-Delivery Signal"}
            )
            fig_fi.update_layout(**get_plotly_theme_layout(), height=340)
            st.plotly_chart(fig_fi, use_container_width=True)
            
        with col_cm:
            st.subheader("Confusion Matrix (Holdout Test)")
            cm = np.array(rf_metrics["confusion_matrix"])
            fig_cm = px.imshow(
                cm,
                text_auto=True,
                labels=dict(x="Predicted Class", y="Actual Truth", color="Count"),
                x=["Predicted On-Time", "Predicted Late"],
                y=["Actual On-Time", "Actual Late"],
                color_continuous_scale="Blues"
            )
            fig_cm.update_layout(**get_plotly_theme_layout(), height=340)
            st.plotly_chart(fig_cm, use_container_width=True)
            
        st.markdown("---")
        
        # Scored Queue Table
        st.subheader("Live At-Risk Order Prioritization Queue")
        scored_df = ml_results["scored_df"]
        
        # Queue Filters
        q_col1, q_col2, q_col3 = st.columns([4, 4, 4])
        with q_col1:
            risk_filter = st.multiselect("Filter by Predicted Risk Level:", ["High Risk", "Medium Risk", "Low Risk"], default=["High Risk"])
        with q_col2:
            min_score = st.slider("Minimum Risk Score Threshold", 0.0, 1.0, 0.60, 0.05)
            
        queue_view = scored_df[
            (scored_df["predicted_risk_level"].isin(risk_filter)) &
            (scored_df["predelivery_risk_score"] >= min_score)
        ][[
            "order_id", "predelivery_risk_score", "predicted_risk_level",
            "warehouse_id", "carrier_id", "product_category", "customer_region",
            "route_distance_km", "shift_staffing_ratio", "pick_hours", "staging_hours"
        ]].sort_values(by="predelivery_risk_score", ascending=False).reset_index(drop=True)
        
        with q_col3:
            st.metric("Orders Flagged in Queue", f"{len(queue_view):,}")
            
        st.dataframe(
            queue_view.style.format({
                "predelivery_risk_score": "{:.3f}",
                "route_distance_km": "{:.1f} km",
                "shift_staffing_ratio": "{:.2f}",
                "pick_hours": "{:.2f} hrs",
                "staging_hours": "{:.2f} hrs"
            }).background_gradient(subset=["predelivery_risk_score"], cmap="YlOrRd"),
            use_container_width=True,
            height=300
        )
        
        # Download Queue CSV
        csv_queue = queue_view.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download At-Risk Queue for Operations Dispatch (CSV)",
            data=csv_queue,
            file_name="flipkart_at_risk_orders_queue.csv",
            mime="text/csv",
            use_container_width=True
        )

# ==============================================================================
# PAGE 4: TARGETED RECOMMENDATIONS & ACTION PLAN
# ==============================================================================
elif selected_page == "💡 Targeted Recommendations":
    st.title("Targeted Operational Recommendations & Governance")
    st.markdown(
        """
        These recommendations are synthesized directly from actual computed network bottlenecks. 
        **Human Review Protocol:** In compliance with corporate safety and labor policies, high-impact recommendations 
        require human managerial sign-off before operational deployment.
        """
    )
    
    recommendations = generate_targeted_recommendations(filtered_df)
    
    for rec in recommendations:
        badge_class = "badge-p0" if "P0" in rec["priority"] else ("badge-p1" if "P1" in rec["priority"] else "badge-p2")
        review_badge = "🔴 Human Review Required" if rec["human_review_required"] else "🟢 Automated Execution Safe"
        
        st.markdown(
            f"""
            <div class="metric-container" style="border-left: 5px solid #8B5CF6; margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <div>
                        <span class="{badge_class}">{rec['priority']}</span>
                        <span style="color: #A78BFA; font-weight: 700; margin-left: 10px; font-size: 1.1rem;">{rec['id']}: {rec['title']}</span>
                    </div>
                    <span style="font-size: 0.8rem; font-weight: 600; color: #E2E8F0;">{review_badge}</span>
                </div>
                <div style="color: #94A3B8; font-size: 0.88rem; margin-bottom: 8px;">
                    <b>Target Domain:</b> {rec['domain']} | <b>Target Node / Cohort:</b> {rec['target']}
                </div>
                <div style="background-color: #111827; border-radius: 6px; padding: 10px 14px; margin-bottom: 10px;">
                    <div style="color: #F8FAFC; font-size: 0.88rem; margin-bottom: 6px;"><b>Empirical Evidence:</b> {rec['evidence']}</div>
                    <div style="color: #E9D5FF; font-size: 0.88rem; margin-bottom: 6px;"><b>Prescriptive Action:</b> {rec['action']}</div>
                    <div style="color: #10B981; font-size: 0.88rem; margin-bottom: 6px;"><b>Expected Impact:</b> {rec['expected_impact']}</div>
                    <div style="color: #94A3B8; font-size: 0.82rem;"><b>Core Assumptions:</b> {rec['assumptions']}</div>
                    <div style="color: #F59E0B; font-size: 0.82rem;"><b>Uncertainty / Risk:</b> {rec['uncertainty']}</div>
                </div>
                <div style="font-size: 0.8rem; color: #64748B;">
                    <b>Governance & Safety Sign-off:</b> {rec['governance_note']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    st.markdown("---")
    st.subheader("Implementation Governance & Stakeholder Matrix")
    governance_table = pd.DataFrame([
        {"Workstream": "Warehouse Shift Staffing", "Primary Lead": "FC General Manager", "SLA Sign-off": "VP Operations", "Check Frequency": "Daily Roster Review", "Risk Level": "High (Labor Safety)"},
        {"Workstream": "Carrier Volume Rebalancing", "Primary Lead": "Logistics Sourcing Lead", "SLA Sign-off": "Director Logistics", "Check Frequency": "Weekly Dynamic Allocation", "Risk Level": "Medium (Contract SLA)"},
        {"Workstream": "Regional Stock Pre-Positioning", "Primary Lead": "Inventory Planning Head", "SLA Sign-off": "Chief Commercial Officer", "Check Frequency": "Bi-weekly Replenishment", "Risk Level": "Medium (Carrying Cost)"},
        {"Workstream": "Pre-delivery WhatsApp Verification", "Primary Lead": "Customer Experience Product Lead", "SLA Sign-off": "VP Product", "Check Frequency": "Automated Continuous", "Risk Level": "Low (Standard Comms)"}
    ])
    st.dataframe(governance_table, use_container_width=True, hide_index=True)

# ==============================================================================
# PAGE 5: WHAT-IF PILOT SIMULATOR
# ==============================================================================
elif selected_page == "🎛️ What-If Pilot Simulator":
    st.title("What-If Pilot Intervention Simulator")
    st.markdown(
        """
        Model the operational and financial impact of rolling out targeted interventions across warehouse shifts, 
        regional stock placement, carrier quotas, and last-mile address pre-validation.
        """
    )
    
    st.subheader("🎛️ Configure Pilot Intervention Levers")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        staffing_uplift = st.slider("FC Shift-C Flex Staffing Uplift (%)", 0, 35, 20, 5, help="Adds contract flex labor to night shifts at bottleneck FCs.")
        inv_rebalance = st.slider("Regional Inventory Rebalancing (%)", 0, 50, 25, 5, help="Pre-positions fast-moving SKUs into regional Mother Hubs to eliminate cross-region splits.")
    with col_s2:
        carrier_shift = st.slider("Dynamic Carrier Volume Re-allocation (%)", 0, 40, 20, 5, help="Shifts volume from low-performing 3PL carriers to top-performing Ekart and BlueDart routes.")
        address_preval = st.slider("WhatsApp Address Pre-Validation (%)", 0, 50, 30, 5, help="Dispatches pre-delivery location pin confirmation to resolve ambiguous pincodes.")
        
    sim_res = simulate_pilot_interventions(
        filtered_df,
        staffing_boost_pct=staffing_uplift,
        inventory_rebalance_pct=inv_rebalance,
        carrier_reallocation_pct=carrier_shift,
        address_preval_pct=address_preval
    )
    
    st.markdown("---")
    st.subheader("Simulated Before vs After Operational Performance")
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        delta_otd = sim_res["delta_ontime_pct"]
        render_kpi_card(
            "On-Time Delivery",
            f"{sim_res['simulated_ontime_pct']}%",
            f"Baseline: {sim_res['baseline_ontime_pct']}% ({'+' if delta_otd>=0 else ''}{delta_otd}%)",
            "good" if delta_otd > 0 else "neutral"
        )
    with m2:
        delta_fadr = sim_res["delta_fadr_pct"]
        render_kpi_card(
            "First-Attempt Rate (FADR)",
            f"{sim_res['simulated_fadr_pct']}%",
            f"Baseline: {sim_res['baseline_fadr_pct']}% ({'+' if delta_fadr>=0 else ''}{delta_fadr}%)",
            "good" if delta_fadr > 0 else "neutral"
        )
    with m3:
        delta_comp = sim_res["delta_complaint_pct"]
        render_kpi_card(
            "Complaint Rate",
            f"{sim_res['simulated_complaint_pct']}%",
            f"Baseline: {sim_res['baseline_complaint_pct']}% ({delta_comp}%)",
            "good" if delta_comp < 0 else "neutral"
        )
    with m4:
        render_kpi_card(
            "Orders Delayed Saved",
            f"{sim_res['delayed_orders_saved']:,}",
            f"Re-attempts saved: {sim_res['reattempts_saved']:,}",
            "good"
        )
        
    st.markdown("---")
    
    # Financial Cost-Benefit Ledger
    st.subheader("Financial Ledger: Pilot Cost vs Economic Savings")
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        render_kpi_card("Monthly Pilot Cost", f"₹{sim_res['total_intervention_cost_lakhs']} L", "Staffing, tech & holding", "neutral")
    with f2:
        render_kpi_card("Gross Economic Savings", f"₹{sim_res['gross_savings_lakhs']} L", "Concessions & reattempts", "good")
    with f3:
        net_status = "good" if sim_res['net_benefit_lakhs'] >= 0 else "danger"
        render_kpi_card("Net Economic Benefit", f"₹{sim_res['net_benefit_lakhs']} L", "Net monthly margin boost", net_status)
    with f4:
        render_kpi_card("Pilot ROI Multiplier", f"{sim_res['roi_multiplier']}x", "Return on operations spend", "good")
        
    # Visual comparison chart
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        comp_df = pd.DataFrame({
            "Metric": ["On-Time Delivery %", "First-Attempt Success %", "Complaint Escalation %"],
            "Baseline": [sim_res["baseline_ontime_pct"], sim_res["baseline_fadr_pct"], sim_res["baseline_complaint_pct"]],
            "Simulated Pilot": [sim_res["simulated_ontime_pct"], sim_res["simulated_fadr_pct"], sim_res["simulated_complaint_pct"]]
        })
        fig_comp = px.bar(
            comp_df,
            x="Metric",
            y=["Baseline", "Simulated Pilot"],
            barmode="group",
            color_discrete_sequence=["#64748B", "#8B5CF6"],
            title="Baseline vs Simulated Performance Metrics"
        )
        fig_comp.update_layout(**get_plotly_theme_layout(), height=340)
        st.plotly_chart(fig_comp, use_container_width=True)
        
    with col_chart2:
        # Waterfall or Ledger Breakdown
        ledger_df = pd.DataFrame({
            "Component": ["Pilot Investment Cost", "SLA Concession Savings", "Reattempt Fuel Savings", "Churn Prevention", "Net Margin"],
            "Amount_Lakhs": [
                -sim_res["total_intervention_cost_lakhs"],
                round((sim_res["delayed_orders_saved"] * 165.0)/100000.0, 2),
                round((sim_res["reattempts_saved"] * 75.0)/100000.0, 2),
                round((sim_res["complaints_prevented"] * 320.0)/100000.0, 2),
                sim_res["net_benefit_lakhs"]
            ]
        })
        fig_ledger = px.bar(
            ledger_df,
            x="Component",
            y="Amount_Lakhs",
            color="Amount_Lakhs",
            color_continuous_scale=["#EF4444", "#10B981"],
            text="Amount_Lakhs",
            title="Monthly Pilot Economic Ledger (₹ Lakhs)"
        )
        fig_ledger.update_traces(texttemplate="₹%{text} L", textposition="outside")
        fig_ledger.update_layout(**get_plotly_theme_layout(), height=340)
        st.plotly_chart(fig_ledger, use_container_width=True)

# ==============================================================================
# PAGE 6: MANAGER EXPLORATION SUITE
# ==============================================================================
elif selected_page == "❓ Manager Exploration Suite":
    st.title("Operations Manager Exploration Suite")
    st.markdown("Investigate three strategic operational questions with interactive controls and grounded data analysis.")
    
    tab1, tab2, tab3 = st.tabs([
        "Question 1: Warehouse Shift Deficits",
        "Question 2: Last-Mile vs Warehouse Origin",
        "Question 3: High-Value SKU Misallocation"
    ])
    
    # QUESTION 1
    with tab1:
        st.subheader("Which warehouse shift is causing the most downstream carrier SLA misses, and why?")
        st.markdown(
            """
            **Managerial Context:** In multi-shift 24/7 fulfillment centers, shift handovers and night staffing deficits 
            frequently result in dock manifest delays, forcing morning linehaul dispatch vehicles to leave empty or delayed.
            """
        )
        shift_df = analyze_shift_performance(filtered_df)
        st.dataframe(
            shift_df.style.format({
                "delay_rate_pct": "{:.1f}%",
                "on_time_pct": "{:.1f}%",
                "avg_staffing_ratio": "{:.2f}",
                "avg_pick_hours": "{:.2f} hrs",
                "avg_staging_hours": "{:.2f} hrs"
            }).background_gradient(subset=["delay_rate_pct"], cmap="Reds"),
            use_container_width=True,
            hide_index=True
        )
        
        # Interactive FC Shift Inspector
        st.markdown("#### Interactive FC Shift Delay Inspector")
        sel_fc = st.selectbox("Select Fulfillment Center to Inspect:", sorted(filtered_df["warehouse_id"].unique()))
        sub_fc = filtered_df[filtered_df["warehouse_id"] == sel_fc]
        fig_fc_shift = px.box(
            sub_fc,
            x="shift_code",
            y="staging_hours",
            color="shift_code",
            points="all",
            labels={"staging_hours": "Dock Staging Duration (Hours)", "shift_code": "Warehouse Shift"},
            title=f"Dock Staging Time Variance by Shift for {sel_fc}"
        )
        fig_fc_shift.update_layout(**get_plotly_theme_layout(), height=340)
        st.plotly_chart(fig_fc_shift, use_container_width=True)
        st.info("💡 **Finding:** Shift-C (Night 22:00-06:00) exhibits chronic understaffing (~76% staffing ratio) and high staging delays. Staged pallets miss the 04:30 AM linehaul trunk departures, compounding downstream delays.")
        
    # QUESTION 2
    with tab2:
        st.subheader("Is our delivery crisis caused by last-mile carrier failure or warehouse dispatch delays?")
        st.markdown(
            """
            **Managerial Context:** Operations teams often blame 3PL carriers for late deliveries, while logistics partners argue 
            that packages were handed over late from the fulfillment dock.
            """
        )
        
        tier_choice = st.radio("Compare Market Context:", ["All Markets", "Tier 1 (Metro)", "Tier 3+ (Semi-Urban/Rural)"], horizontal=True)
        tier_df = filtered_df.copy()
        if tier_choice != "All Markets":
            tier_df = tier_df[tier_df["customer_city_tier"] == tier_choice]
            
        stage_means = pd.DataFrame({
            "Stage": ["Warehouse Pick & Pack", "Dock Staging & Handover", "Linehaul Transit", "Last-Mile Delivery"],
            "Average_Hours": [
                tier_df["pick_hours"].mean(),
                tier_df["staging_hours"].mean(),
                tier_df["transit_hours"].mean(),
                tier_df["lastmile_hours"].mean()
            ]
        })
        fig_stages = px.bar(
            stage_means,
            x="Stage",
            y="Average_Hours",
            color="Average_Hours",
            color_continuous_scale="Purples",
            text="Average_Hours",
            labels={"Average_Hours": "Mean Hours Consumed"}
        )
        fig_stages.update_traces(texttemplate="%{text:.1f} hrs", textposition="outside")
        fig_stages.update_layout(**get_plotly_theme_layout(), height=340)
        st.plotly_chart(fig_stages, use_container_width=True)
        st.info("💡 **Finding:** In **Tier 1 Metros**, warehouse staging accounts for ~42% of total controllable delay. In **Tier 3+ Markets**, however, transit distance and failed first-attempts dominate the delay budget.")
        
    # QUESTION 3
    with tab3:
        st.subheader("Which high-value SKUs suffer the most customer escalations due to stock misallocation?")
        st.markdown(
            """
            **Managerial Context:** When high-value electronics run out of stock in regional hubs, orders are fulfilled 
            via cross-region splits from distant FCs, causing severe customer escalations.
            """
        )
        cat_analysis = filtered_df.groupby("product_category").agg(
            total_orders=("order_id", "count"),
            split_shipment_pct=("is_cross_region_split", lambda x: round(x.mean() * 100.0, 1)),
            on_time_pct=("is_delayed", lambda x: round((1.0 - x.mean()) * 100.0, 1)),
            complaint_pct=("has_complaint", lambda x: round(x.mean() * 100.0, 1)),
            avg_distance_km=("route_distance_km", "mean")
        ).reset_index()
        
        st.dataframe(
            cat_analysis.style.format({
                "split_shipment_pct": "{:.1f}%",
                "on_time_pct": "{:.1f}%",
                "complaint_pct": "{:.1f}%",
                "avg_distance_km": "{:.1f} km"
            }).background_gradient(subset=["complaint_pct"], cmap="Oranges"),
            use_container_width=True,
            hide_index=True
        )
        st.info("💡 **Finding:** **Smartphones & Electronics** exhibit the highest customer sensitivity. Cross-regional fulfillment increases transit distance 4.2x, leading to a 3.1x surge in customer escalation tickets.")

# ==============================================================================
# PAGE 7: HOW THE ALGORITHM WORKS
# ==============================================================================
elif selected_page == "🧭 How the Algorithm Works":
    st.title("Algorithmic Architecture & Validation Logic")
    st.markdown("Connected diagnostic pipeline for order journey analysis, SLA deconstruction, and ML early warning.")
    
    st.subheader("Diagnostic Pipeline Flowchart")
    fig_flow = render_algorithm_flowchart()
    st.plotly_chart(fig_flow, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Mathematical Formulations & Validation Criteria")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.markdown(
            r"""
            #### 1. SLA Variance Formulation
            For each order $i$, delivery delay variance is computed as:
            $$\Delta t_i = t_{\text{actual}, i} - t_{\text{promised}, i}$$
            Where:
            - $\Delta t_i \le 0$: On-time fulfillment compliant with customer promise.
            - $\Delta t_i > 0$: Breach condition requiring bottleneck attribution.
            
            #### 2. Bottleneck Stage Attribution Logic
            Excess duration over SLA budget is calculated for each segment:
            $$E_{\text{pick}} = \max(0, t_{\text{pick}} - B_{\text{pick}})$$
            $$E_{\text{stage}} = \max(0, t_{\text{stage}} - B_{\text{stage}})$$
            $$E_{\text{transit}} = \max(0, t_{\text{transit}} - (\frac{d}{v_{\text{target}}} + \tau))$$
            $$E_{\text{lastmile}} = \max(0, t_{\text{lastmile}} - B_{\text{lastmile}})$$
            $$\text{Bottleneck Stage} = \arg\max_{s} E_s$$
            """
        )
    with col_f2:
        st.markdown(
            r"""
            #### 3. Pre-Delivery Early Warning Classifier
            The late risk classification vector $\vec{x}_i$ strictly incorporates signals observable before linehaul departure:
            $$\vec{x}_i = [\rho_{\text{staffing}}, t_{\text{pick}}, t_{\text{stage}}, d_{\text{route}}, \text{Tier}, \text{Carrier}, \text{Category}, h_{\text{order}}]$$
            Target probability:
            $$\hat{P}(\text{Late}_i = 1 \mid \vec{x}_i) = \text{RandomForest}(\vec{x}_i)$$
            Orders with $\hat{P} \ge 0.60$ are routed to the proactive priority queue.
            
            #### 4. Chronological Integrity Check
            All synthetic journeys satisfy strict non-negative progression:
            $$t_{\text{order}} < t_{\text{pick}} < t_{\text{pack}} < t_{\text{manifest}} < t_{\text{dispatch}} < t_{\text{transit}} \le t_{\text{delivery}}$$
            """
        )

# ==============================================================================
# PAGE 8: DATA EXPLORER & DICTIONARY
# ==============================================================================
elif selected_page == "🗃️ Data Explorer & Dictionary":
    st.title("Data Explorer, Dictionary & CSV Export")
    st.markdown("Inspect filtered synthetic records, explore the data dictionary, and download datasets for offline auditing.")
    
    tab_exp1, tab_exp2 = st.tabs(["📋 Filtered Data Table & Preview", "📖 Operational Data Dictionary"])
    
    with tab_exp1:
        st.subheader(f"Active Filter Records ({len(filtered_df):,} Orders)")
        
        # Search box
        search_query = st.text_input("Search by Order ID or Carrier:", "")
        display_df = filtered_df
        if search_query:
            display_df = display_df[
                display_df["order_id"].str.contains(search_query, case=False, na=False) |
                display_df["carrier_id"].str.contains(search_query, case=False, na=False)
            ]
            
        st.dataframe(display_df, use_container_width=True, height=420)
        
        # Download Filtered CSV
        csv_data = display_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Orders Dataset (CSV)",
            data=csv_data,
            file_name="flipkart_delivery_performance_synthetic_data.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        st.markdown("---")
        st.subheader("Summary Statistics Distribution")
        st.dataframe(display_df.describe().T.round(2), use_container_width=True)
        
    with tab_exp2:
        st.subheader("Data Dictionary & Schema Specification")
        st.markdown("All 30 operational attributes generated in the synthetic prototype:")
        dict_df = get_data_dictionary()
        st.dataframe(dict_df, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #64748B; font-size: 0.8rem; padding: 10px 0;">
        Flipkart Delivery Performance Crisis Prototype | Operations Data Science & Systems Engineering<br>
        100% Synthetic Demo Data | No confidential or live systems accessed.
    </div>
    """,
    unsafe_allow_html=True
)
