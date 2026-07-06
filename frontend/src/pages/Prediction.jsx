import { useState } from "react";

import PredictionType from "../components/prediction/PredictionType";

import HourlyForm from "../components/prediction/HourlyForm";

import ShiftForm from "../components/prediction/ShiftForm";

function Prediction() {
  const [predictionType, setPredictionType] = useState("hour");

  return (
    <div className="space-y-8">
      <div>
        <h1 className="page-title">Crowd Prediction</h1>

        <p className="page-subtitle">
          Predict crowd and staff requirement for an entire metro line.
        </p>
      </div>

      <PredictionType
        predictionType={predictionType}
        setPredictionType={setPredictionType}
      />

      {predictionType === "hour" ? <HourlyForm /> : <ShiftForm />}
    </div>
  );
}

export default Prediction;
