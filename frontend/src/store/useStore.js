import { create } from "zustand";
import { v4 as uuidv4 } from "uuid";
import api from "../services/api.js";

const useStore = create((set, get) => ({
  // Chat state
  sessionId: uuidv4(),
  messages: [],
  isLoading: false,
  activeTools: [],

  // Dashboard state
  dashboardData: null,
  dashboardLoading: false,

  sendMessage: async (text) => {
    const { sessionId, messages } = get();

    // Add user message immediately
    const userMsg = { id: uuidv4(), role: "user", content: text, timestamp: new Date() };
    set({ messages: [...messages, userMsg], isLoading: true, activeTools: [] });

    try {
      const history = messages.map((m) => ({ role: m.role, content: m.content }));
      const res = await api.post("/chat/", { message: text, session_id: sessionId, history });

      const assistantMsg = {
        id: uuidv4(),
        role: "assistant",
        content: res.data.content,
        toolCalls: res.data.tool_calls || [],
        timestamp: new Date(),
      };

      set((state) => ({
        messages: [...state.messages, assistantMsg],
        isLoading: false,
        activeTools: res.data.tool_calls || [],
      }));
    } catch (err) {
      const errMsg = {
        id: uuidv4(),
        role: "assistant",
        content: `⚠️ Error: ${err.response?.data?.detail || err.message}. Make sure the backend is running.`,
        toolCalls: [],
        timestamp: new Date(),
        isError: true,
      };
      set((state) => ({ messages: [...state.messages, errMsg], isLoading: false }));
    }
  },

  clearChat: () => set({ messages: [], sessionId: uuidv4(), activeTools: [] }),

  loadDashboard: async () => {
    set({ dashboardLoading: true });
    try {
      const [customersRes, ordersRes] = await Promise.all([
        api.post("/query/", { question: "Show top 10 customers by contract value with their region and segment" }),
        api.post("/query/", { question: "Show total revenue by region" }),
      ]);
      set({
        dashboardData: {
          customers: customersRes.data.result,
          revenue: ordersRes.data.result,
        },
        dashboardLoading: false,
      });
    } catch {
      set({ dashboardLoading: false });
    }
  },
}));

export default useStore;
