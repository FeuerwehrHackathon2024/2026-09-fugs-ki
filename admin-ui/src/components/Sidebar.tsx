import { NavLink } from "react-router-dom";
import { cn } from "@/lib/utils";

const modules = [
  {
    path: "/knowledge-hub",
    label: "Knowledge Hub",
    icon: (
      <svg
        width="18"
        height="18"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
        aria-hidden="true"
      >
        <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
        <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
      </svg>
    ),
  },
  {
    path: "/system-prompt",
    label: "System Prompt",
    icon: (
      <svg
        width="18"
        height="18"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.8"
        strokeLinecap="round"
        strokeLinejoin="round"
        aria-hidden="true"
      >
        <path d="M12 20h9" />
        <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" />
      </svg>
    ),
  },
];

export function Sidebar() {
  return (
    <aside className="flex h-screen w-56 flex-shrink-0 flex-col bg-[var(--color-sidebar)]">
      <div className="flex items-center gap-2.5 px-5 py-5">
        <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-[var(--color-accent)]">
          <svg
            width="14"
            height="14"
            viewBox="0 0 24 24"
            fill="none"
            stroke="white"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            aria-hidden="true"
          >
            <rect x="3" y="3" width="7" height="7" />
            <rect x="14" y="3" width="7" height="7" />
            <rect x="14" y="14" width="7" height="7" />
            <rect x="3" y="14" width="7" height="7" />
          </svg>
        </div>
        <span className="text-sm font-semibold tracking-wide text-[var(--color-sidebar-text)]">
          Admin UI
        </span>
      </div>

      <div className="px-3 pb-2">
        <p className="px-2 text-[10px] font-medium uppercase tracking-widest text-[var(--color-sidebar-muted)]">
          Module
        </p>
      </div>

      <nav className="flex-1 px-3">
        {modules.map((mod) => (
          <NavLink
            key={mod.path}
            to={mod.path}
            className={({ isActive }) =>
              cn(
                "flex items-center gap-2.5 rounded-lg px-3 py-2.5 text-sm transition-colors",
                isActive
                  ? "bg-[var(--color-sidebar-active-bg)] text-[var(--color-sidebar-active)] font-medium"
                  : "text-[var(--color-sidebar-text)] hover:bg-white/5",
              )
            }
          >
            {mod.icon}
            {mod.label}
          </NavLink>
        ))}
      </nav>

      <div className="px-5 py-4">
        <p className="text-[10px] text-[var(--color-sidebar-muted)]">fugs-ki · Admin</p>
      </div>
    </aside>
  );
}
