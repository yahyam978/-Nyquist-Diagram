import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

st.title("Interactive Nyquist Plotter")
st.write("Enter the Real and Imaginary parts as functions of `w` (omega).")

# Sidebar for user inputs
with st.sidebar:
    st.header("Transfer Function Components")
    # Example: Re = 1 / (w**2 + 1), Im = -w / (w**2 + 1)
    re_input = st.text_input("Real Part: Re(w)", "1 / (w**2 + 1)")
    im_input = st.text_input("Imaginary Part: Im(w)", "-w / (w**2 + 1)")
    
    st.header("Second Function (Optional)")
    mult_enabled = st.checkbox("Multiply by a second function?")
    re_input2 = st.text_input("Real Part 2: Re2(w)", "1", disabled=not mult_enabled)
    im_input2 = st.text_input("Imaginary Part 2: Im2(w)", "0", disabled=not mult_enabled)

    w_max = st.slider("Max Omega (w)", 0.1, 100.0, 10.0)

# Generate omega values
w = np.linspace(0, w_max, 1000)

try:
    # Evaluate expressions safely
    # Note: simple eval() is used here for demo; in production, use a safer parser.
    Re1 = eval(re_input, {"w": w, "np": np})
    Im1 = eval(im_input, {"w": w, "np": np})
    G1 = Re1 + 1j * Im1

    if mult_enabled:
        Re2 = eval(re_input2, {"w": w, "np": np})
        Im2 = eval(im_input2, {"w": w, "np": np})
        G2 = Re2 + 1j * Im2
        G_total = G1 * G2
    else:
        G_total = G1

    # Plotting
    fig, ax = plt.subplots()
    ax.plot(G_total.real, G_total.imag, label='Nyquist Path')
    ax.plot(G_total.real, -G_total.imag, '--', alpha=0.5, label='Mirror Image') # Conjugate
    
    # Add unit circle and (-1, 0) point for stability context
    ax.plot(-1, 0, 'ro') 
    ax.annotate('(-1, 0j)', (-1, 0), textcoords="offset points", xytext=(0,10), ha='center')
    
    ax.set_xlabel('Real')
    ax.set_ylabel('Imaginary')
    ax.axhline(y=0, color='k', lw=1)
    ax.axvline(x=0, color='k', lw=1)
    ax.grid(True)
    ax.legend()
    
    st.pyplot(fig)

except Exception as e:


# ... (previous input code here) ...

# To simulate "0 to infinity", we use a logspace
# This gives a better distribution of points than linspace
w_values = np.logspace(-2, 3, 500) # From 0.01 to 1000

try:
    # 1. Calculate G1 and G2 based on w_values
    G1 = eval(re_input, {"w": w_values, "np": np}) + 1j * eval(im_input, {"w": w_values, "np": np})
    
    if mult_enabled:
        G2 = eval(re_input2, {"w": w_values, "np": np}) + 1j * eval(im_input2, {"w": w_values, "np": np})
        G_total = G1 * G2
    else:
        G_total = G1

    # 2. Extract Components for the Table
    real_part = G_total.real
    imag_part = G_total.imag
    amplitude = np.abs(G_total)
    # phase in degrees
    angle = np.angle(G_total, deg=True)

    # 3. Create the Dataframe
    df = pd.DataFrame({
        "Omega (ω)": w_values,
        "Real Part": real_part,
        "Imaginary Part": imag_part,
        "Amplitude Ratio": amplitude,
        "Angle (Deg)": angle
    })

    # 4. Display Nyquist Plot
    st.subheader("Nyquist Diagram")
    fig, ax = plt.subplots()
    ax.plot(real_part, imag_part, 'b-', label='G(jω)')
    ax.plot(real_part, -imag_part, 'r--', alpha=0.5, label='Conjugate')
    ax.axhline(0, color='black', lw=1)
    ax.axvline(0, color='black', lw=1)
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

    # 5. Display the Table
    st.subheader("Frequency Response Data Table")
    st.write("Showing variation from $\omega \to 0$ to $\omega \to \infty$ (simulated)")
    st.dataframe(df.style.format("{:.4f}"))

    # Optional: Download button for the data
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Data as CSV", csv, "nyquist_data.csv", "text/csv")

except Exception as e:
    st.error(f"Mathematical Error: {e}")
    st.error(f"Error in expression: {e}")
