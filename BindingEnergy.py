import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colormaps


st.set_page_config(layout="wide")


st.sidebar.header("Coefficients")
a1 = st.sidebar.number_input("Volume term (MeV)", value=	15.76)
a2 = st.sidebar.number_input("Surface term (MeV)", value=17.81)
a3 = st.sidebar.number_input("Coulomb term (MeV)", value=0.711)
a4 = st.sidebar.number_input("Asymmetry term (MeV)", value=23.702)
a5 = st.sidebar.number_input("Pairing term (MeV)", value=34)
p = st.sidebar.number_input("Power of A in pairing term", value = -0.75)
st.sidebar.markdown("""---""")
st.sidebar.header("Color and scale")
size_choice = st.sidebar.slider("Size",10, 1000, 200, 10)
colormap = st.sidebar.selectbox("Colormap", ["coolwarm"]+list(colormaps))
multiplication_factor = st.sidebar.number_input("Multiplication factor", value = 1.0)
should_round = st.sidebar.toggle("Round(floor)", value = True)
autoscale = st.sidebar.toggle("Autoscale", value = False)
if autoscale:
    scale_min = None
    scale_max = None
else:
    scale_min = st.sidebar.number_input("Scale minimum", value = -8.0)
    scale_max = st.sidebar.number_input("Scale maximum", min_value=scale_min, value=8.0)
st.sidebar.markdown("""---""")
st.sidebar.header("Turn on/off coefficients")
a1_on = st.sidebar.toggle("Volume term", value = True)
a2_on = st.sidebar.toggle("Surface term", value = True)
a3_on = st.sidebar.toggle("Coulomb term", value = True)
a4_on = st.sidebar.toggle("Asymmetry term", value = True)
a5_on = st.sidebar.toggle("Pairing term", value = True)

size = (size_choice, size_choice)

@st.cache_data
def f1(size):
    array = np.empty(size)
    for n in range(len(array)):
        for z in range(len(array[0])):
            array[n][z] = n+z
    return array

@st.cache_data
def f2(size):
    array = np.power(f1(size), 2/3)
    return array

@st.cache_data
def f3(size):
    array = np.power(f1(size), -1/3)

    for n in range(len(array)):
        for z in range(len(array[0])):
            array[n][z] *= z*(z-1)
    return array

@st.cache_data
def f4(size):
    array = np.divide(1,f1(size))
    for n in range(len(array)):
        for z in range(len(array[0])):
            array[n][z] *= (n-z)**2
    return array

@st.cache_data
def f5(size, p):
    array = np.zeros(size)
    array[::2,::2] = f1(size)[::2,::2] ** p
    array[1::2, 1::2] = -f1(size)[1::2, 1::2] ** p
    return array

sum = a1_on*a1*f1(size) - a2_on*a2*f2(size) - a3_on*a3*f3(size) - a4_on*a4*f4(size) + a5_on*a5*f5(size, p)
sum = multiplication_factor*sum/f1(size)

title = r"$B(MeV) = $ " + str(a1) + r"$A -$ " + str(a2) + r"$ A^\frac{2}{3} -$ " +str(a3)+ r"$\frac{Z(Z-1)}{A^\frac{1}{3}} - $ " + str(a4) + r"$\frac{(N-Z)^2}{A} \pm $ " + str(a5) + f"A^{p}"
st.subheader(title)

fig = plt.figure(facecolor="darkgray")
if should_round:
    plt.imshow(np.floor(np.transpose(sum)), cmap=colormap, vmin=scale_min, vmax = scale_max, origin='lower')
else:
    plt.imshow(np.transpose(sum), cmap=colormap, vmin=scale_min, vmax=scale_max, origin='lower')
plt.colorbar()
plt.xlabel("#P")
plt.ylabel("#N")
plt.title("binding energy of nucleus / A (MeV)")
st.pyplot(fig, use_container_width=False)


