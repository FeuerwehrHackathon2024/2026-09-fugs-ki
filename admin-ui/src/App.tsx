import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { Sidebar } from "@/components/Sidebar";
import { KnowledgeHubPage } from "@/pages/KnowledgeHubPage";
import { SystemPromptPage } from "@/pages/SystemPromptPage";

export default function App() {
  return (
    <BrowserRouter>
      <div className="flex h-screen overflow-hidden bg-[var(--color-surface)]">
        <Sidebar />
        <main className="flex-1 overflow-y-auto">
          <Routes>
            <Route path="/" element={<Navigate to="/knowledge-hub" replace />} />
            <Route path="/knowledge-hub" element={<KnowledgeHubPage />} />
            <Route path="/system-prompt" element={<SystemPromptPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
