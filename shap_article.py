#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import shap


output_path = os.path.join(os.getcwd(), "output")

def plot_export_corr(df, x, y, output_path):
    plt.scatter(x=df[x], y=df[y])
    plt.savefig(output_path + "\\corr_{}.png".format(x))
    plt.clf()

def plot_feature_importance(model, names):
    coeffs = [(name, coef) for name, coef in zip(names, model.coef_)]
    for coef in coeffs:
        print("Feature: {}, Score: {}".format(coef[0], coef[1]))
    plt.bar([coef[0] for coef in coeffs], [k[1] for k in coeffs])
    plt.savefig(output_path + "\\var_impt.png")
    plt.clf()

df = pd.read_csv("insurance.csv")

rating_factors =  list(df.columns[:-1])
claims = df.columns[-1]


rating_factors_encoded = pd.get_dummies(df[rating_factors])

X_train, X_test, y_train, y_test = train_test_split(
            rating_factors_encoded,
            df[claims],
            test_size=0.2,
            random_state=123
        )


lm = LinearRegression()
lm.fit(X_train, y_train)

plot_feature_importance(lm, list(rating_factors_encoded.columns))


background = shap.maskers.Independent(X_train, max_samples=1000)
explainer = shap.LinearExplainer(lm, X_train)
shap_values = explainer(X_train)

idx = 1

shap.plots.beeswarm(shap_values, show=False)
plt.savefig(output_path + "\\shap_summary_plot.png")
plt.clf()


shap.plots.waterfall(shap_values[idx], max_display=14, show=False)
plt.figure(figsize=(20, 10))
plt.savefig(output_path + "\\shap_waterfall_plot.png")
plt.clf()


shap.force_plot(explainer.expected_value, shap_values)
plt.savefig(output_path + "\\shap_plot_{}.png".format(idx))
plt.clf()

#shap.force_plot(shap_values, rating_factors_encoded, matplotlib=True, show=False)
#plt.savefig(output_path + "\\shap_plot_stacked.png")



if __name__ == "__main__":
    for factor in rating_factors:
        plot_export_corr(df, factor, claims, output_path)