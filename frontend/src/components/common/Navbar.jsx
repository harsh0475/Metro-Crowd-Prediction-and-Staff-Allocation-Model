import { useState } from "react";
import { NavLink } from "react-router-dom";

function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false);

  const linkClass = ({ isActive }) =>
    `border-b-2 px-1 py-4 text-sm font-medium transition-colors ${
      isActive
        ? "border-primary text-primary"
        : "border-transparent text-base-content/60 hover:text-base-content"
    }`;

  const mobileLinkClass = ({ isActive }) =>
    `block rounded-md px-3 py-2 text-sm font-medium transition-colors ${
      isActive
        ? "bg-primary/10 text-primary"
        : "text-base-content/70 hover:bg-base-200 hover:text-base-content"
    }`;

  return (
    <header className="border-b border-base-300 bg-base-100">
      <div className="mx-auto flex w-full max-w-7xl items-center justify-between px-4">
        <NavLink
          to="/"
          className="flex items-center gap-2 py-4"
          onClick={() => setMenuOpen(false)}
        >
          <span className="text-sm font-semibold tracking-tight text-base-content sm:text-base">
            Metro Crowd Prediction &amp; Staff Allocation
          </span>
        </NavLink>

        {/* Desktop nav */}
        <nav className="hidden gap-6 md:flex">
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

        {/* Mobile menu toggle */}
        <button
          type="button"
          className="btn btn-square btn-ghost md:hidden"
          aria-label="Toggle navigation menu"
          aria-expanded={menuOpen}
          onClick={() => setMenuOpen((open) => !open)}
        >
          {menuOpen ? (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          ) : (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          )}
        </button>
      </div>

      {/* Mobile nav panel */}
      {menuOpen && (
        <nav className="border-t border-base-300 bg-base-100 px-4 py-3 md:hidden">
          <div className="flex flex-col gap-1">
            <NavLink to="/" end className={mobileLinkClass} onClick={() => setMenuOpen(false)}>
              Dashboard
            </NavLink>

            <NavLink to="/prediction" className={mobileLinkClass} onClick={() => setMenuOpen(false)}>
              Prediction
            </NavLink>

            <NavLink
              to="/festival-prediction"
              className={mobileLinkClass}
              onClick={() => setMenuOpen(false)}
            >
              Festival Prediction
            </NavLink>
          </div>
        </nav>
      )}
    </header>
  );
}

export default Navbar;