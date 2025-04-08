import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from futures_data import (
    get_all_futures_with_market_data, 
    get_future_by_symbol, 
    get_stop_loss_levels, 
    calculate_r_multiples,
    get_current_price,
    calculate_atr,
    FUTURES_DATA
)

# Set page configuration
st.set_page_config(
    page_title="Futures Calculator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 1rem 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 5px 5px 0px 0px;
        gap: 1rem;
        padding: 10px 20px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4e8df5;
        color: white;
    }
    .dataframe {
        font-size: 14px;
    }
    .section-header {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .card {
        background-color: white;
        border-radius: 5px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 5px;
        padding: 15px;
        margin: 5px;
        text-align: center;
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-label {
        font-size: 14px;
        color: #666;
    }
    .stop-loss-card {
        background-color: #f8f9fa;
        border-radius: 5px;
        padding: 10px;
        margin: 5px;
        border-left: 4px solid #ff9800;
    }
    .target-card {
        background-color: #f8f9fa;
        border-radius: 5px;
        padding: 10px;
        margin: 5px;
        border-left: 4px solid #4caf50;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Futures Calculator")
# Use a more reliable emoji instead of an external image
st.sidebar.markdown("### 📊 Futures Trading Tools")

# Navigation
page = st.sidebar.radio("Navigation", ["Futures Table", "Position Size Calculator"])

# Futures Table Page
if page == "Futures Table":
    st.title("Futures Market Instruments")
    st.markdown("### Comprehensive Futures Contract Information")
    
    # Get futures data with market information
    with st.spinner("Loading market data..."):
        futures_data = get_all_futures_with_market_data()
    
    # Convert to DataFrame for display
    df = pd.DataFrame(futures_data)
    
    # Format the DataFrame for display
    display_df = df.copy()
    display_df['tick_value'] = display_df['tick_size'] * display_df['multiplier']
    
    # Format numeric columns
    numeric_cols = ['current_price', 'notional_exposure', 'tick_value', 'initial_margin']
    for col in numeric_cols:
        if col in display_df.columns:
            display_df[col] = display_df[col].apply(
                lambda x: f"${x:.2f}" if isinstance(x, (int, float)) else x
            )
            
    # Store original ATR values for points reference
    if 'atr' in display_df.columns:
        display_df['atr_points'] = display_df['atr']
        
        # Format ATR for display
        display_df['atr'] = display_df['atr'].apply(
            lambda x: f"${x:.2f}" if isinstance(x, (int, float)) else x
        )
    
    # Format daily_pnl_range to show both dollar value and points
    if 'daily_pnl_range' in display_df.columns and 'atr_points' in display_df.columns:
        display_df['daily_pnl_range'] = display_df.apply(
            lambda row: f"${row['daily_pnl_range']:.2f} ({row['atr_points']:.2f} pts)" 
            if isinstance(row['daily_pnl_range'], (int, float)) and isinstance(row['atr_points'], (int, float))
            else row['daily_pnl_range'],
            axis=1
        )
    
    # Group by section for display
    sections = display_df['section'].unique().tolist()
    
    # Create tabs for each section
    tabs = st.tabs(sections)
    
    for i, section in enumerate(sections):
        with tabs[i]:
            section_df = display_df[display_df['section'] == section].copy()
            
            # Select columns to display
            columns_to_display = [
                'name', 'ticker', 'symbol', 'notional_value', 'tick_size', 
                'multiplier', 'tick_value', 'current_price', 'notional_exposure', 
                'initial_margin', 'etf_equivalent', 'etf_shares_approx', 'daily_pnl_range'
            ]
            
            # Rename columns for better display
            renamed_columns = {
                'name': 'Name',
                'ticker': 'Ticker',
                'symbol': 'Symbol',
                'notional_value': 'Notional Value',
                'tick_size': 'Tick Size',
                'multiplier': 'Multiplier',
                'tick_value': 'Tick Value',
                'current_price': 'Current Price',
                'notional_exposure': 'Notional Exposure',
                'initial_margin': 'SPAN Margin (Approx)',
                'etf_equivalent': 'ETF Equivalent',
                'etf_shares_approx': 'ETF Shares Approx',
                'daily_pnl_range': 'Avg Daily P/L Range'
            }
            
            # Display the section data
            st.markdown(f"### {section} Futures")
            
            # Convert all columns to string to avoid PyArrow type errors
            display_section_df = section_df[columns_to_display].rename(columns=renamed_columns).copy()
            for col in display_section_df.columns:
                display_section_df[col] = display_section_df[col].astype(str)
                
            st.dataframe(
                display_section_df,
                use_container_width=True,
                hide_index=True
            )

# Position Size Calculator Page
elif page == "Position Size Calculator":
    st.title("Futures Position Size Calculator")
    st.markdown("### Calculate position size, stop loss, and profit targets")
    
    # Get all futures symbols for selection
    all_futures = get_all_futures_with_market_data()
    futures_dict = {f"{future['name']} ({future['ticker']})": future['symbol'] for future in all_futures}
    
    # Create two columns for the layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Select Future")
        selected_future_name = st.selectbox(
            "Choose a futures contract:",
            options=list(futures_dict.keys())
        )
        
        selected_symbol = futures_dict[selected_future_name]
        future = next((f for f in all_futures if f['symbol'] == selected_symbol), None)
        
        if future:
            # Display contract specifications
            st.markdown("### Contract Specifications")
            specs_data = {
                "Specification": ["Ticker", "Symbol", "Tick Size", "Multiplier", "Value per Tick", "ETF Equivalent"],
                "Value": [
                    future['ticker'],
                    future['symbol'],
                    future['tick_size'],
                    future['multiplier'],
                    f"${future['tick_size'] * future['multiplier']:.2f}",
                    future['etf_equivalent']
                ]
            }
            st.dataframe(pd.DataFrame(specs_data), use_container_width=True, hide_index=True)
            
            # Get current price and ATR
            current_price = future.get('current_price')
            atr_value = future.get('atr')
            
            if isinstance(current_price, (int, float)) and isinstance(atr_value, (int, float)):
                st.markdown("### Market Data")
                col_price, col_atr = st.columns(2)
                
                with col_price:
                    st.metric("Current Price", f"${current_price:.2f}")
                
                with col_atr:
                    st.metric("14-Day ATR", f"${atr_value:.2f}")
                
                # Position size inputs
                st.markdown("### Position Sizing")
                
                account_size = st.number_input("Account Size ($)", min_value=1000.0, value=100000.0, step=1000.0)
                risk_percentage = st.slider("Risk Percentage (%)", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
                risk_amount = account_size * (risk_percentage / 100)
                st.metric("Risk Amount ($)", f"${risk_amount:.2f}")
                
                # ATR multiplier for stop loss
                atr_multiplier = st.select_slider(
                    "ATR Multiplier for Stop Loss",
                    options=[0.25, 0.5, 0.75, 1.0, 1.25, 1.5],
                    value=1.0
                )
                
                # Calculate stop distance and stop loss amount
                stop_distance = atr_value * atr_multiplier
                stop_price = current_price - stop_distance  # For long position
                stop_loss_amount = stop_distance * future['multiplier']
                
                # Display stop loss information
                st.markdown(f"""<div style='background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-top: 10px;'>
                            <p><b>Stop Loss:</b> ${stop_price:.2f} (${stop_loss_amount:.2f} per contract)</p>
                            </div>""", unsafe_allow_html=True)
                
                # Calculate position size - ensure it's at least 1 if valid
                if stop_loss_amount > 0:
                    max_contracts = max(1, int(risk_amount / stop_loss_amount))
                else:
                    max_contracts = 0
                
                # Display max contracts as a reference
                st.metric("Maximum Contracts (Based on Risk)", max_contracts)
                
                # Allow user to input their desired number of contracts
                user_contracts = st.number_input(
                    "Number of Contracts to Trade", 
                    min_value=1, 
                    max_value=None, 
                    value=1,
                    step=1,
                    help="Enter the number of contracts you want to trade"
                )
                
                # Calculate and display the risk for the user-selected number of contracts
                user_risk_amount = user_contracts * stop_loss_amount
                user_risk_percent = (user_risk_amount / account_size) * 100
                
                st.markdown(f"""<div style='background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-top: 10px;'>
                            <p><b>Risk for {user_contracts} contract{'s' if user_contracts > 1 else ''}:</b> ${user_risk_amount:.2f} ({user_risk_percent:.2f}% of account)</p>
                            </div>""", unsafe_allow_html=True)
                
            else:
                st.error("Unable to fetch current price or ATR data for this contract.")
    
    with col2:
        if future and isinstance(current_price, (int, float)) and isinstance(atr_value, (int, float)):
            st.markdown("### Stop Loss & Target Analysis")
            
            # Create tabs for long and short positions
            position_tabs = st.tabs(["Long Position", "Short Position"])
            
            with position_tabs[0]:  # Long Position
                st.markdown("#### Stop Loss Levels")
                
                # Calculate stop loss levels for different ATR multipliers
                atr_multipliers = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5]
                stop_loss_cols = st.columns(len(atr_multipliers))
                
                for i, multiplier in enumerate(atr_multipliers):
                    stop_distance = atr_value * multiplier
                    stop_price = current_price - stop_distance
                    stop_loss_amount = stop_distance * future['multiplier']
                    
                    with stop_loss_cols[i]:
                        st.markdown(f"<div class='stop-loss-card'>"
                                    f"<p><b>{multiplier} ATR</b></p>"
                                    f"<p>Price: ${stop_price:.2f}</p>"
                                    f"<p>Distance: {stop_distance:.2f} points (${stop_loss_amount:.2f})</p>"
                                    f"</div>", unsafe_allow_html=True)
                
                # Calculate R-multiple targets based on the selected stop loss
                st.markdown("#### Profit Targets (Based on selected ATR multiplier)")
                
                # Use the stop distance from the selected ATR multiplier
                selected_stop_distance = atr_value * atr_multiplier
                selected_stop_loss_amount = selected_stop_distance * future['multiplier']
                
                r_multiples = [1, 2, 2.5, 3]
                target_cols = st.columns(len(r_multiples))
                
                for i, r in enumerate(r_multiples):
                    target_distance = selected_stop_distance * r
                    target_price = current_price + target_distance
                    target_amount = selected_stop_loss_amount * r
                    
                    with target_cols[i]:
                        st.markdown(f"<div class='target-card'>"
                                    f"<p><b>{r}R Target</b></p>"
                                    f"<p>Price: ${target_price:.2f}</p>"
                                    f"<p>Distance: {target_distance:.2f} points (${target_amount:.2f})</p>"
                                    f"</div>", unsafe_allow_html=True)
                
                # Risk-Reward visualization
                st.markdown("#### Risk-Reward Visualization")
                
                # Create price range for visualization
                price_range = np.linspace(
                    stop_price - selected_stop_distance,
                    current_price + (selected_stop_distance * 3.5),
                    100
                )
                
                # Create figure
                fig = go.Figure()
                
                # Add price range area
                fig.add_trace(go.Scatter(
                    x=[0, 0],
                    y=[price_range.min(), price_range.max()],
                    mode='lines',
                    line=dict(width=0),
                    showlegend=False
                ))
                
                # Add current price line
                fig.add_shape(
                    type="line",
                    x0=0, x1=1,
                    y0=current_price, y1=current_price,
                    line=dict(color="blue", width=2, dash="solid"),
                    xref="paper", yref="y"
                )
                
                # Add stop loss line
                fig.add_shape(
                    type="line",
                    x0=0, x1=1,
                    y0=stop_price, y1=stop_price,
                    line=dict(color="red", width=2, dash="dash"),
                    xref="paper", yref="y"
                )
                
                # Add target lines
                for r, color in zip(r_multiples, ["green", "purple", "orange", "teal"]):
                    target_price = current_price + (selected_stop_distance * r)
                    fig.add_shape(
                        type="line",
                        x0=0, x1=1,
                        y0=target_price, y1=target_price,
                        line=dict(color=color, width=2, dash="dot"),
                        xref="paper", yref="y"
                    )
                
                # Add annotations
                fig.add_annotation(
                    x=1.02, y=current_price,
                    text="Entry",
                    showarrow=False,
                    xref="paper", yref="y"
                )
                
                fig.add_annotation(
                    x=1.02, y=stop_price,
                    text=f"Stop ({atr_multiplier} ATR)",
                    showarrow=False,
                    xref="paper", yref="y"
                )
                
                for r in r_multiples:
                    target_price = current_price + (selected_stop_distance * r)
                    fig.add_annotation(
                        x=1.02, y=target_price,
                        text=f"{r}R",
                        showarrow=False,
                        xref="paper", yref="y"
                    )
                
                # Update layout
                fig.update_layout(
                    title="Price Levels for Long Position",
                    xaxis_title="",
                    yaxis_title="Price",
                    showlegend=False,
                    height=400,
                    margin=dict(l=0, r=100, t=30, b=0),
                    xaxis=dict(showticklabels=False),
                    yaxis=dict(range=[stop_price - (selected_stop_distance * 0.5), 
                                      current_price + (selected_stop_distance * 3.5)])
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
            with position_tabs[1]:  # Short Position
                st.markdown("#### Stop Loss Levels")
                
                # Calculate stop loss levels for different ATR multipliers
                atr_multipliers = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5]
                stop_loss_cols = st.columns(len(atr_multipliers))
                
                for i, multiplier in enumerate(atr_multipliers):
                    stop_distance = atr_value * multiplier
                    stop_price = current_price + stop_distance  # For short position
                    stop_loss_amount = stop_distance * future['multiplier']
                    
                    with stop_loss_cols[i]:
                        st.markdown(f"<div class='stop-loss-card'>"
                                    f"<p><b>{multiplier} ATR</b></p>"
                                    f"<p>Price: ${stop_price:.2f}</p>"
                                    f"<p>Distance: {stop_distance:.2f} points (${stop_loss_amount:.2f})</p>"
                                    f"</div>", unsafe_allow_html=True)
                
                # Calculate R-multiple targets
                st.markdown("#### Profit Targets (Based on selected ATR multiplier)")
                
                selected_stop_distance = atr_value * atr_multiplier
                selected_stop_loss_amount = selected_stop_distance * future['multiplier']
                
                r_multiples = [1, 2, 2.5, 3]
                target_cols = st.columns(len(r_multiples))
                
                for i, r in enumerate(r_multiples):
                    target_distance = selected_stop_distance * r
                    target_price = current_price - target_distance  # For short position
                    target_amount = selected_stop_loss_amount * r
                    
                    with target_cols[i]:
                        st.markdown(f"<div class='target-card'>"
                                    f"<p><b>{r}R Target</b></p>"
                                    f"<p>Price: ${target_price:.2f}</p>"
                                    f"<p>Distance: {target_distance:.2f} points (${target_amount:.2f})</p>"
                                    f"</div>", unsafe_allow_html=True)
                
                # Risk-Reward visualization
                st.markdown("#### Risk-Reward Visualization")
                
                # Create price range for visualization
                price_range = np.linspace(
                    current_price - (selected_stop_distance * 3.5),
                    stop_price + selected_stop_distance,
                    100
                )
                
                # Create figure
                fig = go.Figure()
                
                # Add price range area
                fig.add_trace(go.Scatter(
                    x=[0, 0],
                    y=[price_range.min(), price_range.max()],
                    mode='lines',
                    line=dict(width=0),
                    showlegend=False
                ))
                
                # Add current price line
                fig.add_shape(
                    type="line",
                    x0=0, x1=1,
                    y0=current_price, y1=current_price,
                    line=dict(color="blue", width=2, dash="solid"),
                    xref="paper", yref="y"
                )
                
                # Add stop loss line
                stop_price_short = current_price + selected_stop_distance
                fig.add_shape(
                    type="line",
                    x0=0, x1=1,
                    y0=stop_price_short, y1=stop_price_short,
                    line=dict(color="red", width=2, dash="dash"),
                    xref="paper", yref="y"
                )
                
                # Add target lines
                for r, color in zip(r_multiples, ["green", "purple", "orange", "teal"]):
                    target_price = current_price - (selected_stop_distance * r)
                    fig.add_shape(
                        type="line",
                        x0=0, x1=1,
                        y0=target_price, y1=target_price,
                        line=dict(color=color, width=2, dash="dot"),
                        xref="paper", yref="y"
                    )
                
                # Add annotations
                fig.add_annotation(
                    x=1.02, y=current_price,
                    text="Entry",
                    showarrow=False,
                    xref="paper", yref="y"
                )
                
                fig.add_annotation(
                    x=1.02, y=stop_price_short,
                    text=f"Stop ({atr_multiplier} ATR)",
                    showarrow=False,
                    xref="paper", yref="y"
                )
                
                for r in r_multiples:
                    target_price = current_price - (selected_stop_distance * r)
                    fig.add_annotation(
                        x=1.02, y=target_price,
                        text=f"{r}R",
                        showarrow=False,
                        xref="paper", yref="y"
                    )
                
                # Update layout
                fig.update_layout(
                    title="Price Levels for Short Position",
                    xaxis_title="",
                    yaxis_title="Price",
                    showlegend=False,
                    height=400,
                    margin=dict(l=0, r=100, t=30, b=0),
                    xaxis=dict(showticklabels=False),
                    yaxis=dict(range=[current_price - (selected_stop_distance * 3.5), 
                                      stop_price_short + (selected_stop_distance * 0.5)])
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
            # Position sizing summary
            st.markdown("### Position Sizing Summary")
            
            # Use the user-selected number of contracts for position sizing
            # Calculate different position sizes
            position_sizes = [
                {"size": 1, "label": "Minimum"},
                {"size": user_contracts, "label": "Selected"},
                {"size": max(1, max_contracts), "label": "Max Risk"}
            ]
            
            # Create columns for each position size
            size_cols = st.columns(len(position_sizes))
            
            for i, pos in enumerate(position_sizes):
                contracts = pos["size"]
                risk = contracts * selected_stop_loss_amount
                risk_percent = (risk / account_size) * 100
                
                with size_cols[i]:
                    st.markdown(f"""
                    <div style='background-color: #f0f2f6; padding: 15px; border-radius: 5px; text-align: center;'>
                        <h4>{pos["label"]}</h4>
                        <div style='font-size: 24px; font-weight: bold;'>{contracts} contract{'s' if contracts > 1 else ''}</div>
                        <p>Risk: ${risk:.2f} ({risk_percent:.2f}%)</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Calculate R-multiple outcomes for the selected position size
            st.markdown("### Potential Outcomes")
            
            outcomes_data = []
            for r in [1, 2, 2.5, 3]:
                for pos in position_sizes:
                    contracts = pos["size"]
                    profit = contracts * selected_stop_loss_amount * r
                    
                    outcomes_data.append({
                        "Position Size": f"{pos['label']} ({contracts} contract{'s' if contracts > 1 else ''})",
                        "R-Multiple": f"{r}R",
                        "Profit/Loss": profit
                    })
            
            # Create DataFrame for display
            outcomes_df = pd.DataFrame(outcomes_data)
            
            # Format profit/loss column
            outcomes_df["Profit/Loss"] = outcomes_df["Profit/Loss"].apply(lambda x: f"${x:.2f}")
            
            # Convert all columns to strings to avoid PyArrow errors
            for col in outcomes_df.columns:
                outcomes_df[col] = outcomes_df[col].astype(str)
            
            # Display the outcomes table
            st.dataframe(
                outcomes_df,
                use_container_width=True,
                hide_index=True
            )
            
        else:
            st.info("Please select a futures contract to see position sizing calculations.")

# Add disclaimers and footer
st.markdown("---")
st.markdown(
    """
    <div style="padding: 10px; background-color: #f8f9fa; border-radius: 5px; margin-bottom: 20px;">
        <h4>Disclaimers:</h4>
        <ul>
            <li>Future quotes may be delayed and are not automatically refreshed. Data is provided for informational purposes only.</li>
            <li>SPAN margin requirements are approximate and may vary significantly between brokers. Please consult your broker for actual margin requirements.</li>
            <li>Average Daily P/L Range is calculated based on 14-day ATR and is intended as a general guide only.</li>
        </ul>
    </div>
    <div style="text-align: center; color: #888;">
        Futures Calculator App | Data provided by Yahoo Finance
    </div>
    """,
    unsafe_allow_html=True
)
