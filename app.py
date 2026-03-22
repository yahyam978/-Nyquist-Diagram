import pandas as pd

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
