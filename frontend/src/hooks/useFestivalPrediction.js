import { useEffect, useState } from "react";

import { getLines } from "../services/dashboardService";
import { getFestivals } from "../services/festivalService";

const useFestivalPrediction = () => {
  const [lines, setLines] = useState([]);
  const [selectedLine, setSelectedLine] = useState("");

  const [festivals, setFestivals] = useState([]);
  const [selectedFestival, setSelectedFestival] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    setLoading(true);
    setError("");

    let hadError = false;

    try {
      const linesResponse = await getLines();

      setLines(linesResponse);

      if (linesResponse.length > 0) {
        setSelectedLine(linesResponse[0]);
      }
    } catch (err) {
      console.error("Failed to load lines:", err);
      hadError = true;
    }

    try {
      const festivalsResponse = await getFestivals();

      setFestivals(festivalsResponse);

      if (festivalsResponse.length > 0) {
        setSelectedFestival(festivalsResponse[0]);
      }
    } catch (err) {
      console.error("Failed to load festivals:", err);
      hadError = true;
    }

    if (hadError) {
      setError("Unable to load some festival prediction options. Check console for details.");
    }

    setLoading(false);
  };

  return {
    lines,
    selectedLine,
    setSelectedLine,

    festivals,
    selectedFestival,
    setSelectedFestival,

    loading,
    error,
  };
};

export default useFestivalPrediction;