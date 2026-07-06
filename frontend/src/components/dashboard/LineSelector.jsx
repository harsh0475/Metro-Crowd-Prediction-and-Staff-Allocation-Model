function LineSelector({
  lines,
  selectedLine,
  onChange,
}) {
  return (
    <div>

      <label className="label">

        <span className="label-text">
          Metro Line
        </span>

      </label>

      <select
        className="select select-bordered w-full"
        value={selectedLine}
        onChange={(e) =>
          onChange(e.target.value)
        }
      >
        {lines.map((line) => (
          <option
            key={line}
            value={line}
          >
            {line}
          </option>
        ))}
      </select>

    </div>
  );
}

export default LineSelector;