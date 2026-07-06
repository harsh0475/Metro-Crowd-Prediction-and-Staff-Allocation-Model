import { useEffect, useState } from "react";

import {
  getLines,
  getHourlyPrediction,
} from "../services/dashboardService";

import {
  getCurrentDate,
  getCurrentHour,
} from "../utils/date";

import { DEFAULT_LINE } from "../utils/constants";

const useDashboard = () => {
  const [lines, setLines] = useState([]);

  const [selectedLine, setSelectedLine] = useState(DEFAULT_LINE);

  const [prediction, setPrediction] = useState([]);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");

  const loadPrediction = async (line) => {
    try {
      setLoading(true);

      const response = await getHourlyPrediction({
        line,
        date: getCurrentDate(),
        hour: getCurrentHour(),
      });

      setPrediction(response.results || []);
    } catch (err) {
      setError("Unable to load prediction.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const initialize = async () => {
      try {
        const fetchedLines = await getLines();

        setLines(fetchedLines);

        if (fetchedLines.includes(DEFAULT_LINE)) {
          await loadPrediction(DEFAULT_LINE);
        } else if (fetchedLines.length > 0) {
          setSelectedLine(fetchedLines[0]);
          await loadPrediction(fetchedLines[0]);
        }
      } catch {
        setError("Unable to connect to backend.");
        setLoading(false);
      }
    };

    initialize();
  }, []);

  const changeLine = async (line) => {
    setSelectedLine(line);
    await loadPrediction(line);
  };

  return {
    lines,
    selectedLine,
    prediction,
    loading,
    error,
    changeLine,
  };
};

export default useDashboard;