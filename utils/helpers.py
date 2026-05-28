"""
Helper Functions
Reusable utility functions
"""

import streamlit as st
from datetime import datetime, timedelta

def format_date(date_obj):
    """Format date for display"""
    if not date_obj:
        return "N/A"
    if isinstance(date_obj, str):
        return date_obj
    return date_obj.strftime("%d %b %Y")

def calculate_days_ago(date_obj):
    """Calculate days since a date"""
    if not date_obj:
        return None
    if isinstance(date_obj, str):
        date_obj = datetime.strptime(date_obj, "%Y-%m-%d")
    delta = datetime.now() - date_obj
    return delta.days

def get_grade_color(rating):
    """Get color for grade rating"""
    colors = {
        'A': '#22c55e',
        'B': '#eab308',
        'C': '#f97316',
        'D': '#ef4444',
        'F': '#991b1b'
    }
    return colors.get(rating, '#6b7280')

def get_grade_emoji(rating):
    """Get emoji for grade"""
    emojis = {
        'A': '🟢',
        'B': '🟡',
        'C': '🟠',
        'D': '🔴',
        'F': '⚫'
    }
    return emojis.get(rating, '⚪')

def format_currency(amount):
    """Format amount as Malaysian Ringgit"""
    return f"RM {amount:.2f}"

def calculate_rer(weight_kg):
    """Calculate Resting Energy Requirement"""
    # Convert to float to handle Decimal from database
    weight_kg = float(weight_kg)
    return round(70 * (weight_kg ** 0.75))

def calculate_der(rer, activity_level):
    """Calculate Daily Energy Requirement"""
    # Convert to float
    rer = float(rer)
    multipliers = {
        'Sedentary': 1.0,
        'Moderate': 1.2,
        'Active': 1.4,
        'Very Active': 1.6
    }
    return round(rer * multipliers.get(activity_level, 1.2))

def show_success(message):
    """Show success message with custom styling"""
    st.success(f"✅ {message}")

def show_error(message):
    """Show error message with custom styling"""
    st.error(f"❌ {message}")

def show_warning(message):
    """Show warning message with custom styling"""
    st.warning(f"⚠️ {message}")

def show_info(message):
    """Show info message with custom styling"""
    st.info(f"ℹ️ {message}")