import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier


df = pd.read_csv("irrigation_prediction.csv")


X = df.drop(["Soil_pH","Organic_Carbon","Electrical_Conductivity","Crop_Growth_Stage","Season","Irrigation_Type","Water_Source","Field_Area_hectare","Mulching_Used","Region","Irrigation_Need"], axis=1)
y = df["Irrigation_Need"]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


numeric_features = X.select_dtypes(
    include=["int64", "float64"]
).columns


categorical_features = X.select_dtypes(
    include=["object"]
).columns


numeric_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="mean")),
    ("scaler", StandardScaler())
])


categorical_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])


preprocessor = ColumnTransformer([
    ("num", numeric_transformer, numeric_features),
    ("cat", categorical_transformer, categorical_features)
])


model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(
        n_estimators=200,
        random_state=42
    ))
])


model.fit(X_train, y_train)


joblib.dump(model, "irrigation_model.pkl")
print("done")
