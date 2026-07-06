import { useState } from "react";

import useFestivalPrediction from "../../hooks/useFestivalPrediction";

import LineSelector from "../dashboard/LineSelector";
import HourSelector from "../prediction/HourSelector";
import FestivalSelector from "./FestivalSelector";

import FestivalPredictionResult from "./FestivalPredictionResult";

import Loading from "../common/Loading";
import Error from "../common/Error";

import { predictFestivalHourly } from "../../services/festivalService";

import { getCurrentDate, getCurrentHour } from "../../utils/date";

function FestivalHourlyForm() {
  const {
    lines,
    selectedLine,
    setSelectedLine,
    festivals,
    selectedFestival,
    setSelectedFestival,
    loading,
  } = useFestivalPrediction();

  const [date, setDate] = useState(getCurrentDate());
  const [hour, setHour] = useState(getCurrentHour());

  const [prediction, setPrediction] = useState([]);
  const [predictLoading, setPredictLoading] = useState(false);
  const [error, setError] = useState("");

  const handlePredict = async () => {
    if (!date) {
      setError("Please select a date.");
      return;
    }

    try {
      setPredictLoading(true);
      setError("");

      const response = await predictFestivalHourly({
        line: selectedLine,
        date,
        hour,
        festival_name: selectedFestival,
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
          <h2 className="card-title">Festival Hourly Prediction</h2>

          <div className="grid gap-5 md:grid-cols-4">
            <LineSelector
              lines={lines}
              selectedLine={selectedLine}
              onChange={setSelectedLine}
            />

            <FestivalSelector
              festivals={festivals}
              selectedFestival={selectedFestival}
              onChange={setSelectedFestival}
            />

            <div>
              <label className="label">
                <span className="label-text">Date</span>
              </label>

              <input
                type="date"
                className="input input-bordered w-full"
                value={date}
                onChange={(e) => setDate(e.target.value)}
              />
            </div>

            <HourSelector selectedHour={hour} onChange={setHour} />
          </div>

          <div className="mt-6">
            <button
              className="btn btn-primary"
              onClick={handlePredict}
              disabled={predictLoading}
            >
              {predictLoading ? "Predicting..." : "Predict"}
            </button>
          </div>
        </div>
      </div>

      {loading && <Loading />}
      {error && <Error message={error} />}

      {!loading && !predictLoading && (
        <FestivalPredictionResult data={prediction} />
      )}
    </div>
  );
}

export default FestivalHourlyForm;