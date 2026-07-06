function PredictionTable({ data = [] }) {
  if (!Array.isArray(data) || data.length === 0) {
    return (
      <div className="rounded-lg border border-base-300 bg-base-100 p-8 text-center">
        <p className="text-sm text-base-content/50">No prediction data available.</p>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto rounded-lg border border-base-300 bg-base-100">
      <table className="table table-zebra">
        <thead>
          <tr className="text-xs uppercase tracking-wide text-base-content/50">
            <th>Station</th>
            <th>Counter</th>
            <th>Passengers</th>
            <th>Available Staff</th>
            <th>Required Staff</th>
            <th>Staff Gap</th>
            <th>Status</th>
          </tr>
        </thead>

        <tbody>
          {data.map((station) =>
            (station.booking_counters || []).map((counter, index) => {
              const staffGap =
                (counter.available_staff || 0) - (counter.required_staff || 0);

              let badgeClass = "badge-warning";

              if (counter.status === "Sufficient") {
                badgeClass = "badge-success";
              } else if (counter.status === "Shortage") {
                badgeClass = "badge-error";
              } else if (counter.status === "Not Manned") {
                badgeClass = "badge-ghost";
              }

              return (
                <tr key={`${station.station}-${counter.booking_counter}-${index}`}>
                  <td>{index === 0 ? station.station_name : ""}</td>
                  <td>{counter.booking_counter}</td>
                  <td>{counter.predicted_passengers}</td>
                  <td>{counter.available_staff}</td>
                  <td>{counter.required_staff}</td>
                  <td>
                    <span
                      className={
                        staffGap >= 0
                          ? "text-success font-semibold"
                          : "text-error font-semibold"
                      }
                    >
                      {staffGap}
                    </span>
                  </td>
                  <td>
                    <span className={`badge ${badgeClass}`}>
                      {counter.status}
                    </span>
                  </td>
                </tr>
              );
            })
          )}
        </tbody>
      </table>
    </div>
  );
}

export default PredictionTable;