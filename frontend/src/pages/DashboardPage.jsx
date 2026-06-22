import { useEffect } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts";
import useStore from "../store/useStore.js";
import { Users, TrendingUp, AlertTriangle, Database, RefreshCw } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

const CHART_COLORS = ["#0E6BA8", "#1A3A6B", "#6B9AB8", "#B8D4E3", "#0A2342"];

const KPI_CARDS = [
  { label: "Total Customers",     value: "100",   sub: "Sample dataset", icon: Users,         color: "text-[#0E6BA8]", bg: "bg-[#0E6BA8]/10" },
  { label: "Churn Rate",          value: "25%",   sub: "Model target",   icon: AlertTriangle, color: "text-amber-400", bg: "bg-amber-400/10" },
  { label: "Avg Contract Value",  value: "$6.2k", sub: "Across segments", icon: TrendingUp,   color: "text-emerald-400", bg: "bg-emerald-400/10" },
  { label: "DB Tables Active",    value: "3",     sub: "Live PostgreSQL", icon: Database,      color: "text-purple-400", bg: "bg-purple-400/10" },
];

const SAMPLE_REVENUE = [
  { region: "North America", revenue: 142000 },
  { region: "Europe",        revenue: 98000 },
  { region: "APAC",          revenue: 76000 },
  { region: "LATAM",         revenue: 41000 },
  { region: "Middle East",   revenue: 28000 },
];

const SAMPLE_SEGMENTS = [
  { name: "Enterprise",  value: 35 },
  { name: "Mid-Market",  value: 40 },
  { name: "SMB",         value: 25 },
];

export default function DashboardPage() {
  const { loadDashboard, dashboardData, dashboardLoading } = useStore();

  useEffect(() => { loadDashboard(); }, []);

  return (
    <div className="flex-1 overflow-y-auto px-6 py-5 space-y-5 bg-[#0A2342]">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-white font-semibold text-lg">Business Overview</h1>
          <p className="text-[#6B9AB8] text-xs mt-0.5">Live data from PostgreSQL · Refreshed on load</p>
        </div>
        <button
          onClick={loadDashboard}
          className="flex items-center gap-1.5 text-xs text-[#6B9AB8] hover:text-white transition-colors px-3 py-1.5 rounded-lg border border-[#1A3A6B] hover:border-[#0E6BA8]/50"
        >
          <RefreshCw size={12} className={dashboardLoading ? "animate-spin" : ""} />
          Refresh
        </button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-4 gap-3">
        {KPI_CARDS.map(({ label, value, sub, icon: Icon, color, bg }) => (
          <div key={label} className="bg-[#0D2A4A] border border-[#1A3A6B] rounded-xl p-4">
            <div className="flex items-start justify-between mb-3">
              <div className={`w-8 h-8 rounded-lg ${bg} flex items-center justify-center`}>
                <Icon size={15} className={color} />
              </div>
            </div>
            <div className="text-white font-bold text-2xl">{value}</div>
            <div className="text-white/70 text-xs font-medium mt-0.5">{label}</div>
            <div className="text-[#6B9AB8] text-xs mt-1">{sub}</div>
          </div>
        ))}
      </div>

      {/* Charts row */}
      <div className="grid grid-cols-3 gap-4">
        {/* Revenue by Region */}
        <div className="col-span-2 bg-[#0D2A4A] border border-[#1A3A6B] rounded-xl p-4">
          <div className="text-white font-medium text-sm mb-1">Revenue by Region</div>
          <div className="text-[#6B9AB8] text-xs mb-4">Sample data · USD</div>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={SAMPLE_REVENUE} barSize={24}>
              <XAxis dataKey="region" tick={{ fill: "#6B9AB8", fontSize: 11 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill: "#6B9AB8", fontSize: 11 }} axisLine={false} tickLine={false} tickFormatter={(v) => `$${(v/1000).toFixed(0)}k`} />
              <Tooltip
                contentStyle={{ background: "#1A3A6B", border: "1px solid #0E6BA8", borderRadius: 8, color: "#fff", fontSize: 12 }}
                formatter={(v) => [`$${v.toLocaleString()}`, "Revenue"]}
              />
              <Bar dataKey="revenue" fill="#0E6BA8" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Customer Segments */}
        <div className="bg-[#0D2A4A] border border-[#1A3A6B] rounded-xl p-4">
          <div className="text-white font-medium text-sm mb-1">Customer Segments</div>
          <div className="text-[#6B9AB8] text-xs mb-4">Distribution</div>
          <ResponsiveContainer width="100%" height={150}>
            <PieChart>
              <Pie data={SAMPLE_SEGMENTS} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={60} strokeWidth={0}>
                {SAMPLE_SEGMENTS.map((_, i) => (
                  <Cell key={i} fill={CHART_COLORS[i % CHART_COLORS.length]} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{ background: "#1A3A6B", border: "1px solid #0E6BA8", borderRadius: 8, color: "#fff", fontSize: 12 }}
              />
            </PieChart>
          </ResponsiveContainer>
          <div className="space-y-1 mt-2">
            {SAMPLE_SEGMENTS.map(({ name, value }, i) => (
              <div key={name} className="flex items-center justify-between text-xs">
                <div className="flex items-center gap-1.5">
                  <div className="w-2 h-2 rounded-full" style={{ background: CHART_COLORS[i] }} />
                  <span className="text-[#6B9AB8]">{name}</span>
                </div>
                <span className="text-white font-medium">{value}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Live DB Query Result */}
      {dashboardData?.customers && (
        <div className="bg-[#0D2A4A] border border-[#1A3A6B] rounded-xl p-4">
          <div className="text-white font-medium text-sm mb-1">Live Database Query</div>
          <div className="text-[#6B9AB8] text-xs mb-4">Top customers by contract value · Real-time from PostgreSQL</div>
          <div className="prose prose-invert max-w-none text-sm">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{dashboardData.customers}</ReactMarkdown>
          </div>
        </div>
      )}

      {/* Architecture info cards */}
      <div className="grid grid-cols-3 gap-4">
        {[
          { title: "Text-to-SQL Engine", desc: "Converts natural language to validated PostgreSQL queries. Schema-injected, SELECT-only, table-whitelisted.", color: "border-emerald-500/30 bg-emerald-500/5" },
          { title: "ML Churn Model", desc: "Gradient Boosting classifier trained on customer behavioral features. Served as both agent tool and REST API.", color: "border-purple-500/30 bg-purple-500/5" },
          { title: "RAG Search", desc: "ChromaDB vector store with OpenAI embeddings. Semantic search over uploaded policy documents and FAQs.", color: "border-amber-500/30 bg-amber-500/5" },
        ].map(({ title, desc, color }) => (
          <div key={title} className={`rounded-xl p-4 border ${color}`}>
            <div className="text-white font-medium text-sm mb-2">{title}</div>
            <p className="text-[#6B9AB8] text-xs leading-relaxed">{desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
