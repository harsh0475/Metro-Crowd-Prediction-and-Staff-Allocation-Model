function PredictionResult({ data = [] }) {
  if (!Array.isArray(data) || data.length === 0) {
    return (
      <div className="card border border-base-300 bg-base-100">
        <div className="card-body text-center">
          <h2 className="text-lg font-semibold">
            No Prediction Available
          </h2>

          <p className="text-base-content/50">
            Click Predict to view results.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="card border border-base-300 bg-base-100">
      <div className="card-body">
        <h2 className="card-title mb-4">
          Prediction Result
        </h2>

        <div className="overflow-x-auto">
          <table className="table table-zebra">
            <thead>
              <tr>
                <th>Station</th>
                <th>Counter</th>
                <th>Passengers</th>
                <th>Available</th>
                <th>Required</th>
                <th>Gap</th>
                <th>Status</th>
              </tr>
            </thead>

            <tbody>
              {data.map((station) =>
                station.booking_counters.map((counter, index) => (
                  <tr key={`${station.station}-${counter.booking_counter}`}>
                    <td>
                      {index === 0 ? station.station_name : ""}
                    </td>
                    <td>{counter.booking_counter}</td>
                    <td>{counter.predicted_passengers}</td>
                    <td>{counter.available_staff}</td>
                    <td>{counter.required_staff}</td>
                    <td>
                      <span
                        className={
                          counter.staff_gap >= 0
                            ? "text-success font-semibold"
                            : "text-error font-semibold"
                        }
                      >
                        {counter.staff_gap}
                      </span>
                    </td>
                    <td>
                      <span
                        className={`badge ${
                          counter.status === "Need Staff"
                            ? "badge-error"
                            : counter.status === "Balanced"
                            ? "badge-warning"
                            : "badge-success"
                        }`}
                      >
                        {counter.status}
                      </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default PredictionResult;