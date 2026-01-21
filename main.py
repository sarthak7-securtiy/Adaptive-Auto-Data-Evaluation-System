from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
import pandas as pd
import io
import json
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import warnings

warnings.filterwarnings('ignore')

import uuid

# Global store for active sessions (In-memory for demo; use Redis/DB for production)
sessions = {}

app = FastAPI(title="Adaptive Auto Data Evaluation System")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("static/index.html", "r") as f:
        return f.read()

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename
    content = await file.read()
    
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(content))
        elif filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(io.BytesIO(content))
        elif filename.endswith('.json'):
            df = pd.read_json(io.BytesIO(content))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
            
        # Basic understanding module
        # Handle non-serializable types like Timestamp and standard datetime
        preview_df = df.head(10).copy()
        for col in preview_df.columns:
            # Check if column is datetime-like
            if pd.api.types.is_datetime64_any_dtype(preview_df[col]):
                preview_df[col] = preview_df[col].astype(str)
            elif preview_df[col].dtype == 'object':
                # Attempt to catch any stray datetime objects in overflow/object columns
                try:
                    preview_df[col] = preview_df[col].apply(lambda x: str(x) if hasattr(x, 'isoformat') else x)
                except:
                    pass
            
        summary = {
            "columns": [str(c) for c in df.columns],
            "shape": list(df.shape),
            "missing_values": {str(k): int(v) for k, v in df.isnull().sum().to_dict().items()},
            "data_types": {str(col): str(dtype) for col, dtype in df.dtypes.items()},
            "preview": preview_df.replace({np.nan: None}).to_dict(orient='records')
        }
        
        # generate session id
        session_id = str(uuid.uuid4())
        sessions[session_id] = df
        
        return JSONResponse(content={"status": "success", "session_id": session_id, "summary": summary})
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze")
async def analyze_data(request: dict):
    try:
        session_id = request.get("session_id")
        df = sessions.get(session_id)
        
        if df is None:
            return JSONResponse(
                status_code=400, 
                content={"status": "error", "message": "Session expired or invalid. Please re-upload your file."}
            )
        
        analysis_type = request.get("type", "descriptive")
        numeric_df = df.select_dtypes(include=[np.number]).dropna()
        
        insights = []
        chart_data = {"labels": [], "values": []}

        # Real ML logic
        if analysis_type == "clustering" and not numeric_df.empty:
            if len(numeric_df) < 2:
                insights.append({"type": "warning", "text": "Insufficient data for clustering (need >= 2 rows)."})
            else:
                scaler = StandardScaler()
                scaled_data = scaler.fit_transform(numeric_df)
                num_clusters = min(3, len(scaled_data))
                kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init='auto').fit(scaled_data)
                
                counts = np.bincount(kmeans.labels_)
                chart_data = {
                    "labels": [f"Cluster {i+1}" for i in range(len(counts))],
                    "values": [int(c) for c in counts]
                }
                insights.append({"type": "ml", "text": f"K-Means identified {len(counts)} patterns in the numeric data."})

        elif analysis_type == "prediction" and not numeric_df.empty:
            if len(numeric_df) < 5 or numeric_df.shape[1] < 2:
                insights.append({"type": "warning", "text": "Predictive modeling requires multiple numeric columns and sufficient rows."})
            else:
                # Use the last column as target, others as features
                X = numeric_df.iloc[:, :-1].values
                y = numeric_df.iloc[:, -1].values
                target_name = numeric_df.columns[-1]
                
                model = LinearRegression().fit(X, y)
                score = model.score(X, y)
                
                # Predict on same data for visualization (Actual vs Predicted comparison could be better, 
                # but for simplicity we show the first 10 actual values of target)
                chart_data = {
                    "labels": [f"Sample {i+1}" for i in range(min(10, len(y)))],
                    "values": [float(v) for v in y[:10]]
                }
                insights.append({"type": "ml", "text": f"Linear Regression model trained to predict '{target_name}' (R²={score:.2f})."})

        elif analysis_type == "correlation" and not numeric_df.empty:
            corr = numeric_df.corr()
            if not corr.empty and len(numeric_df.columns) > 1:
                # Find strongest pair
                unstacked = corr.abs().unstack()
                # Remove self correlations and duplicates
                pairs = unstacked.sort_values(ascending=False)
                pairs = pairs[pairs < 1.0] 
                
                if not pairs.empty:
                    (f1, f2), val = pairs.index[0], pairs.iloc[0]
                    insights.append({"type": "stat", "text": f"Strongest correlation found between '{f1}' and '{f2}' (r={val:.2f})."})
            
            chart_data = {
                "labels": [str(c) for c in numeric_df.columns[:5]],
                "values": [float(v) for v in numeric_df.mean()[:5]]
            }
        
        # Fallback/Descriptive
        if not insights:
            insights.append({"type": "stat", "text": f"Summary check: Found {len(df)} rows and {len(df.columns)} features."})
            if not numeric_df.empty:
                chart_data = {
                    "labels": [str(c) for c in numeric_df.columns[:5]],
                    "values": [float(v) for v in numeric_df.mean()[:5]]
                }

        return {
            "status": "success", 
            "analysis": {
                "type": analysis_type,
                "viz_preference": request.get("viz", "auto"),
                "insights": insights,
                "chart_data": chart_data
            }
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"Analytical engine error: {str(e)}"}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
