const TOOL_META = {
  sql_query_tool:  { label: "SQL Engine",      color: "text-emerald-400 bg-emerald-400/10 border-emerald-400/20" },
  ml_predict_tool: { label: "ML Prediction",   color: "text-purple-400 bg-purple-400/10 border-purple-400/20" },
  rag_search_tool: { label: "Document Search", color: "text-amber-400 bg-amber-400/10 border-amber-400/20" },
};

export default function ToolBadges({ tools = [] }) {
  if (!tools.length) return null;
  return (
    <div className="flex gap-1.5 items-center">
      <span className="text-[#6B9AB8] text-xs">Used:</span>
      {[...new Set(tools)].map((tool) => {
        const meta = TOOL_META[tool] || { label: tool, color: "text-blue-400 bg-blue-400/10 border-blue-400/20" };
        return (
          <span key={tool} className={`text-xs px-2 py-0.5 rounded-full border font-mono ${meta.color}`}>
            {meta.label}
          </span>
        );
      })}
    </div>
  );
}
