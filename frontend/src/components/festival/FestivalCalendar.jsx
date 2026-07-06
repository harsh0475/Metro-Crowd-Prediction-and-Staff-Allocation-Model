import { useState } from "react";

import { FESTIVAL_YEARS, getFestivalCalendar } from "../../utils/festivalCalendarData";

function FestivalCalendar() {
  const [year, setYear] = useState("All");

  const events = getFestivalCalendar().filter(
    (event) => year === "All" || event.year === Number(year)
  );

  return (
    <div className="card border border-base-300 bg-base-100">
      <div className="card-body">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 className="card-title">Festival Calendar</h2>
            <p className="mt-1 text-sm text-base-content/50">
              Reference dates for Durga Puja, Christmas and New Year (2023 - 2027).
            </p>
          </div>

          <div className="w-full sm:w-48">
            <label className="label">
              <span className="label-text">Year</span>
            </label>

            <select
              className="select select-bordered w-full"
              value={year}
              onChange={(e) => setYear(e.target.value)}
            >
              <option value="All">All Years</option>
              {FESTIVAL_YEARS.map((y) => (
                <option key={y} value={y}>
                  {y}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="mt-4 overflow-x-auto rounded-lg border border-base-300">
          <table className="table table-zebra">
            <thead>
              <tr className="text-xs uppercase tracking-wide text-base-content/50">
                <th>Year</th>
                <th>Festival</th>
                <th>Period</th>
                <th>Start Date</th>
                <th>End Date</th>
              </tr>
            </thead>

            <tbody>
              {events.map((event) => (
                <tr key={`${event.year}-${event.festival}`}>
                  <td>{event.year}</td>
                  <td>{event.festival}</td>
                  <td>{event.label}</td>
                  <td>{event.startLabel}</td>
                  <td>{event.endLabel}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default FestivalCalendar;
