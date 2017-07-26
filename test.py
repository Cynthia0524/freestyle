import Markowitz_Frontier as mf
import csv
import numpy as np

port_price = mf.read_prices("ASSET.csv")

returns = mf.get_return(port_price)
print(returns)
