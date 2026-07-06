function FestivalSelector({ festivals, selectedFestival, onChange }) {
  return (
    <div>
      <label className="label">
        <span className="label-text">Festival</span>
      </label>

      <select
        className="select select-bordered w-full"
        value={selectedFestival}
        onChange={(e) => onChange(e.target.value)}
      >
        {festivals.map((festival) => (
          <option key={festival} value={festival}>
            {festival.replace(/_/g, " ")}
          </option>
        ))}
      </select>
    </div>
  );
}

export default FestivalSelector;