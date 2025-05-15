import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Titanic datasetini yükləyək
titanic = sns.load_dataset('titanic')
#titanic = pd.read_csv("titanic.csv")

# Datasetə ilkin baxış
print("Dataset ölçüsü:", titanic.shape)
print("\nİlk 5 sətir:")
print(titanic.head())

# Sütunların növü və boş dəyərlərin sayı
print("\nDəyişənlərin növü və boş dəyərlər:")
print(titanic.info())

# Statistik məlumat
print("\nStatistik məlumat:")
print(titanic.describe())

# Boş dəyərlərin sayı
print("\nHər sütundakı boş dəyərlər:")
print(titanic.isnull().sum())

# Datasetdə korrelasiya analizi və vizualizasiyası
plt.figure(figsize=(12, 8))
correlation = titanic.select_dtypes(include=['float64', 'int64']).corr()
sns.heatmap(correlation, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Korrelasiya Matrisi')
plt.tight_layout()

# Sağ qalanların sayı
plt.figure(figsize=(8, 6))
sns.countplot(x='survived', data=titanic)
plt.title('Sağ qalanlar və həlak olanlar')
plt.xlabel('Sağ qalma (0: Həlak olub, 1: Sağ qalıb)')
plt.ylabel('Sərnişin sayı')

# Cinslərə görə sağ qalma nisbəti
plt.figure(figsize=(8, 6))
sns.countplot(x='sex', hue='survived', data=titanic)
plt.title('Cinslərə görə sağ qalma nisbəti')
plt.xlabel('Cins')
plt.ylabel('Sərnişin sayı')
plt.legend(['Həlak olub', 'Sağ qalıb'])

# Sərnişin siniflərinə görə sağ qalma nisbəti
plt.figure(figsize=(8, 6))
sns.countplot(x='class', hue='survived', data=titanic)
plt.title('Sərnişin siniflərinə görə sağ qalma nisbəti')
plt.xlabel('Sinif')
plt.ylabel('Sərnişin sayı')
plt.legend(['Həlak olub', 'Sağ qalıb'])

# Yaş qruplarına görə sağ qalma nisbəti
plt.figure(figsize=(12, 6))
sns.histplot(data=titanic, x='age', hue='survived', multiple='stack', bins=20)
plt.title('Yaş qruplarına görə sağ qalma nisbəti')
plt.xlabel('Yaş')
plt.ylabel('Sərnişin sayı')

# Data hazırlığı
# Hədəf və xüsusiyyətləri ayıraq
X = titanic.drop(['survived', 'alive'], axis=1)  # 'alive' sütunu 'survived' ilə eynidir
y = titanic['survived']

# Kateqoriyalı və ədədi sütunları ayıraq
categorical_cols = ['sex', 'embarked', 'class', 'who', 'adult_male', 'deck', 'embark_town', 'alone']
numerical_cols = ['age', 'pclass', 'sibsp', 'parch', 'fare']

# Preprocessing pipelines
numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# ColumnTransformer ilə preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
    ])

# Model yaradaq - RandomForest istifadə edək
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42))
])

# Train və test məlumatlarını ayıraq
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modeli öyrədək
model.fit(X_train, y_train)

# Test məlumatları üzərində proqnozlar
y_pred = model.predict(X_test)

# Model qiymətləndirməsi
print("\nTest məlumatları üzərində dəqiqlik:", accuracy_score(y_test, y_pred))
print("\nTəsnifat hesabatı:")
print(classification_report(y_test, y_pred))

# Qarışıqlıq matrisi
plt.figure(figsize=(8, 6))
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Qarışıqlıq Matrisi')
plt.xlabel('Proqnoz')
plt.ylabel('Həqiqi')

# Hyperparameter tuning - GridSearchCV
param_grid = {
    'classifier__n_estimators': [50, 100, 200],
    'classifier__max_depth': [None, 10, 20],
    'classifier__min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(model, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

print("\nƏn yaxşı parametrlər:", grid_search.best_params_)
print("Ən yaxşı cross-validation nəticəsi:", grid_search.best_score_)

# Ən yaxşı modelin test məlumatları üzərində qiymətləndirilməsi
best_model = grid_search.best_estimator_
y_pred_best = best_model.predict(X_test)

print("\nƏn yaxşı model ilə test məlumatları üzərində dəqiqlik:", accuracy_score(y_test, y_pred_best))
print("\nƏn yaxşı model ilə təsnifat hesabatı:")
print(classification_report(y_test, y_pred_best))

# Xüsusiyyət əhəmiyyətliliyi
feature_names = numerical_cols + list(best_model.named_steps['preprocessor'].transformers_[1][1].named_steps['onehot'].get_feature_names_out(categorical_cols))
feature_importance = best_model.named_steps['classifier'].feature_importances_

# Xüsusiyyət əhəmiyyətliliyini əhəmiyyətə görə sıralayaq
sorted_idx = np.argsort(feature_importance)
plt.figure(figsize=(12, 8))
plt.barh(range(len(sorted_idx)), feature_importance[sorted_idx])
plt.yticks(range(len(sorted_idx)), [feature_names[i] for i in sorted_idx])
plt.title('Xüsusiyyət Əhəmiyyətliliyi')
plt.xlabel('Əhəmiyyətlilik')
plt.tight_layout()

plt.show()