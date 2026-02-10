import { NavLink } from "react-router";

const navItems = [
  { to: "/", label: "首页" },
  { to: "/record", label: "记录" },
  { to: "/recommend", label: "推荐" },
  { to: "/profile", label: "档案" },
];

function BottomNav() {
  return (
    <nav className="fixed right-0 bottom-0 left-0 border-t border-slate-200/90 bg-white/95 px-3 py-2 backdrop-blur">
      <div className="mx-auto grid w-full max-w-5xl grid-cols-4 gap-2">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.to === "/"}
            className={({ isActive }) =>
              [
                "rounded-lg px-2 py-2 text-center text-sm font-semibold transition-colors",
                isActive
                  ? "bg-teal-100 text-teal-800"
                  : "text-slate-600 hover:bg-slate-100 hover:text-slate-900",
              ].join(" ")
            }
          >
            {item.label}
          </NavLink>
        ))}
      </div>
    </nav>
  );
}

export default BottomNav;

