import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Check if the file exists and read it
file_path = 'darjeeling_erw_results.out'

try:
    # Read the file and display first few rows to see actual column names
    print("Reading PHREEQC output file...")
    data = pd.read_csv(file_path, sep='\t')
    
    print("File successfully loaded!")
    print(f"Number of rows: {len(data)}")
    print(f"Number of columns: {len(data.columns)}")
    print("\nActual column names:")
    for i, col in enumerate(data.columns):
        print(f"  {i}: '{col}'")
    
    print("\nFirst few rows:")
    print(data.head())
    
    # Map column names (handle different possible names)
    column_map = {}
    
    # Find step/time column
    step_cols = [col for col in data.columns if any(x in col.lower() for x in ['step', 'time', 'sim'])]
    step_col = step_cols[0] if step_cols else data.columns[0]
    
    # Find pH column  
    ph_cols = [col for col in data.columns if 'ph' in col.lower()]
    ph_col = ph_cols[0] if ph_cols else None
    
    # Find alkalinity column
    alk_cols = [col for col in data.columns if any(x in col.lower() for x in ['alk', 'alkalinity'])]
    alk_col = alk_cols[0] if alk_cols else None
    
    # Find calcium column
    ca_cols = [col for col in data.columns if 'ca' in col.lower() and '+2' in col]
    ca_col = ca_cols[0] if ca_cols else None
    
    # Find magnesium column
    mg_cols = [col for col in data.columns if 'mg' in col.lower() and '+2' in col]
    mg_col = mg_cols[0] if mg_cols else None
    
    # Find bicarbonate column
    hco3_cols = [col for col in data.columns if 'hco3' in col.lower()]
    hco3_col = hco3_cols[0] if hco3_cols else None
    
    print(f"\nMapped columns:")
    print(f"Time/Step: {step_col}")
    print(f"pH: {ph_col}")
    print(f"Alkalinity: {alk_col}")
    print(f"Calcium: {ca_col}")
    print(f"Magnesium: {mg_col}")
    print(f"Bicarbonate: {hco3_col}")
    
    # Create visualizations
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Enhanced Rock Weathering - Darjeeling Tea Plantation\nPHREEQC Simulation Results', 
                 fontsize=16, fontweight='bold')
    
    # Plot 1: pH Evolution (if available)
    if ph_col:
        axes[0,0].plot(data[step_col], data[ph_col], 'b-', linewidth=2, marker='o', markersize=2)
        axes[0,0].set_title('pH Buffering in Tea Plantation Soil', fontweight='bold')
        axes[0,0].set_xlabel('Time Steps')
        axes[0,0].set_ylabel('pH')
        axes[0,0].grid(True, alpha=0.3)
        
        # Add horizontal line at neutral pH
        axes[0,0].axhline(y=7, color='r', linestyle='--', alpha=0.5, label='Neutral pH')
        axes[0,0].legend()
    else:
        axes[0,0].text(0.5, 0.5, 'pH data not found', ha='center', va='center', transform=axes[0,0].transAxes)
        axes[0,0].set_title('pH Data Not Available')
    
    # Plot 2: Alkalinity (if available)
    if alk_col:
        axes[0,1].plot(data[step_col], data[alk_col], 'g-', linewidth=2, marker='s', markersize=2)
        axes[0,1].set_title('Carbon Removal (Alkalinity)', fontweight='bold')
        axes[0,1].set_xlabel('Time Steps')
        axes[0,1].set_ylabel('Alkalinity (eq/L)')
        axes[0,1].grid(True, alpha=0.3)
    else:
        axes[0,1].text(0.5, 0.5, 'Alkalinity data not found', ha='center', va='center', transform=axes[0,1].transAxes)
        axes[0,1].set_title('Alkalinity Data Not Available')
    
    # Plot 3: Nutrient Release (if available)
    if ca_col or mg_col:
        if ca_col:
            axes[0,2].plot(data[step_col], data[ca_col], 'r-', linewidth=2, label='Ca²⁺', marker='^', markersize=2)
        if mg_col:
            axes[0,2].plot(data[step_col], data[mg_col], 'orange', linewidth=2, label='Mg²⁺', marker='v', markersize=2)
        axes[0,2].set_title('Nutrient Release from Basalt', fontweight='bold')
        axes[0,2].set_xlabel('Time Steps')
        axes[0,2].set_ylabel('Concentration (mol/L)')
        axes[0,2].legend()
        axes[0,2].grid(True, alpha=0.3)
    else:
        axes[0,2].text(0.5, 0.5, 'Nutrient data not found', ha='center', va='center', transform=axes[0,2].transAxes)
        axes[0,2].set_title('Nutrient Data Not Available')
    
    # Plot 4: Bicarbonate Formation (if available)
    if hco3_col:
        axes[1,0].plot(data[step_col], data[hco3_col], 'purple', linewidth=2, marker='d', markersize=2)
        axes[1,0].set_title('Carbon Sequestration (HCO₃⁻)', fontweight='bold')
        axes[1,0].set_xlabel('Time Steps')
        axes[1,0].set_ylabel('HCO₃⁻ Concentration (mol/L)')
        axes[1,0].grid(True, alpha=0.3)
    else:
        axes[1,0].text(0.5, 0.5, 'HCO3- data not found', ha='center', va='center', transform=axes[1,0].transAxes)
        axes[1,0].set_title('HCO₃⁻ Data Not Available')
    
    # Plot 5: All available numeric data
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    plot_cols = [col for col in numeric_cols if col != step_col][:5]  # First 5 numeric columns
    
    for i, col in enumerate(plot_cols):
        color = plt.cm.tab10(i)
        axes[1,1].plot(data[step_col], data[col], color=color, linewidth=1.5, label=col[:15], alpha=0.8)
    
    axes[1,1].set_title('All Numeric Variables', fontweight='bold')
    axes[1,1].set_xlabel('Time Steps')
    axes[1,1].set_ylabel('Values')
    axes[1,1].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    axes[1,1].grid(True, alpha=0.3)
    
    # Plot 6: Summary Statistics
    if ph_col and alk_col:
        initial_pH = data[ph_col].iloc[0]
        final_pH = data[ph_col].iloc[-1]
        pH_change = final_pH - initial_pH
        
        initial_alk = data[alk_col].iloc[0]
        final_alk = data[alk_col].iloc[-1]
        alk_change = final_alk - initial_alk
        
        metrics = ['pH Change', 'Alkalinity\nIncrease']
        values = [pH_change, alk_change]
        colors = ['blue', 'green']
        
        bars = axes[1,2].bar(metrics, values, color=colors, alpha=0.7)
        axes[1,2].set_title('Key ERW Metrics', fontweight='bold')
        axes[1,2].grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            axes[1,2].text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.01, 
                          f'{value:.4f}', ha='center', va='bottom', fontweight='bold')
    else:
        axes[1,2].text(0.5, 0.5, 'Insufficient data for metrics', ha='center', va='center', transform=axes[1,2].transAxes)
        axes[1,2].set_title('Metrics Not Available')
    
    plt.tight_layout()
    plt.savefig('darjeeling_erw_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Print summary for Alt Carbon interview
    print("\n" + "="*60)
    print("ENHANCED ROCK WEATHERING RESULTS SUMMARY")
    print("="*60)
    print(f"Simulation steps completed: {len(data)}")
    
    if ph_col:
        print(f"Initial pH: {data[ph_col].iloc[0]:.3f}")
        print(f"Final pH: {data[ph_col].iloc[-1]:.3f}")
        print(f"pH improvement: +{data[ph_col].iloc[-1] - data[ph_col].iloc[0]:.3f}")
    
    if alk_col:
        alk_increase = data[alk_col].iloc[-1] - data[alk_col].iloc[0]
        co2_removal = alk_increase * 44.01 * 1000  # Convert to g CO2/L
        print(f"Alkalinity increase: {alk_increase:.6f} eq/L")
        print(f"Estimated CO₂ removal: {co2_removal:.3f} g/L")
    
    if ca_col:
        print(f"Final Ca²⁺ concentration: {data[ca_col].iloc[-1]:.6f} mol/L")
    
    if mg_col:
        print(f"Final Mg²⁺ concentration: {data[mg_col].iloc[-1]:.6f} mol/L")
    
    print("\nVisualization saved as: darjeeling_erw_analysis.png")
    print("Ready for Alt Carbon interview presentation!")

except Exception as e:
    print(f"Error: {e}")
    print("\nTrying alternative file reading methods...")
    
    # Try different separators
    for sep in ['\t', ' ', ',', ';']:
        try:
            data = pd.read_csv(file_path, sep=sep)
            print(f"Successfully read with separator: '{sep}'")
            print("Columns found:", list(data.columns))
            print("First few rows:")
            print(data.head())
            break
        except:
            continue
