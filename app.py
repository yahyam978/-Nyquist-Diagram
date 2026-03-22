import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Page configuration
st.set_page_config(page_title="Nyquist Plotter", layout="wide")

st.title("🎛️ Nyquist Diagram & Frequency Response Generator")
st.markdown("""
Enter the Real and Imaginary parts as functions of `w` (omega). 
For example: `1 / (w**2 + 1)` or `np.sin(w)`.
""")

# --- Sidebar Inputs ---
with st.sidebar:
    st.header("1. Define Transfer Function")
    re_input = st.text_input("Real Part: Re(w)", "1 / (w**2 + 1)")
    im_input = st.text_input("Imaginary Part: Im(w)", "-w / (w**2 + 1)")
    
    st.divider()
    
    mult_enabled = st.checkbox("Multiply by a second function?")
    if mult_enabled:
        re_input2 = st.text_input("Real Part 2: Re2(w)", "1")
        im_input2 = st.text_input("Imaginary Part 2: Im2(w)", "-w")
    
    st.divider()
    
    st.header("2. Frequency Range (w)")
    w_start = st.number_input("Start Omega (w)", value=0.001, format="%.4f")
    w_end = st.number_input("End Omega (w -> ∞)", value=1000.0, format="%.1f")
    points = st.slider("Number of points", 100, 2000, 500)

# --- Calculations ---
try:
    # Generate omega on a log scale to better represent "0 to infinity"
    w = np.logspace(np.log10(w_start), np.log10(w_end), points)

    # Evaluate the functions
    # Using np namespace allows users to use np.pi, np.exp, etc.
    safe_dict = {"w": w, "np": np}
    
    G1_re = eval(re_input, safe_dict)
    G1_im = eval(im_input, safe_dict)
    G1 = G1_re + 1j * G1_im

    if mult_enabled:
        G2_re = eval(re_input2, safe_dict)
        G2_im = eval(im_input2, safe_dict)
        G2 = G2_re + 1j * G2_im
        G_final = G1 * G2
    else:
        G_final = G1

    # Extract Metrics
    real = G_final.real
    imag = G_final.imag
    magnitude = np.abs(G_final)
    phase = np.angle(G_final, deg=True)

    # --- Layout: Plot and Table ---
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Nyquist Plot")
        fig, ax = plt.subplots(figsize=(8, 7))
        
        # Plot positive frequencies
        ax.plot(real, imag, 'b-', linewidth=2, label='G(jω)')
        # Plot negative frequencies (Mirror)
        ax.plot(real, -imag, 'r--', alpha=0.5, label='G(-jω)')
        
        # Stability point (-1, 0)
        ax.plot(-1, 0, 'ro', markersize=8)
        ax.annotate('Critical Point (-1,0)', (-1, 0), textcoords="offset points", 
                    xytext=(-10,10), ha='right', color='red')
        
        ax.axhline(0, color='black', lw=1.5)
        ax.axvline(0, color='black', lw=1.5)
        ax.set_xlabel("Real Part")
        ax.set_ylabel("Imaginary Part")
        ax.grid(True, which='both', linestyle='--', alpha=0.7)
        ax.legend()
        st.pyplot(fig)

    with col2:
        st.subheader("Frequency Response Table")
        df = pd.DataFrame({
            "Omega (w)": w,
            "Real": real,
            "Imaginary": imag,
            "Amp Ratio": magnitude,
            "Phase (Deg)": phase
        })
        
        # Display table with formatting
        st.dataframe(df.style.format({
            "Omega (w)": "{:.4f}",
            "Real": "{:.4f}",
            "Imaginary": "{:.4f}",
            "Amp Ratio": "{:.4f}",
            "Phase (Deg)": "{:.2f}"
        }), height=500)
        
        # Download Link
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📩 Download Data as CSV", csv, "nyquist_data.csv", "text/csv")

except Exception as e:
    st.error(f"❌ Error in calculation: {e}")
    st.info("Check your syntax. Use `w` for omega and `**` for powers (e.g., `w**2`).")
