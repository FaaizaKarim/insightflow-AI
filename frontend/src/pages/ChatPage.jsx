import ChatWindow from "../components/chat/ChatWindow.jsx";
import ChatInput from "../components/chat/ChatInput.jsx";
import ToolBadges from "../components/chat/ToolBadges.jsx";
import useStore from "../store/useStore.js";
import { Trash2, Sparkles } from "lucide-react";

const SUGGESTIONS = [
  "Which customers are most likely to churn next month?",
  "Show me revenue by region for all time",
  "What is our refund policy for enterprise clients?",
  "Predict churn for customer ID 5 and summarize their history",
];

export default function ChatPage() {
  const { messages, isLoading, activeTools, clearChat } = useStore();

  return (
    <div className="flex flex-col h-full bg-[#0A2342]">
      {/* Header */}
      <div className="flex items-center justify-between px-6 py-4 border-b border-[#1A3A6B]">
        <div>
          <h1 className="text-white font-semibold text-base">Data Intelligence Agent</h1>
          <p className="text-[#6B9AB8] text-xs mt-0.5">SQL · ML Predictions · Document Search</p>
        </div>
        <div className="flex items-center gap-3">
          <ToolBadges tools={activeTools} />
          {messages.length > 0 && (
            <button
              onClick={clearChat}
              className="flex items-center gap-1.5 text-xs text-[#6B9AB8] hover:text-white transition-colors px-3 py-1.5 rounded-lg hover:bg-[#1A3A6B]"
            >
              <Trash2 size={13} />
              Clear
            </button>
          )}
        </div>
      </div>

      {/* Chat area */}
      <div className="flex-1 overflow-hidden flex flex-col">
        {messages.length === 0 ? (
          <EmptyState />
        ) : (
          <ChatWindow />
        )}
      </div>

      {/* Suggestions when empty */}
      {messages.length === 0 && (
        <div className="px-6 pb-4 grid grid-cols-2 gap-2">
          {SUGGESTIONS.map((s) => (
            <SuggestionChip key={s} text={s} />
          ))}
        </div>
      )}

      {/* Input */}
      <div className="px-6 pb-6 pt-3">
        <ChatInput disabled={isLoading} />
      </div>
    </div>
  );
}

function EmptyState() {
  return (
    <div className="flex-1 flex flex-col items-center justify-center px-6 text-center">
      <div className="w-14 h-14 rounded-2xl bg-[#0E6BA8]/20 border border-[#0E6BA8]/30 flex items-center justify-center mb-4">
        <Sparkles size={24} className="text-[#0E6BA8]" />
      </div>
      <h2 className="text-white font-semibold text-xl mb-2">Ask anything about your data</h2>
      <p className="text-[#6B9AB8] text-sm max-w-sm">
        I can query your database, run ML predictions, and search company documents — all from one question.
      </p>
    </div>
  );
}

function SuggestionChip({ text }) {
  const { sendMessage } = useStore();
  return (
    <button
      onClick={() => sendMessage(text)}
      className="text-left text-xs text-[#B8D4E3] bg-[#1A3A6B]/40 hover:bg-[#1A3A6B] border border-[#1A3A6B] hover:border-[#0E6BA8]/50 rounded-lg px-3 py-2.5 transition-all duration-150 leading-relaxed"
    >
      {text}
    </button>
  );
}
