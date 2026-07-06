import { useEffect, useState } from "react";

import { getLines } from "../services/dashboardService";

const usePrediction = () => {
  const [lines, setLines] = useState([]);

  const [selectedLine, setSelectedLine] = useState("");

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  useEffect(() => {
    loadLines();
  }, []);

  const loadLines = async () => {
    try {
      setLoading(true);

      const response = await getLines();

      setLines(response);

      if (response.length > 0) {
        setSelectedLine(response[0]);
      }
    } catch (err) {
      console.error(err);
      setError("Unable to load metro lines.");
    } finally {
      setLoading(false);
    }
  };

  return {
    lines,
    selectedLine,
    setSelectedLine,

    loading,
    error,
  };
};

export default usePrediction;