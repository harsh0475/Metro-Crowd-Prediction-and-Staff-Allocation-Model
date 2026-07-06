import { useState } from "react";

import usePrediction from "../../hooks/usePrediction";

import LineSelector from "../dashboard/LineSelector";
import HourSelector from "./HourSelector";

import PredictionResult from "./PredictionResult";

import Loading from "../common/Loading";
import Error from "../common/Error";

import { predictHourly } from "../../services/predictionService";

import {
  getCurrentDate,
  getCurrentHour,
} from "../../utils/date";

function HourlyForm() {
  const {
    lines,
    selectedLine,
    setSelectedLine,
    loading,
  } = usePrediction();

  const [date, setDate] = useState(getCurrentDate());

  const [hour, setHour] = useState(getCurrentHour());

  const [prediction, setPrediction] = useState([]);

  const [predictLoading, setPredictLoading] =
    useState(false);

  const [error, setError] = useState("");

  const handlePredict = async () => {
    if (!date) {
      setError("Please select a date.");
      return;
    }

    try {
      setPredictLoading(true);

      setError("");

      const response = await predictHourly({
        line: selectedLine,
        date,
        hour,
      });

      if (response.success) {
        setPrediction(response.results);
      } else {
        setPrediction([]);
        setError(response.error);
      }
    } catch (err) {
      console.error(err);

      setPrediction([]);

      setError("Prediction failed.");
    } finally {
      setPredictLoading(false);
    }
  };

  return (
    <div className="space-y-6">

      <div className="card border border-base-300 bg-base-100">

        <div className="card-body">

          <h2 className="card-title">

            Hourly Prediction

          </h2>

          <div className="grid gap-5 md:grid-cols-3">

            <LineSelector
              lines={lines}
              selectedLine={selectedLine}
              onChange={setSelectedLine}
            />

            <div>

              <label className="label">

                <span className="label-text">

                  Date

                </span>

              </label>

              <input
                type="date"
                className="input input-bordered w-full"
                value={date}
                onChange={(e) =>
                  setDate(e.target.value)
                }
              />

            </div>

            <HourSelector
              selectedHour={hour}
              onChange={setHour}
            />

          </div>

          <div className="mt-6">

            <button
              className="btn btn-primary"
              onClick={handlePredict}
              disabled={predictLoading}
            >
              {predictLoading
                ? "Predicting..."
                : "Predict"}
            </button>

          </div>

        </div>

      </div>

      {loading && <Loading />}

      {error && <Error message={error} />}

      {!loading && !predictLoading && (
        <PredictionResult
          data={prediction}
        />
      )}

    </div>
  );
}

export default HourlyForm;