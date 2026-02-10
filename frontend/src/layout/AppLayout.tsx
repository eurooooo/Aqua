import { Outlet } from "react-router";

import AppHeader from "@/components/navigation/AppHeader";
import BottomNav from "@/components/navigation/BottomNav";

function AppLayout() {
  return (
    <div className="min-h-screen bg-slate-50 pb-24 text-slate-900">
      <AppHeader />
      <main className="mx-auto w-full max-w-5xl px-4 sm:px-6">
        <Outlet />
      </main>
      <BottomNav />
    </div>
  );
}

export default AppLayout;
