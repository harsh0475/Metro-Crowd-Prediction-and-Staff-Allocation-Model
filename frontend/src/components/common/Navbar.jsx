import { NavLink } from "react-router-dom";

function Navbar() {
  const linkClass = ({ isActive }) =>
    `border-b-2 px-1 py-4 text-sm font-medium transition-colors ${
      isActive
        ? "border-primary text-primary"
        : "border-transparent text-base-content/60 hover:text-base-content"
    }`;

  return (
    <header className="border-b border-base-300 bg-base-100">
      <div className="mx-auto flex w-full max-w-7xl items-center justify-between px-4">
        <NavLink to="/" className="flex items-center gap-2 py-4">
          <span className="text-base font-semibold tracking-tight text-base-content">
            Metro Crowd Prediction &amp; Staff Allocation
          </span>
        </NavLink>

        <nav className="flex gap-6">
          <NavLink to="/" end className={linkClass}>
            Dashboard
          </NavLink>

          <NavLink to="/prediction" className={linkClass}>
            Prediction
          </NavLink>

          <NavLink to="/festival-prediction" className={linkClass}>
            Festival Prediction
          </NavLink>
        </nav>
      </div>
    </header>
  );
}

export default Navbar;
