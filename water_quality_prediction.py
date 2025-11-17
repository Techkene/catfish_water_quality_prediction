#!/usr/bin/env python
# coding: utf-8

# # Catfish Water Quality Prediction Model
# This notebook loads water quality data, preprocesses it, trains a machine learning model, and predicts water quality status for catfish farming.

# In[ ]:





# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib

# Set plot style
sns.set(style="whitegrid")


# ## Problem Definition & ML Strategy
# 
# ### The Problem
# The dataset (`WQD.xlsx`) contains various chemical and biological water quality measurements, such as temperature, dissolved oxygen (DO), pH, and turbidity. The final column, "Water Quality," is our target variable.
# 
# Based on the snippets, the "Water Quality" column contains discrete integer values (e.g., 0, 2), indicating this is a **classification problem**. The goal is to build a model that can predict the water quality class based on the other measurements.
# 
# ### How ML Can Help
# A machine learning classification model can learn the complex, non-linear relationships between the different measurements and the resulting water quality.
# 
# * **Prediction:** Once trained, the model can instantly classify new water samples, providing a real-time monitoring tool.
# * **Insight:** The model can help identify which factors (e.g., 'BOD', 'Turbidity') are the most important predictors of poor water quality.
# * **Automation:** This automates a potentially slow and complex manual assessment process, allowing for faster responses to pollution events.

# In[2]:


# Load the dataset
file_name = 'WQD.xlsx'
df = pd.read_excel(file_name)

# --- Data Cleaning (from snippet inspection) ---
# The 'pH`' column in the snippet has a trailing backtick. Let's fix it.
if 'pH`' in df.columns:
    df = df.rename(columns={'pH`': 'pH'})


# In[3]:


# Display first few rows and data types
print(df.head())
print("\n" + "="*50 + "\n")
print(df.info())
print(df.describe())


# In[4]:


# Check for missing values
print("Missing values per column:")
print(df.isnull().sum())



# In[5]:


# Simple imputation: fill missing values with the median of the column
# (Median is more robust to outliers than mean)
for col in df.columns:
    if df[col].isnull().any():
        median_val = df[col].median()
        df[col] = df[col].fillna(median_val)
        print(f"Filled NaNs in '{col}' with median: {median_val}")


# In[6]:


# Define Features (X) and Target (y)
target = 'Water Quality'
X = df.drop(target, axis=1)
y = df[target]


# ## Exploratory Data Analysis (EDA))

# In[7]:


# 1. Target Variable Distribution
plt.figure(figsize=(8, 5))
sns.countplot(x=y)
plt.title('Distribution of Water Quality Classes')
plt.xlabel('Water Quality Class')
plt.ylabel('Count')
plt.show()



# In[8]:


# 2. Correlation Heatmap
plt.figure(figsize=(18, 12))
sns.heatmap(df.corr(), annot=True, fmt='.2f', cmap='coolwarm', annot_kws={"size": 8})
plt.title('Correlation Heatmap of All Features')
plt.show()



# In[9]:


# 3. Feature Distributions
X.hist(bins=30, figsize=(20, 15), layout=(5, 3))
plt.suptitle('Histograms of Feature Distributions')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()


# ## Preprocessing and Splitting

# In[10]:


# Split data into training and testing sets
# We use stratify=y to ensure the class distribution is the same in train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Scale the features
# ML models (especially linear ones) perform better when features are on a similar scale.
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# In[11]:


# We will try three common, powerful classifiers
models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Random Forest': RandomForestClassifier(random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(random_state=42)
}



# In[12]:


# Iterate, train, and evaluate
for name, model in models.items():
    print(f"--- Training {name} ---")
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(classification_report(y_test, y_pred))
    print("\n")

# Random Forest and Gradient Boosting usually perform best out-of-the-box.
# Let's pick Random Forest to tune.


# ## Hyperparameter Tuning

# In[13]:


# Define a smaller, faster parameter grid for demonstration
# You can expand this for a more exhaustive search
param_grid = {
    'n_estimators': [100, 200],      # Number of trees
    'max_depth': [10, 20, None],     # Max depth of trees
    'min_samples_split': [2, 5],     # Min samples to split a node
    'min_samples_leaf': [1, 2]       # Min samples at a leaf node
}


# In[14]:


# Use GridSearchCV to find the best parameters
# cv=3 for 3-fold cross-validation (faster)
grid_search = GridSearchCV(
    estimator=RandomForestClassifier(random_state=42),
    param_grid=param_grid,
    cv=3,
    n_jobs=-1,  # Use all available CPU cores
    scoring='accuracy',
    verbose=1
)


# In[15]:


grid_search.fit(X_train_scaled, y_train)

print(f"\nBest parameters found: {grid_search.best_params_}")
best_model = grid_search.best_estimator_


# ## Model Evaluation

# In[16]:


# Evaluate the tuned model on the test set
y_pred_final = best_model.predict(X_test_scaled)


print(f"Accuracy: {accuracy_score(y_test, y_pred_final):.4f}")
print(classification_report(y_test, y_pred_final))


# In[17]:


# Plot confusion matrix
cm = confusion_matrix(y_test, y_pred_final)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=np.unique(y), yticklabels=np.unique(y))
plt.title('Confusion Matrix')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()


# ## Save Model, Scaler, and Columns

# In[18]:


# Save the three essential components for deployment
model_columns = list(X.columns)
joblib.dump(best_model, 'water_quality_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
joblib.dump(model_columns, 'model_columns.pkl')

print("Model, scaler, and column list saved to disk.")
print(f"Model columns: {model_columns}")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




