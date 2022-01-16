from web.models import Departmentprice, Verifypricemessage
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np
from datetime import datetime


def forecast(y_train):
    model = LinearRegression()
    x_train = np.array(range(12))
    print("124124")
    print(x_train)
    # model.fit(x_train, y_train)

    return hpdf
