from covid19_data_fetch import fetch_data
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU
from matplotlib.colors import CSS4_COLORS as mcolor_css
import numpy as np


line_colors = [mcolor_css["bisque"],            # Ahvenanmaa
               mcolor_css["cadetblue"],         # Satakunta
               mcolor_css["dimgrey"],           # Varsinais-Suomi
               mcolor_css["goldenrod"],         # Kanta-Häme
               mcolor_css["darkorange"],        # Pirkanmaa
               mcolor_css["khaki"],             # Päijät-Häme
               mcolor_css["mediumblue"],        # Kymenlaakso
               mcolor_css["darkgoldenrod"],     # Etelä-Karjala
               mcolor_css["yellow"],            # Etelä-Savo
               mcolor_css["firebrick"],         # Itä-Savc
               mcolor_css["darkred"],           # Pohjois-Karjala
               mcolor_css["palegoldenrod"],     # Pohjois-Savo
               mcolor_css["green"],             # Keski-Suomi
               mcolor_css["darkgrey"],          # Etelä-Pohjanmaa
               mcolor_css["tan"],               # Vaasa
               mcolor_css["lightsteelblue"],    # Keski-Pohjanmaa
               mcolor_css["slategrey"],         # Pohjois-Pohjanmaa
               mcolor_css["saddlebrown"],       # Kainuu
               mcolor_css["powderblue"],        # Länsi-Pohja
               mcolor_css["paleturquoise"],     # Lappi
               mcolor_css["cornflowerblue"],    # Helsinki & Uusimaa
               mcolor_css["red"],               # All districts
               mcolor_css["whitesmoke"]]        # Mundane numbers

hcds, dates, maximum_value = fetch_data()

#today = date.today()
formatter = mdates.DateFormatter('%d/%m')
fig, ax = plt.subplots()
j = 0
for hcd in hcds:
    if hcd.infected_total < 0:
        line, = plt.plot_date(dates[7:], hcd.fiveDMA[1:], '-o', xdate=True, label=hcd.name,
                              color=str(line_colors[22]))
    else:
        line, = plt.plot_date(dates[7:], hcd.fiveDMA[1:], '-o', xdate=True, label=hcd.name,
                              color=str(line_colors[j]))
    j += 1

plt.yticks(np.arange(0, maximum_value, 5))
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=(MO,TU,WE,TH,FR,SA,SU), interval= 1))
ax.xaxis.set_major_formatter(formatter)
ax.xaxis.set_minor_locator(mdates.AutoDateLocator())
ax.grid(True)
plt.legend([hcd.name for hcd in hcds])
plt.show()