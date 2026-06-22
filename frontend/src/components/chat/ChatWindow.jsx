import { useEffect, useRef } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import useStore from "../../store/useStore.js";
import { Bot, User } from "lucide-react";

export default function ChatWindow() {
  const { messages, isLoading } = useStore();
  const endRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  return (
    <div className="flex-1 overflow-y-auto px-6 py-4 space-y-5">
      {messages.map((msg) => (
        <MessageBubble key={msg.id} message={msg} />
      ))}
      {isLoading && <TypingIndicator />}
      <div ref={endRef} />
    </div>
  );
}

function MessageBubble({ message }) {
  const isUser = message.role === "user";

  return (
    <div className={`flex gap-3 animate-slide-up ${isUser ? "flex-row-reverse" : ""}`}>
      {/* Avatar */}
      <div
        className={`w-8 h-8 rounded-full flex-shrink-0 flex items-center justify-center ${
          isUser ? "bg-[#0E6BA8]" : "bg-[#1A3A6B] border border-[#0E6BA8]/30"
        }`}
      >
        {isUser ? <User size={14} className="text-white" /> : <Bot size={14} className="text-[#6B9AB8]" />}
      </div>

      {/* Content */}
      <div className={`max-w-[80%] ${isUser ? "items-end" : "items-start"} flex flex-col gap-1`}>
        <div
          className={`rounded-2xl px-4 py-3 text-sm ${
            isUser
              ? "bg-[#0E6BA8] text-white rounded-tr-sm"
              : message.isError
              ? "bg-red-900/30 border border-red-500/30 text-red-300 rounded-tl-sm"
              : "bg-[#1A3A6B] border border-[#0E6BA8]/10 rounded-tl-sm"
          }`}
        >
          {isUser ? (
            <p className="text-white leading-relaxed">{message.content}</p>
          ) : (
            <div className="prose prose-invert max-w-none text-sm">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{message.content}</ReactMarkdown>
            </div>
          )}
        </div>

        {/* Tool call badges */}
        {message.toolCalls?.length > 0 && (
          <div className="flex gap-1.5 flex-wrap">
            {message.toolCalls.map((tool) => (
              <ToolTag key={tool} name={tool} />
            ))}
          </div>
        )}

        <span className="text-[#6B9AB8]/50 text-xs px-1">
          {new Date(message.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
        </span>
      </div>
    </div>
  );
}

function ToolTag({ name }) {
  const labels = {
    sql_query_tool: { label: "SQL", color: "text-green-400 bg-green-400/10 border-green-400/20" },
    ml_predict_tool: { label: "ML", color: "text-purple-400 bg-purple-400/10 border-purple-400/20" },
    rag_search_tool: { label: "RAG", color: "text-amber-400 bg-amber-400/10 border-amber-400/20" },
  };
  const { label, color } = labels[name] || { label: name, color: "text-blue-400 bg-blue-400/10 border-blue-400/20" };
  return (
    <span className={`text-xs font-mono px-2 py-0.5 rounded-full border ${color}`}>
      {label}
    </span>
  );
}

function TypingIndicator() {
  return (
    <div className="flex gap-3 animate-fade-in">
      <div className="w-8 h-8 rounded-full bg-[#1A3A6B] border border-[#0E6BA8]/30 flex items-center justify-center flex-shrink-0">
        <Bot size={14} className="text-[#6B9AB8]" />
      </div>
      <div className="bg-[#1A3A6B] border border-[#0E6BA8]/10 rounded-2xl rounded-tl-sm px-4 py-3">
        <div className="flex gap-1.5 items-center h-4">
          {[0, 1, 2].map((i) => (
            <div
              key={i}
              className="w-2 h-2 rounded-full bg-[#6B9AB8]"
              style={{ animation: `pulseDot 1.4s ease-in-out ${i * 0.2}s infinite` }}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
