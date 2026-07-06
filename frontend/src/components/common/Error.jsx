function Error({ message }) {
  return (
    <div className="rounded-md border border-error/30 bg-error/10 px-4 py-3 text-sm text-error">
      {message}
    </div>
  );
}

export default Error;
