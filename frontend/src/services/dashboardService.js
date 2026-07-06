import api from "./api";

export const getLines = async () => {
  const response = await api.get("/lines");
  return response.data.lines;
};

export const getHourlyPrediction = async (payload) => {
  const response = await api.post("/predict-hour", payload);
  return response.data;
};