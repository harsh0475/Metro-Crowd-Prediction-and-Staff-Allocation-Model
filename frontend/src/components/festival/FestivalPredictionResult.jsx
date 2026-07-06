function FestivalPredictionResult({ data = [] }) {
  if (!Array.isArray(data) || data.length === 0) {
    return (
      <div className="card border border-base-300 bg-base-100">
        <div className="card-body text-center">
          <h2 className="text-lg font-semibold">
            No Prediction Available
          </h2>

          <p className="text-gray-500">
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
          Festival Prediction Result
        </h2>

        <div className="overflow-x-auto">
          <table className="table table-zebra">
            <thead>
              <tr>
                <th>Station</th>
                <th>Predicted Passengers</th>
                <th>Required Staff</th>
              </tr>
            </thead>

            <tbody>
              {data.map((station) => (
                <tr key={station.station}>
                  <td>{station.station_name}</td>
                  <td>{station.predicted_passengers}</td>
                  <td>
                    <span className="badge badge-primary">
                      {station.required_staff}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default FestivalPredictionResult;