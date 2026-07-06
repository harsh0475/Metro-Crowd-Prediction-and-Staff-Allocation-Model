// Reference festival calendar (2023 - 2027).
// Durga Puja dates (Mahalaya - Dashami) mirror backend/data/raw/festival_calendar.csv.
// Christmas & New Year are fixed calendar dates observed every year.

const formatDate = (isoDate) =>
  new Date(`${isoDate}T00:00:00`).toLocaleDateString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });

const DURGA_PUJA_DATES = {
  2023: { start: "2023-10-14", end: "2023-10-24" },
  2024: { start: "2024-10-02", end: "2024-10-13" },
  2025: { start: "2025-09-21", end: "2025-10-02" },
  2026: { start: "2026-10-08", end: "2026-10-18" },
  2027: { start: "2027-09-28", end: "2027-10-08" },
};

export const FESTIVAL_YEARS = [2023, 2024, 2025, 2026, 2027];

export const getFestivalCalendar = () => {
  const events = [];

  FESTIVAL_YEARS.forEach((year) => {
    const durgaPuja = DURGA_PUJA_DATES[year];

    events.push({
      year,
      festival: "Durga Puja",
      label: "Mahalaya - Dashami",
      startDate: durgaPuja.start,
      endDate: durgaPuja.end,
      startLabel: formatDate(durgaPuja.start),
      endLabel: formatDate(durgaPuja.end),
    });

    // events.push({
    //   year,
    //   festival: "Christmas & New Year",
    //   label: "Christmas - New Year",
    //   startDate: `${year}-12-25`,
    //   endDate: `${year + 1}-01-01`,
    //   startLabel: formatDate(`${year}-12-25`),
    //   endLabel: formatDate(`${year + 1}-01-01`),
    // });
  });

  return events;
};
