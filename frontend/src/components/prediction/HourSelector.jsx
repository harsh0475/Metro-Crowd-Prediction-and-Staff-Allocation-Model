function HourSelector({
  selectedHour,
  onChange,
}) {
  const hours = Array.from(
    { length: 17 },
    (_, index) => index + 6
  );

  return (
    <div className="form-control w-full">

      <label className="label">
        <span className="label-text font-medium">
          Hour
        </span>
      </label>

      <select
        className="select select-bordered w-full"
        value={selectedHour}
        onChange={(e) =>
          onChange(Number(e.target.value))
        }
      >
        {hours.map((hour) => (
          <option
            key={hour}
            value={hour}
          >
            {hour}:00
          </option>
        ))}
      </select>

    </div>
  );
}

export default HourSelector;