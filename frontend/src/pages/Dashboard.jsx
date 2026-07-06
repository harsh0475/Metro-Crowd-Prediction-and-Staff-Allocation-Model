import LineSelector from "../components/dashboard/LineSelector";
import PredictionTable from "../components/dashboard/PredictionTable";
import SummaryCard from "../components/dashboard/SummaryCard";

import Loading from "../components/common/Loading";
import Error from "../components/common/Error";

import useDashboard from "../hooks/useDashboard";

import { getCurrentTime } from "../utils/date";

function Dashboard() {
  const {
    lines,
    selectedLine,
    prediction,
    loading,
    error,
    changeLine,
  } = useDashboard();

  const totalPassengers = prediction.reduce((sum, station) => {
    return (
      sum +
      (station.booking_counters || []).reduce(
        (s, counter) => s + (counter.predicted_passengers || 0),
        0
      )
    );
  }, 0);

  const totalAvailableStaff = prediction.reduce((sum, station) => {
    return (
      sum +
      (station.booking_counters || []).reduce(
        (s, counter) => s + (counter.available_staff || 0),
        0
      )
    );
  }, 0);

  const totalRequiredStaff = prediction.reduce((sum, station) => {
    return (
      sum +
      (station.booking_counters || []).reduce(
        (s, counter) => s + (counter.required_staff || 0),
        0
      )
    );
  }, 0);

  const totalGap = totalAvailableStaff - totalRequiredStaff;

  return (
    <div className="space-y-6">

      <div className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">

        <div>
          <h1 className="page-title">Live Crowd Prediction</h1>

          <p className="page-subtitle">
            Current Time: {getCurrentTime()}
          </p>
        </div>

        {lines.length > 0 && (
          <LineSelector
            lines={lines}
            selectedLine={selectedLine}
            onChange={changeLine}
          />
        )}

      </div>

      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 xl:grid-cols-4">

        <SummaryCard
          title="Total Passengers"
          value={totalPassengers}
        />

        <SummaryCard
          title="Available Staff"
          value={totalAvailableStaff}
          color="text-success"
        />

        <SummaryCard
          title="Required Staff"
          value={totalRequiredStaff}
          color="text-warning"
        />

        <SummaryCard
          title="Staff Gap"
          value={totalGap}
          color={totalGap >= 0 ? "text-success" : "text-error"}
        />

      </div>

      {loading && <Loading />}

      {!loading && error && (
        <Error message={error} />
      )}

      {!loading && !error && (
        <PredictionTable
          data={prediction}
        />
      )}

    </div>
  );
}

export default Dashboard;