import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";           // The main landing content with Get Started
import Dashboard from "./pages/Dashboard"; // Dashboard component
import MeetingDetails from "./pages/MeetingDetails"; // add this at the top


export default function App() {
  return (
    <Router>
      <div className="relative min-h-screen bg-gradient-to-br from-[#e9dcc8] to-[#f5f0e6] flex flex-col items-center text-center px-4 overflow-hidden">
        
        {/* === Background SVGs here (unchanged) === */}

        {/* === Heading === */}
        <h1 className="absolute top-6 left-1/2 transform -translate-x-1/2 text-[4rem] md:text-[10rem] lg:text-[15rem] font-extrabold text-[#3b2f2f] z-10 leading-none">
          NexMeet
        </h1>

        {/* === Routes: Home or Dashboard === */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/meeting/:id" element={<MeetingDetails />} /> {/* ✅ NEW */}

        </Routes>

        {/* === Footer === */}
        <div className=" bottom-4 left-4 text-sm text-[#5c4a2f] z-10">
          Crafted by Dhyey Patel
        </div>
        <div className=" bottom-4 right-4 text-sm text-[#5c4a2f] z-10">
          © 2025 NexMeet. All rights reserved.
        </div>
      </div>
    </Router>
  );
}
