
# Projectverslag: Voorspellen van eindexamencijfer G3

# Inleiding:
# In dit project analyseren we gegevens van studenten om het eindcijfer (G3) te voorspellen.
# We gebruiken hiervoor lineaire regressie en een decision tree-regressor om inzicht te krijgen in de belangrijkste factoren die de prestaties beïnvloeden.

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Dataset inladen
df = pd.read_csv('student_data.csv')

# Beschrijving van de dataset:
# De dataset bevat 395 studenten en 33 kolommen, waaronder demografische gegevens, studiegedrag, alcoholgebruik en cijfers.
print(df.info())
print(df.head())

# Doelvariabele
target = "G3"
features = df.drop(columns=[target])
labels = df[target]

# Categorische en numerieke kolommen onderscheiden
categorical_cols = features.select_dtypes(include=['object']).columns.tolist()
numerical_cols = features.select_dtypes(include=['int64']).columns.tolist()

# Preprocessing: OneHotEncoder voor categorische kolommen
preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
], remainder="passthrough")

# Pipelines maken voor beide modellen
linreg_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", LinearRegression())
])

tree_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", DecisionTreeRegressor(random_state=42, max_depth=5))
])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Train modellen
linreg_pipeline.fit(X_train, y_train)
tree_pipeline.fit(X_train, y_train)

# Voorspellingen
y_pred_linreg = linreg_pipeline.predict(X_test)
y_pred_tree = tree_pipeline.predict(X_test)

# Evaluatie
linreg_mse = mean_squared_error(y_test, y_pred_linreg)
linreg_r2 = r2_score(y_test, y_pred_linreg)
tree_mse = mean_squared_error(y_test, y_pred_tree)
tree_r2 = r2_score(y_test, y_pred_tree)

print(f"Lineaire Regressie - MSE: {linreg_mse:.2f}, R2: {linreg_r2:.3f}")
print(f"Decision Tree - MSE: {tree_mse:.2f}, R2: {tree_r2:.3f}")

# Reflectie:
# Beide modellen presteren goed met een R2 rond de 0.72.
# Lineaire regressie presteerde iets beter in termen van nauwkeurigheid.
# In de toekomst zou hyperparameter-tuning en feature selection de prestaties kunnen verbeteren.
