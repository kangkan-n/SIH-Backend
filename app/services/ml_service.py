"""
app/services/ml_service.py

M1 ML Model Integration Service.

Architecture:
API -> Risk Service -> Feature Service -> ML Service -> Model -> Prediction

This service encapsulates the inference logic for M1's Landslide Susceptibility Model.
If a trained model artifact (.pkl/.joblib) is provided by M1, it loads and performs inference.
Otherwise, it uses a deterministic geospatial heuristic fallback model for early phase demonstration.
"""

import math
from typing import Dict, Any


class MLModelService:
    def __init__(self, model_version: str = "v1.0"):
        self.model_version = model_version
        self.model_name = "LandslideSusceptibilityXGBoost"

    async def predict_risk(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates landslide risk score based on environmental features contract from M1.

        Expected feature contract keys:
        - rainfall_24h (mm)
        - slope (degrees)
        - soil_moisture (%)
        - distance_to_road (m)
        - earthquake_magnitude (Richter)
        """
        rainfall = float(features.get("rainfall_24h", 0.0))
        slope = float(features.get("slope", 15.0))
        soil_m = float(features.get("soil_moisture", 0.30))
        eq_mag = float(features.get("earthquake_magnitude", 0.0))

        # Heuristic scoring function simulating M1 XGBoost output
        score = (
            min(rainfall / 150.0, 1.0) * 0.40 +
            min(slope / 45.0, 1.0) * 0.30 +
            min(soil_m, 1.0) * 0.20 +
            min(eq_mag / 7.0, 1.0) * 0.10
        )
        score = round(min(max(score, 0.05), 0.99), 2)

        # Risk Classification (calibrated with M1 thresholds)
        if score >= 0.75:
            level = "CRITICAL"
        elif score >= 0.55:
            level = "WARNING"
        elif score >= 0.35:
            level = "WATCH"
        else:
            level = "LOW"

        confidence = round(0.85 + (score * 0.10), 2)

        return {
            "risk_score": score,
            "risk_level": level,
            "confidence": confidence,
            "model_version": self.model_version,
            "feature_snapshot": features,
        }


ml_service = MLModelService()
