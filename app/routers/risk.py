"""
app/routers/risk.py

Risk Prediction API Endpoints (M1 Interface):
- GET /api/v1/risk/location?lat=27.55&lon=93.65
- GET /api/v1/risk/area?min_lat=...&max_lat=...&min_lon=...&max_lon=...
"""

from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.ml_service import ml_service
from app.schemas.risk import RiskResponse
from app.schemas.field_report import GeoJSONFeatureCollection, GeoJSONFeature, GeoJSONGeometry

router = APIRouter(prefix="/risk", tags=["Landslide Risk"])


@router.get("/location", response_model=RiskResponse)
async def get_risk_by_location(
    lat: float = Query(..., ge=-90.0, le=90.0, description="Latitude (e.g. 27.55)"),
    lon: float = Query(..., ge=-180.0, le=180.0, description="Longitude (e.g. 93.65)"),
    rainfall_24h: float = Query(45.0, description="Recent 24h rainfall in mm"),
    slope: float = Query(25.0, description="Terrain slope in degrees"),
    db: AsyncSession = Depends(get_db),
):
    """
    Get AI risk prediction for a specific coordinate (M1 ML integration endpoint).
    """
    features = {
        "latitude": lat,
        "longitude": lon,
        "rainfall_24h": rainfall_24h,
        "slope": slope,
        "soil_moisture": 0.42,
    }

    prediction = await ml_service.predict_risk(features)

    return RiskResponse(
        latitude=lat,
        longitude=lon,
        risk_score=prediction["risk_score"],
        risk_level=prediction["risk_level"],
        confidence=prediction["confidence"],
        model_version=prediction["model_version"],
        feature_snapshot=prediction["feature_snapshot"],
        timestamp=datetime.now(timezone.utc),
    )


@router.get("/area", response_model=GeoJSONFeatureCollection)
async def get_risk_area(
    min_lat: float = Query(26.0, ge=-90.0, le=90.0),
    max_lat: float = Query(28.0, ge=-90.0, le=90.0),
    min_lon: float = Query(91.0, ge=-180.0, le=180.0),
    max_lon: float = Query(94.0, ge=-180.0, le=180.0),
):
    """
    Get spatial grid of risk levels as GeoJSON FeatureCollection for bounding box (M4 GIS Dashboard layer).
    """
    features = []
    # Sample grid resolution simulation for NER region
    lat_steps = 3
    lon_steps = 3
    lat_delta = (max_lat - min_lat) / lat_steps
    lon_delta = (max_lon - min_lon) / lon_steps

    for i in range(lat_steps):
        for j in range(lon_steps):
            c_lat = min_lat + (i + 0.5) * lat_delta
            c_lon = min_lon + (j + 0.5) * lon_delta
            
            pred = await ml_service.predict_risk({"rainfall_24h": 55.0, "slope": 30.0})

            feature = GeoJSONFeature(
                type="Feature",
                geometry=GeoJSONGeometry(
                    type="Point",
                    coordinates=[round(c_lon, 4), round(c_lat, 4)],
                ),
                properties={
                    "risk_score": pred["risk_score"],
                    "risk_level": pred["risk_level"],
                    "confidence": pred["confidence"],
                    "model_version": pred["model_version"],
                },
            )
            features.append(feature)

    return GeoJSONFeatureCollection(type="FeatureCollection", features=features)
