import { useState, useRef } from "react";
import { Send } from "lucide-react";
import useStore from "../../store/useStore.js";

export default function ChatInput({ disabled }) {
  const [value, setValue] = useState("");
  const { sendMessage } = useStore();
  const textareaRef = useRef(null);

  const handleSubmit = () => {
    const trimmed = value.trim();
    if (!trimmed || disabled) return;
    sendMessage(trimmed);
    setValue("");
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleInput = (e) => {
    setValue(e.target.value);
    e.target.style.height = "auto";
    e.target.style.height = Math.min(e.target.scrollHeight, 140) + "px";
  };

  return (
    <div className="flex items-end gap-3 bg-[#1A3A6B]/40 border border-[#1A3A6B] hover:border-[#0E6BA8]/50 focus-within:border-[#0E6BA8] rounded-xl px-4 py-3 transition-colors">
      <textarea
        ref={textareaRef}
        value={value}
        onChange={handleInput}
        onKeyDown={handleKeyDown}
        disabled={disabled}
        placeholder="Ask about your data, customers, predictions…"
        rows={1}
        className="flex-1 bg-transparent text-white placeholder-[#6B9AB8]/60 text-sm resize-none focus:outline-none leading-relaxed"
        style={{ maxHeight: "140px" }}
      />
      <button
        onClick={handleSubmit}
        disabled={!value.trim() || disabled}
        className="w-8 h-8 rounded-lg bg-[#0E6BA8] disabled:bg-[#1A3A6B] disabled:text-[#6B9AB8]/40 flex items-center justify-center text-white transition-all duration-150 hover:bg-[#0A5A8A] flex-shrink-0"
      >
        <Send size={14} />
      </button>
    </div>
  );
}
