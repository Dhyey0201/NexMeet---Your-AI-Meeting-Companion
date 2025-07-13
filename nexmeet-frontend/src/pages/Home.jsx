// import { useNavigate } from "react-router-dom";

// export default function Home() {
//   const navigate = useNavigate();

//   return (
//     <div className="flex-grow flex flex-col justify-center items-center space-y-4 mx-auto pt-20 z-10">
//       <h2 className="text-6xl md:text-8xl font-semibold text-[#5c4a2f] leading-none">
//         Your AI Meeting Companion
//       </h2>

//       <p className="text-md md:text-lg text-[#5c4a2f]">
//         Transcribe, summarize, detect emotions, and extract action items — all with one smart assistant.
//       </p>

//       <button
//         onClick={() => navigate("/dashboard")}
//         className="bg-[#ffffffcc] text-[#3b2f2f] text-lg sm:text-xl md:text-2xl lg:text-3xl font-bold px-8 py-5 rounded-full shadow-lg hover:bg-white hover:scale-105 transition-all duration-300 mt-6"
//       >
//         Get Started
//       </button>
//     </div>
//   );
// }
import { useNavigate } from "react-router-dom";
import "../Home.css";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="home-container">
      {/* Abstract Background Shapes */}
      <div className="shape shape-1"></div>
      <div className="shape shape-2"></div>
      <div className="shape shape-3"></div>
      <div className="shape shape-4"></div>
      <div className="shape shape-5"></div>
      
      {/* Content */}
      <div className="home-content">
        <h2 className="home-title">
          Your AI Meeting Companion
        </h2>

        <p className="home-subtitle">
          Transcribe, summarize, detect emotions, and extract action items — all with one smart assistant.
        </p>

        <button
          onClick={() => navigate("/dashboard")}
          className="home-button"
        >
          Get Started
        </button>
      </div>
    </div>
  );
}