import api from "./api";

export const predictHourly = async (payload) => {
  const response = await api.post("/predict-hour", payload);
  return response.data;
};

export const predictShift = async (payload) => {
  const response = await api.post("/predict-shift", payload);
  return response.data;
};