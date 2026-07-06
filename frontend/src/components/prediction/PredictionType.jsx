function PredictionType({ predictionType, setPredictionType }) {
  return (
    <div className="card border border-base-300 bg-base-100">

      <div className="card-body">

        <h2 className="card-title">
          Prediction Type
        </h2>

        <div className="flex gap-8 mt-2">

          <label className="label cursor-pointer gap-2">

            <input
              type="radio"
              className="radio radio-primary"
              checked={predictionType === "hour"}
              onChange={() =>
                setPredictionType("hour")
              }
            />

            <span>Hourly</span>

          </label>

          <label className="label cursor-pointer gap-2">

            <input
              type="radio"
              className="radio radio-primary"
              checked={predictionType === "shift"}
              onChange={() =>
                setPredictionType("shift")
              }
            />

            <span>Shift</span>

          </label>

        </div>

      </div>

    </div>
  );
}

export default PredictionType;