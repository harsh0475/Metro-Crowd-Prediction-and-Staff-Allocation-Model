function SummaryCard({ title, value, color = "text-primary" }) {
  return (
    <div className="card border border-base-300 bg-base-100">
      <div className="card-body p-5">
        <h2 className="text-xs font-medium uppercase tracking-wide text-base-content/50">
          {title}
        </h2>

        <p className={`mt-1 text-2xl font-semibold ${color}`}>
          {value}
        </p>
      </div>
    </div>
  );
}

export default SummaryCard;
