"""
Synthetic Data Generation Engine for Flipkart Delivery Operations Prototype.
Generates realistic, chronologically consistent synthetic logistics data.
DISCLAIMER: ALL DATA IS 100% SYNTHETIC AND FOR DEMO/ANALYSIS PURPOSES ONLY.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Master reference datasets
FULFILLMENT_CENTERS = [
    {"id": "BLR_Malur_FC", "name": "Bengaluru Malur FC", "region": "South", "capacity_tier": "Tier-1 Mega Hub", "base_efficiency": 0.92},
    {"id": "BOM_Bhiwandi_FC", "name": "Mumbai Bhiwandi FC", "region": "West", "capacity_tier": "Tier-1 Mega Hub", "base_efficiency": 0.82},
    {"id": "DEL_Farukhnagar_FC", "name": "Delhi Farukhnagar FC", "region": "North", "capacity_tier": "Tier-1 Mega Hub", "base_efficiency": 0.85},
    {"id": "CCU_Haringhata_FC", "name": "Kolkata Haringhata FC", "region": "East", "capacity_tier": "Tier-1 Mega Hub", "base_efficiency": 0.79},
    {"id": "HYD_Shamshabad_FC", "name": "Hyderabad Shamshabad FC", "region": "South", "capacity_tier": "Tier-2 Regional FC", "base_efficiency": 0.88},
]

CARRIERS = [
    {"id": "Ekart Logistics", "type": "Captive First-Party", "base_reliability": 0.89, "avg_speed_kmh": 46.0},
    {"id": "Delhivery", "type": "3PL Express Partner", "base_reliability": 0.84, "avg_speed_kmh": 43.0},
    {"id": "Shadowfax", "type": "Intra-City & Last-Mile 3PL", "base_reliability": 0.81, "avg_speed_kmh": 40.0},
    {"id": "BlueDart", "type": "Premium Air Express 3PL", "base_reliability": 0.93, "avg_speed_kmh": 55.0},
    {"id": "Xpressbees", "type": "E-Commerce 3PL Partner", "base_reliability": 0.83, "avg_speed_kmh": 42.0},
]

CATEGORIES = [
    {"category": "Smartphones & Electronics", "weight_factor": 1.0, "picking_complexity": 1.1, "high_value": True, "base_sla_days": 2},
    {"category": "Fashion & Apparel", "weight_factor": 0.6, "picking_complexity": 0.8, "high_value": False, "base_sla_days": 3},
    {"category": "Home & Kitchen", "weight_factor": 1.4, "picking_complexity": 1.3, "high_value": False, "base_sla_days": 4},
    {"category": "Grocery & Supermart", "weight_factor": 0.8, "picking_complexity": 0.7, "high_value": False, "base_sla_days": 1},
    {"category": "Large Appliances", "weight_factor": 2.2, "picking_complexity": 1.9, "high_value": True, "base_sla_days": 4},
]

REGIONS = ["North", "South", "West", "East", "Central", "North-East"]
CITY_TIERS = ["Tier 1 (Metro)", "Tier 2 (Urban)", "Tier 3+ (Semi-Urban/Rural)"]

SHIFTS = [
    {"name": "Morning Shift (06:00 - 14:00)", "code": "Shift-A", "staffing_mean": 0.98, "staffing_std": 0.05},
    {"name": "Afternoon Shift (14:00 - 22:00)", "code": "Shift-B", "staffing_mean": 0.92, "staffing_std": 0.07},
    {"name": "Night Shift (22:00 - 06:00)", "code": "Shift-C", "staffing_mean": 0.76, "staffing_std": 0.12}, # Chronic shortage
]

FIRST_ATTEMPT_FAILURE_REASONS = [
    "Customer Unavailable / Phone Unreachable",
    "Incomplete Address / Pincode Error",
    "Rider Shift Timeout / High Route Density",
    "Customer Refused / COD Cash Shortage",
    "OTP Verification Delivery Failure",
    "Customer Requested Rescheduled Delivery"
]

COMPLAINT_REASONS = [
    "Late Delivery Escalation",
    "Tracking Status Stalled / Not Updated",
    "Rude / Unprofessional Delivery Agent",
    "Package Outer Seal Damaged",
    "Delivery Rescheduled Without Consent"
]


def generate_synthetic_orders(num_records: int = 4000, random_seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic order journeys with end-to-end operational timestamps,
    delays, warehouse shifts, carrier scans, and complaints.
    """
    rng = np.random.default_rng(random_seed)
    
    # 30-day timeline ending recently
    base_end_date = datetime(2026, 10, 27, 18, 0, 0)
    start_date = base_end_date - timedelta(days=30)
    
    records = []
    
    fc_ids = [fc["id"] for fc in FULFILLMENT_CENTERS]
    hour_probs = np.array([
        0.015, 0.010, 0.005, 0.005, 0.005, 0.010, # 00-05
        0.020, 0.035, 0.045, 0.055, 0.060, 0.065, # 06-11
        0.070, 0.065, 0.060, 0.055, 0.055, 0.060, # 12-17
        0.075, 0.085, 0.090, 0.080, 0.045, 0.025  # 18-23
    ])
    hour_probs = hour_probs / hour_probs.sum()
    
    fc_weights = np.array([0.28, 0.26, 0.22, 0.14, 0.10])
    fc_weights = fc_weights / fc_weights.sum()
    
    carrier_weights = np.array([0.46, 0.22, 0.14, 0.10, 0.08])
    carrier_weights = carrier_weights / carrier_weights.sum()
    
    cat_weights = np.array([0.32, 0.28, 0.18, 0.12, 0.10])
    cat_weights = cat_weights / cat_weights.sum()
    
    region_weights = np.array([0.26, 0.28, 0.22, 0.12, 0.07, 0.05])
    region_weights = region_weights / region_weights.sum()
    
    city_tier_weights = np.array([0.48, 0.34, 0.18])
    city_tier_weights = city_tier_weights / city_tier_weights.sum()
    
    bin_probs = np.array([0.62, 0.22, 0.10, 0.06])
    bin_probs = bin_probs / bin_probs.sum()
    
    for i in range(num_records):
        order_num = 1000000 + i
        order_id = f"OD-FK-{order_num}"
        
        # Order placement timestamp
        random_day_offset = rng.uniform(0, 29)
        random_hour = rng.choice(24, p=hour_probs)
        random_minute = rng.integers(0, 60)
        random_second = rng.integers(0, 60)
        order_placed_at = start_date + timedelta(days=random_day_offset, hours=int(random_hour), minutes=int(random_minute), seconds=int(random_second))
        
        # Determine shift of order receipt
        hour = order_placed_at.hour
        if 6 <= hour < 14:
            shift_idx = 0
        elif 14 <= hour < 22:
            shift_idx = 1
        else:
            shift_idx = 2
        shift_info = SHIFTS[shift_idx]
        
        # Attributes
        fc_idx = rng.choice(len(FULFILLMENT_CENTERS), p=fc_weights)
        fc = FULFILLMENT_CENTERS[fc_idx]
        
        carrier_idx = rng.choice(len(CARRIERS), p=carrier_weights)
        carrier = CARRIERS[carrier_idx]
        
        cat_idx = rng.choice(len(CATEGORIES), p=cat_weights)
        cat = CATEGORIES[cat_idx]
        
        dest_region = rng.choice(REGIONS, p=region_weights)
        city_tier = rng.choice(CITY_TIERS, p=city_tier_weights)
        is_plus_member = bool(rng.random() < 0.38) # Flipkart VIP / Plus
        
        # Shift staffing ratio at FC
        staffing_ratio = float(np.clip(rng.normal(shift_info["staffing_mean"], shift_info["staffing_std"]), 0.55, 1.15))
        if fc["id"] == "BOM_Bhiwandi_FC" and shift_info["code"] == "Shift-C":
            staffing_ratio *= 0.88 # Known severe bottleneck node
            
        # Proximity and inventory split
        same_region = (fc["region"] == dest_region)
        if same_region:
            is_cross_region_split = bool(rng.random() < 0.08)
            route_distance_km = float(rng.uniform(15, 380))
        else:
            is_cross_region_split = True
            route_distance_km = float(rng.uniform(450, 1950))
            
        if city_tier == "Tier 3+ (Semi-Urban/Rural)":
            route_distance_km += float(rng.uniform(60, 220))
            
        stock_bin_loc = rng.choice(
            ["Primary Fast-Pick Bin", "High-Bay Remote Bin", "Cross-Dock Aisle", "Split-Backorder Staging"],
            p=bin_probs
        )
        
        # Promised SLA
        base_days = cat["base_sla_days"]
        if is_plus_member and base_days > 1:
            base_days -= 1
        if not same_region:
            base_days += 1
        if city_tier == "Tier 3+ (Semi-Urban/Rural)":
            base_days += 1
        promised_delivery_hours = base_days * 24.0
        promised_delivery_date = order_placed_at + timedelta(hours=promised_delivery_hours)
        
        # 1. Picking & Packing Stage
        # Understaffing or remote bin increases picking delay
        base_pick_hours = 1.8 * cat["picking_complexity"]
        staffing_multiplier = 1.0 / max(staffing_ratio, 0.4)
        bin_delay = 1.5 if stock_bin_loc == "High-Bay Remote Bin" else (2.4 if stock_bin_loc == "Split-Backorder Staging" else 0.2)
        pick_hours = base_pick_hours * staffing_multiplier + bin_delay + rng.exponential(0.6)
        pick_hours = float(np.clip(pick_hours, 0.5, 28.0))
        
        pick_start_at = order_placed_at + timedelta(hours=pick_hours * 0.4)
        pack_completed_at = order_placed_at + timedelta(hours=pick_hours)
        
        # 2. Dock Staging & Manifesting Stage
        # Bhiwandi and Haringhata night shifts suffer dock congestion
        dock_congestion = 2.8 if (fc["id"] in ["BOM_Bhiwandi_FC", "CCU_Haringhata_FC"] and shift_info["code"] in ["Shift-B", "Shift-C"]) else 0.8
        staging_hours = float(np.clip(dock_congestion + rng.exponential(1.1), 0.4, 18.0))
        manifested_at = pack_completed_at + timedelta(hours=staging_hours * 0.6)
        dispatched_at = pack_completed_at + timedelta(hours=staging_hours)
        
        # 3. Linehaul Transit Stage
        # Speed varies by carrier and distance
        carrier_speed = carrier["avg_speed_kmh"] * rng.uniform(0.85, 1.15)
        # Weather/highway congestion in North / East
        if dest_region in ["North", "East", "North-East"] and rng.random() < 0.22:
            transit_road_delay_hours = float(rng.uniform(6.0, 26.0))
        else:
            transit_road_delay_hours = float(rng.exponential(1.5))
            
        transit_hours = float((route_distance_km / max(carrier_speed, 20.0)) + transit_road_delay_hours)
        transit_hours = float(np.clip(transit_hours, 1.2, 96.0))
        hub_received_at = dispatched_at + timedelta(hours=transit_hours)
        
        # 4. Last-Mile Delivery Hub & First Attempt
        # Hub sorting and rider dispatch
        lastmile_sort_hours = float(np.clip(rng.uniform(1.5, 6.0), 1.0, 14.0))
        out_for_delivery_at = hub_received_at + timedelta(hours=lastmile_sort_hours)
        
        first_attempt_hours = float(rng.uniform(2.0, 7.5))
        first_attempt_at = out_for_delivery_at + timedelta(hours=first_attempt_hours)
        
        # First attempt success probability
        base_fadr = 0.88 if city_tier == "Tier 1 (Metro)" else (0.81 if city_tier == "Tier 2 (Urban)" else 0.72)
        if carrier["id"] == "Shadowfax" and city_tier == "Tier 3+ (Semi-Urban/Rural)":
            base_fadr *= 0.86
        first_attempt_success = bool(rng.random() < base_fadr)
        
        if first_attempt_success:
            delivery_attempts = 1
            first_attempt_fail_reason = "None (Success)"
            final_delivery_at = first_attempt_at
        else:
            first_attempt_fail_reason = str(rng.choice(FIRST_ATTEMPT_FAILURE_REASONS))
            # 2nd or 3rd attempt
            if rng.random() < 0.74:
                delivery_attempts = 2
                final_delivery_at = first_attempt_at + timedelta(hours=float(rng.uniform(18.0, 28.0)))
            else:
                delivery_attempts = 3
                final_delivery_at = first_attempt_at + timedelta(hours=float(rng.uniform(42.0, 56.0)))
                
        # Total duration and delay calculation
        actual_total_duration_hours = (final_delivery_at - order_placed_at).total_seconds() / 3600.0
        delivery_delay_hours = round(actual_total_duration_hours - promised_delivery_hours, 2)
        is_delayed = bool(delivery_delay_hours > 0.0)
        
        # Primary Delay Bottleneck Attribution
        # Benchmark budgets:
        # Pick budget: 3.5 hrs
        # Staging budget: 2.5 hrs
        # Linehaul budget: distance / 45 km/h + 3 hrs buffer
        # Last-mile budget: 10 hrs
        pick_budget = 3.5
        staging_budget = 2.5
        linehaul_budget = (route_distance_km / 45.0) + 3.0
        lastmile_budget = 10.0
        
        pick_excess = max(0.0, pick_hours - pick_budget)
        staging_excess = max(0.0, staging_hours - staging_budget)
        transit_excess = max(0.0, transit_hours - linehaul_budget)
        lastmile_excess = max(0.0, (final_delivery_at - hub_received_at).total_seconds()/3600.0 - lastmile_budget)
        
        if not is_delayed:
            bottleneck_stage = "Within SLA (No Bottleneck)"
        else:
            excesses = {
                "Warehouse Pick & Pack": pick_excess,
                "Dock Staging & Manifest": staging_excess,
                "Linehaul Transit": transit_excess,
                "Last-Mile & Delivery Attempts": lastmile_excess,
            }
            if is_cross_region_split and (pick_excess > 3.0 or transit_excess > 6.0):
                excesses["Inventory Split-Shipment"] = max(pick_excess, transit_excess) * 1.15
                
            bottleneck_stage = max(excesses, key=excesses.get)
            
        # Complaints probability
        complaint_prob = 0.02
        if is_delayed:
            if delivery_delay_hours > 24:
                complaint_prob += 0.35
            elif delivery_delay_hours > 6:
                complaint_prob += 0.18
            else:
                complaint_prob += 0.07
        if delivery_attempts > 1:
            complaint_prob += 0.15
        if cat["high_value"] and is_delayed:
            complaint_prob += 0.12
            
        has_complaint = bool(rng.random() < min(complaint_prob, 0.85))
        complaint_category = str(rng.choice(COMPLAINT_REASONS)) if has_complaint else "No Complaint"
        
        # Estimated cost impact (INR)
        # SLA breach penalty / concession + customer escalation handling cost
        cost_impact_inr = 0.0
        if is_delayed:
            cost_impact_inr += 120.0 + min(delivery_delay_hours * 15.0, 450.0)
        if delivery_attempts > 1:
            cost_impact_inr += (delivery_attempts - 1) * 65.0 # Reroute attempt cost
        if has_complaint:
            cost_impact_inr += 250.0 # Customer support ticket cost + appeasement voucher
            
        records.append({
            "order_id": order_id,
            "order_placed_at": order_placed_at,
            "promised_delivery_date": promised_delivery_date,
            "final_delivery_at": final_delivery_at,
            "promised_delivery_hours": round(promised_delivery_hours, 1),
            "actual_total_duration_hours": round(actual_total_duration_hours, 1),
            "delivery_delay_hours": delivery_delay_hours,
            "is_delayed": is_delayed,
            "delay_status": "Delayed" if is_delayed else "On-Time",
            "warehouse_id": fc["id"],
            "warehouse_name": fc["name"],
            "warehouse_region": fc["region"],
            "shift_name": shift_info["name"],
            "shift_code": shift_info["code"],
            "shift_staffing_ratio": round(staffing_ratio, 2),
            "stock_bin_location": stock_bin_loc,
            "carrier_id": carrier["id"],
            "carrier_type": carrier["type"],
            "product_category": cat["category"],
            "is_high_value": cat["high_value"],
            "customer_region": dest_region,
            "customer_city_tier": city_tier,
            "is_plus_member": is_plus_member,
            "is_cross_region_split": is_cross_region_split,
            "route_distance_km": round(route_distance_km, 1),
            "pick_hours": round(pick_hours, 2),
            "staging_hours": round(staging_hours, 2),
            "transit_hours": round(transit_hours, 2),
            "lastmile_hours": round((final_delivery_at - hub_received_at).total_seconds()/3600.0, 2),
            "bottleneck_stage": bottleneck_stage,
            "delivery_attempts": delivery_attempts,
            "first_attempt_success": first_attempt_success,
            "first_attempt_fail_reason": first_attempt_fail_reason,
            "has_complaint": has_complaint,
            "complaint_category": complaint_category,
            "cost_impact_inr": round(cost_impact_inr, 2),
            "data_origin": "SYNTHETIC_DATA_DEMO"
        })
        
    df = pd.DataFrame(records)
    # Sort chronologically by order placed timestamp
    df = df.sort_values("order_placed_at").reset_index(drop=True)
    return df


if __name__ == "__main__":
    test_df = generate_synthetic_orders(100)
    print("Generated test sample:", test_df.shape)
    print("Delay distribution:\n", test_df["delay_status"].value_counts(normalize=True))
    print("Bottleneck stages:\n", test_df["bottleneck_stage"].value_counts())
