import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import streamlit as st


def graph(data, siteID):
    filtered = data[data['siteID'] == siteID].sort_values('Tiempo', ascending = False)
    myFmt = mdates.DateFormatter('%d/%m')
    fig, ax = plt.subplots(2, 1, figsize=(14, 7), layout='constrained', sharex=True)
    ax[0].xaxis.set_major_formatter(myFmt)
    ax[0].xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax[1].xaxis.set_major_formatter(myFmt)
    ax[1].xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax[0].plot(filtered['Tiempo'], filtered['meanLost'])
    ax[1].plot(filtered['Tiempo'], filtered['maxLost'])
    ax[0].set_title('Mean Lost')
    ax[1].set_title('Max Lost')
    fig.suptitle(filtered.iloc[0]['Nombre Sitio'])
    ax[0].grid(True)
    ax[1].grid(True)
    st.pyplot(fig)