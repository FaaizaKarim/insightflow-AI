import { NavLink } from "react-router-dom";
import { MessageSquare, LayoutDashboard, Zap, Database, FileText } from "lucide-react";

const navItems = [
  { to: "/chat",      icon: MessageSquare, label: "Chat Agent" },
  { to: "/dashboard", icon: LayoutDashboard, label: "Dashboard" },
];

export default function AppShell({ children }) {
  return (
    <div className="flex h-screen overflow-hidden bg-[#0A2342]">
      {/* Sidebar */}
      <aside className="w-60 flex-shrink-0 bg-[#0D2A4A] border-r border-[#1A3A6B] flex flex-col">
        {/* Logo */}
        <div className="px-5 py-5 border-b border-[#1A3A6B]">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-[#0E6BA8] flex items-center justify-center">
              <Zap size={16} className="text-white" />
            </div>
            <div>
              <div className="text-white font-semibold text-sm leading-tight">InsightFlow</div>
              <div className="text-[#6B9AB8] text-xs">AI</div>
            </div>
          </div>
        </div>

        {/* Nav */}
        <nav className="flex-1 px-3 py-4 space-y-1">
          {navItems.map(({ to, icon: Icon, label }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150 ${
                  isActive
                    ? "bg-[#0E6BA8]/20 text-white border border-[#0E6BA8]/30"
                    : "text-[#6B9AB8] hover:text-white hover:bg-[#1A3A6B]/60"
                }`
              }
            >
              <Icon size={16} />
              {label}
            </NavLink>
          ))}
        </nav>

        {/* Capability pills */}
        <div className="px-4 pb-5 space-y-2">
          <div className="text-[#6B9AB8] text-xs font-medium uppercase tracking-wider mb-2">Capabilities</div>
          {[
            { icon: Database, label: "SQL Engine" },
            { icon: Zap,      label: "ML Predictions" },
            { icon: FileText, label: "RAG Search" },
          ].map(({ icon: Icon, label }) => (
            <div key={label} className="flex items-center gap-2 text-xs text-[#6B9AB8]">
              <div className="w-1.5 h-1.5 rounded-full bg-[#0E6BA8]" />
              {label}
            </div>
          ))}
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 overflow-hidden flex flex-col">
        {children}
      </main>
    </div>
  );
}
