export const getCurrentDate = () => {
  return new Date().toISOString().split("T")[0];
};

export const getCurrentHour = () => {
  const hour = new Date().getHours();

  // Metro operates between 6 AM and 10 PM
  if (hour < 6) return 6;
  if (hour > 22) return 22;

  return hour;
};

export const getCurrentShift = () => {
  const hour = new Date().getHours();

  return hour < 14 ? "Morning" : "Evening";
};

export const getCurrentTime = () => {
  return new Date().toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });
};