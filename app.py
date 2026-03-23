import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Page configuration
st.set_page_config(page_title="Nyquist Plotter Pro", layout="wide")

st.title("🎛️ Nyquist Diagram & Frequency Response")
st.markdown("""
**Instructions:** Enter the Real and Imaginary parts as functions of `w`. 
You can now use: `sin(w)`, `cos(w)`, `exp(w)`, `sqrt(w)`, and `pi`.
Example: Real = `cos(w)/(w+1)`, Imaginary = `-sin(w)/(w+1)`
""")

# --- Sidebar Inputs ---
with st.sidebar:
    st.header("1. Transfer Function Definition")
    re_input = st.text_input("Real Part: Re(w)", "cos(w) / (w + 1)")
    im_input = st.text_input("Imaginary Part: Im(w)", "-sin(w) / (w + 1)")
    
    st.divider()
    
    mult_enabled = st.checkbox("Multiply by a second function?")
    if mult_enabled:
        re_input2 = st.text_input("Real Part 2: Re2(w)", "1")
        im_input2 = st.text_input("Imaginary Part 2: Im2(w)", "0")
    
    st.divider()
    
    st.header("2. Range & Scale")
    scale_type = st.radio("Frequency Scale", ["Linear", "Logarithmic"])
    w_start = st.number_input("Start Omega (w)", value=0.0, format="%.4f")
    w_end = st.number_input("End Omega (w)", value=10.0, format="%.1f")
    points = st.slider("Number of points", 100, 5000, 1000)

# --- Calculations ---
try:
    # Generate omega values based on selected scale
    if scale_type == "Logarithmic":
        # Ensure w_start is not 0 for log scale
        start_val = np.log10(w_start) if w_start > 0 else -2
        w = np.logspace(start_val, np.log10(w_end), points)
    else:
        w = np.linspace(w_start, w_end, points)

    # Define the math environment for eval()
    # This maps 'sin' to 'np.sin', etc., so the user can type naturally
    math_env = {
        "w": w,
        "sin": np.sin,
        "cos": np.cos,
        "tan": np.tan,
        "exp": np.exp,
        "sqrt": np.sqrt,
        "pi": np.pi,
        "log": np.log,
        "np": np
    }
    
    # Calculate G1
    G1_re = eval(re_input, {"__builtins__": None}, math_env)
    G1_im = eval(im_input, {"__builtins__": None}, math_env)
    G1 = G1_re + 1j * G1_im

    if mult_enabled:
        G2_re = eval(re_input2, {"__builtins__": None}, math_env)
        G2_im = eval(im_input2, {"__builtins__": None}, math_env)
        G2 = G2_re + 1j * G2_im
        G_final = G1 * G2
    else:
        G_final = G1

    # Extract Metrics
    real = G_final.real
    imag = G_final.imag
    magnitude = np.abs(G_final)
    # Wrap phase to -180 to 180 range
    phase = np.angle(G_final, deg=True)

    # --- UI Layout ---
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Nyquist Diagram")
        fig, ax = plt.subplots(figsize=(8, 7))
        
        # Primary Path
        ax.plot(real, imag, 'b-', linewidth=2, label='G(jω)')
        # Mirror Path (Negative Frequencies)
        ax.plot(real, -imag, 'r--', alpha=0.4, label='G(-jω)')
        
        # Critical Point (-1, 0)
        ax.plot(-1, 0, 'ro', markersize=6)
        ax.axhline(0, color='black', lw=1)
        ax.axvline(0, color='black', lw=1)
        
        ax.set_xlabel("Real Axis")
        ax.set_ylabel("Imaginary Axis")
        ax.grid(True, which='both', linestyle=':', alpha=0.6)
        ax.legend()
        
        # Equal aspect ratio ensures circles look like circles
        ax.set_aspect('equal', 'datalim')
        st.pyplot(fig)

    with col2:
        st.subheader("Data Table (ω → ∞)")
        df = pd.DataFrame({
            "Omega (w)": w,
            "Real": real,
            "Imaginary": imag,
            "Amp Ratio": magnitude,
            "Phase (Deg)": phase
        })
        
        st.dataframe(df.style.format("{:.4f}"), height=500)
        
        # CSV Download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Results (.csv)", csv, "nyquist_results.csv")

except Exception as e:
    st.error(f"⚠️ Calculation Error: {e}")
    st.warning("Ensure your syntax is correct. Example: `sin(w) / w` or `w**2 + 5`.")
