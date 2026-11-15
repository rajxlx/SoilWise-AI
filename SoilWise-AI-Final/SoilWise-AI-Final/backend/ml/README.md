# Optional ML training workspace

The API runtime intentionally does not pretend a model exists. No labeled soil dataset was supplied with this project, so no trained weights, accuracy claims, Grad-CAM maps, SHAP values, or image-derived nutrient diagnoses are included.

## Image model dataset

Prepare an ethically sourced, consented, expert-labeled dataset in ImageFolder layout:

```text
dataset/soil_images/
  train/
    sandy/
    clay/
    loamy/
  val/
    sandy/
    clay/
    loamy/
```

Use labels that describe the actual task. Do not label nutrient deficiency from appearance unless a paired laboratory measurement and agronomist-reviewed label supports it. Keep farms/fields separated across train and validation/test splits to avoid leakage. Record provenance, location, date, camera, soil moisture, lighting, lab method, and label reviewer.

Run from `backend/` after installing `requirements-ml.txt`:

```bash
python train_image_model.py --data-dir ml/data/soil_images --output ml/artifacts/soil_resnet50.pt --epochs 10
```

## Structured model dataset

CSV columns: `nitrogen`, `phosphorus`, `potassium`, `ph`, `organic_matter`, `moisture`, and `target`. N/P/K units must be consistent (currently assumed mg/kg); the target must be a reviewed classification label. Run:

```bash
python train_tabular_model.py --csv ml/data/soil_lab_results.csv --output ml/artifacts/soil_tabular.joblib
```

The script reports held-out metrics and writes a fitted scikit-learn pipeline. Do not deploy unless the holdout split is farm/region-aware, class balance is reviewed, calibration is checked, and an independent regional test set passes agronomist review. The scripts are training utilities, not a production inference integration.
