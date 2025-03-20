# FlightSense


# Stacking Ensemble: Correct Implementation Guide

## Introduction

Stacking is a powerful ensemble learning technique that leverages multiple base models to improve prediction accuracy. However, improper stacking can lead to data leakage and suboptimal results. This guide explains the correct approach to implementing stacking, ensuring robust performance and proper model generalization.

## Common Mistake in Stacking

A common error is training the base models on the full dataset and then using their predictions as input features for the meta model. This leads to data leakage because the predictions used for training the meta model are generated from models that have already seen the data.

## Correct Approach

To correctly implement stacking, we use K-Fold Cross-Validation to generate Out-of-Fold (OOF) predictions for training the meta model while also producing robust test predictions.

## Step-by-Step Implementation

### 1. Train Base Models with K-Fold Cross-Validation

Perform a grid search (optional) to find the best hyperparameters.

Use K-Fold Cross-Validation (e.g., k=5) to train each base model:

Each iteration uses 4 folds for training and 1 fold for validation.

The validation set’s predictions are stored as OOF predictions (training features for the meta model).

Repeat this for all folds so that every data point has a corresponding prediction.

### 2. Generate OOF Predictions (First Numpy Array)

The predictions for each fold’s validation set are stored in a numpy array, oof_preds.

This forms the training dataset for the meta model.

Instead of using class labels, store predicted probabilities as features:

Binary Classification: If we have M base models, each data point gets M probability values.

Multi-Class Classification: If we have C classes and M models, each data point gets C * M probability values.

### 3. Generate Test Set Predictions (Second Numpy Array)

Since we trained k models, we also generate k predictions for x_test.

The final test predictions are computed by averaging all k predictions.

This ensures the test set predictions are stable and generalizable.

### 4. Train the Meta Model

Use oof_preds as the training dataset for the meta model.

Train the meta model using the OOF predictions as input features.

### 5. Evaluate the Meta Model

Use the averaged test set predictions (x_test_pred) as the final evaluation set.

Compare results against a holdout set or through cross-validation to validate performance.



## Summary of Key Arrays
| Array Name    | Description                                        |
|--------------|------------------------------------------------|
| `oof_preds`  | Training dataset for the meta model (Out-of-Fold predictions) |
| `x_test_pred` | Test set predictions (Averaged across `k` models) |



