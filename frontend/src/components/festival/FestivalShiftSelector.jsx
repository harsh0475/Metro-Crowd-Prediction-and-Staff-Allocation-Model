function FestivalShiftSelector({ selectedShift, onChange }) {
  return (
    <div className="form-control w-full">
      <label className="label">
        <span className="label-text font-medium">Shift</span>
      </label>

      <select
        className="select select-bordered w-full"
        value={selectedShift}
        onChange={(e) => onChange(e.target.value)}
      >
        <option value="Morning">Morning</option>
        <option value="Evening">Evening</option>
        <option value="Night">Night</option>
      </select>
    </div>
  );
}

export default FestivalShiftSelector;