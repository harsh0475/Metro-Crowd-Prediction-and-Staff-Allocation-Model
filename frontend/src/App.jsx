import { BrowserRouter, Routes, Route } from "react-router-dom";

import Navbar from "./components/common/Navbar";

import Dashboard from "./pages/Dashboard";
import Prediction from "./pages/Prediction";
import FestivalPrediction from "./pages/FestivalPrediction";

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-base-200">
        <Navbar />

        <main className="mx-auto max-w-7xl p-4 sm:p-6">
          <Routes>
            <Route
              path="/"
              element={<Dashboard />}
            />

            <Route
              path="/prediction"
              element={<Prediction />}
            />

            <Route
              path="/festival-prediction"
              element={<FestivalPrediction />}
            />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;