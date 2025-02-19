# pylint: disable=line-too-long
"""
Escriba el codigo que ejecute la accion solicitada.
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

def pregunta_01():
    """
    El archivo `files//shipping-data.csv` contiene información sobre los envios
    de productos de una empresa. Cree un dashboard estático en HTML que
    permita visualizar los siguientes campos:

    * `Warehouse_block`

    * `Mode_of_Shipment`

    * `Customer_rating`

    * `Weight_in_gms`

    El dashboard generado debe ser similar a este:

    https://github.com/jdvelasq/LAB_matplotlib_dashboard/blob/main/shipping-dashboard-example.png

    Para ello, siga las instrucciones dadas en el siguiente video:

    https://youtu.be/AgbWALiAGVo

    Tenga en cuenta los siguientes cambios respecto al video:

    * El archivo de datos se encuentra en la carpeta `data`.

    * Todos los archivos debe ser creados en la carpeta `docs`.

    * Su código debe crear la carpeta `docs` si no existe.

    """

    if os.path.exists('docs'):
        os.system('rm -rf docs')
    
    os.makedirs('docs')

    dfp = pd.read_csv('files/input/shipping-data.csv')
    dfp2 = dfp.copy()
    cuenteos = dfp2['Warehouse_block'].value_counts()
    cuenteos.plot.bar(
        title="Shipping per warehouse",
        xlabel="Warehouse block",
        ylabel="Record count",
        color="tab:blue",
        fontsize=8
    )
    
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.savefig('docs/shipping_per_warehouse.png')

    dfp3 = dfp.copy()
    plt.figure()
    cuenteos = dfp3['Mode_of_Shipment'].value_counts()
    cuenteos.plot.pie(
        title="Mode of shipment",
        wedgeprops=dict(width=0.35),
        ylabel="",
        colors=["tab:blue", "tab:orange", "tab:green"],
    )
    plt.savefig('docs/mode_of_shipment.png')

    dfp4 = dfp.copy()
    plt.figure()
    dfp4 = (
        dfp4[["Mode_of_Shipment", "Customer_rating"]]
        .groupby("Mode_of_Shipment")
        .describe()
    )
    dfp4.columns = dfp4.columns.droplevel()
    dfp4 = dfp4[["mean", "min", "max"]]
    plt.barh(
        y=dfp4.index.values,
        width=dfp4["max"].values - 1,
        left=dfp4["min"].values,
        height=0.9,
        color="lightgray",
        alpha=0.8,
    )

    colors = [
    "tab:green" if value >= 3.0 else "tab:orange" for value in dfp4 ["mean"]. values]

    plt.barh(
        y=dfp4.index.values,
        width=dfp4 ["mean"].values - 1,
        left=dfp4 ["min"].values,
        color=colors,
        height=0.5,
        alpha=1.0,
    )
    plt.title("Average Customer Rating")
    plt.gca().spines["left"].set_color("gray")
    plt.gca().spines["bottom"].set_color("gray")
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)

    plt.savefig("docs/average_customer_rating.png")
    
    dfp5 = dfp.copy()
    plt.figure()
    dfp5.Weight_in_gms.plot.hist(
        title="Shipped Weight Distribution",
        color="tab:orange",
        edgecolor="white",
    )
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.savefig("docs/weight_distribution.png")

    # crear html
    html = """
<!DOCTYPE html>
<html lang="en">
<body>
    <h1>Shipping Dashboard Example</h1>
    <div style="width: 45%; float: left">
    <img src="shipping_per_warehouse.png" alt="Fig 1" />
    <img src="mode_of_shipment.png" alt="Fig 2" />
    </div>
    <div style="width: 45%; float: left">
    <img src="average_customer_rating.png" alt="Fig 3" />
    <img src="weight_distribution.png" alt="Fig 4" />
    </div>
</body>
</html>
    """

    # crear index.html
    os.system("touch docs/index.html")
    with open("docs/index.html", "w") as file:
        file.write(html)
    