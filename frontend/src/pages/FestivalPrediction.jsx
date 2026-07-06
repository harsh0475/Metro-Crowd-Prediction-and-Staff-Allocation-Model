import { useState } from "react";

import PredictionType from "../components/prediction/PredictionType";

import FestivalHourlyForm from "../components/festival/FestivalHourlyForm";
import FestivalShiftForm from "../components/festival/FestivalShiftForm";
import FestivalCalendar from "../components/festival/FestivalCalendar";

function FestivalPrediction() {
  const [predictionType, setPredictionType] = useState("hour");

  return (
    <div className="space-y-8">
      <div>
        <h1 className="page-title">Festival Crowd Prediction</h1>

        <p className="page-subtitle">
          Predict station-wise crowd and required staff during Durga Puja, Christmas and New Year.
        </p>
      </div>

      <FestivalCalendar />

      <PredictionType
        predictionType={predictionType}
        setPredictionType={setPredictionType}
      />

      {predictionType === "hour" ? <FestivalHourlyForm /> : <FestivalShiftForm />}
    </div>
  );
}

export default FestivalPrediction;
