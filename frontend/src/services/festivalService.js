import api from "./api";

export const getFestivals = async () => {
  const response = await api.get("/festivals");
  return response.data.festivals;
};

export const predictFestivalHourly = async (payload) => {
  const response = await api.post("/festival/predict-hour", payload);
  return response.data;
};

export const predictFestivalShift = async (payload) => {
  const response = await api.post("/festival/predict-shift", payload);
  return response.data;
};