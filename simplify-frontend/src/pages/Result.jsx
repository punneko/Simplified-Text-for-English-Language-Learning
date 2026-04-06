import React, { useState, useRef, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import TooltipText from "../components/Tooltip";
import axios from "axios";

const EXPLANATION_KEYS = [
  "what_it_is",
  "effect_on_meaning",
  "usage_note",
  "what_it_does_here",
  "structure",
  "examples",
];

const Result = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(true);
  const [viewMode, setViewMode] = useState("original");
  const [hoveredWord, setHoveredWord] = useState(null);
  const [showEnglish, setShowEnglish] = useState(false);
  const [loading, setLoading] = useState(true);

  const [data, setData] = useState({
    original: "",
    simplified: "",
    translation: { original: "", simplified: "" },
    grammar: { original: [], simplified: [] },
    vocabulary: [],
    alignment: [],
    tokens: { original: [], simplified: [] },
    highlights: [],
  });

  const navigate = useNavigate();
  const location = useLocation();
  const hasFetched = useRef(false);

  const toggleSidebar = () => setSidebarOpen(!sidebarOpen);

  const fetchSimplify = async (text) => {
    const userId = localStorage.getItem("user_id");
    if (!userId) {
      navigate("/login");
      return;
    }

    try {
      setLoading(true);
      const res = await axios.post(
        "http://localhost:5000/api/simplify",
        { text },
        { headers: { "X-User-Id": userId } },
      );
      setData(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (hasFetched.current) return;
    hasFetched.current = true;

    const init = async () => {
      if (location.state?.original) {
        setData(location.state);
        setLoading(false);
      } else {
        const params = new URLSearchParams(window.location.search);
        const text = params.get("text");
        if (!text) {
          navigate("/simplifier");
          return;
        }
        await fetchSimplify(text);
      }
    };

    init();
  }, []);

  const handleReset = () => navigate("/simplifier");

  const renderTranslation = () => (
    <div className="mb-6 p-4 bg-white/80 backdrop-blur-xl rounded-2xl shadow border border-white/40">
      <h2 className="font-bold text-lg mb-2">Translation ({viewMode})</h2>
      <p className="text-gray-700 whitespace-pre-wrap">
        {data.translation?.[viewMode]?.trim()
          ? data.translation[viewMode]
          : "—"}
      </p>
    </div>
  );

  const renderVocabulary = () =>
    data.vocabulary?.length > 0 && (
      <>
        <div className="flex justify-between items-center mb-3">
          <h2 className="font-bold text-lg">Suggested Vocabulary</h2>
          <button
            onClick={() => setShowEnglish(!showEnglish)}
            className="text-xs px-3 py-1 bg-gray-200 rounded-full hover:bg-gray-300 transition-all duration-200"
          >
            {showEnglish ? "TH" : "EN"}
          </button>
        </div>

        <ul className="list-disc list-inside text-sm space-y-3 mb-6">
          {data.vocabulary.map((v, i) => (
            <li key={i}>
              <strong>{v.word}</strong> ({v.cefr || "-"}) ={" "}
              {showEnglish ? v.definition_en || "-" : v.translation_th || "-"}
              {v.synonyms?.length > 0 && (
                <div className="text-gray-500 ml-5 italic mt-1">
                  Synonyms:{" "}
                  {v.synonyms
                    .map((s) => `${s.word} (${s.cefr || "-"})`)
                    .join(", ")}
                </div>
              )}
            </li>
          ))}
        </ul>
      </>
    );

  const renderGrammar = () =>
    data.grammar?.[viewMode]?.length > 0 && (
      <>
        <h2 className="font-bold text-lg mb-2">Grammar Tip</h2>
        <div className="space-y-3">
          {data.grammar[viewMode].map((g, i) => (
            <div
              key={i}
              className="relative z-50 bg-white/80 backdrop-blur-xl min-h-[12rem] p-6 rounded-2xl shadow-xl border border-white/40 leading-7"
            >
              {g.topic && <h3 className="font-semibold mb-2">{g.topic}</h3>}

              {g.explanation && (
                <ul className="list-disc list-inside text-sm space-y-1">
                  {EXPLANATION_KEYS.map((key) => {
                    if (!g.explanation[key]) return null;

                    if (key === "structure") {
                      return (
                        <li key={key}>
                          <strong>โครงสร้างประโยค:</strong>{" "}
                          {g.explanation.structure}
                        </li>
                      );
                    }

                    if (key === "examples") {
                      return (
                        <li key={key}>
                          <strong>ประโยคที่พบ:</strong>
                          <ul className="list-disc list-inside ml-5 mt-1 space-y-1">
                            {g.explanation.examples.map((ex, idx) => (
                              <li key={idx}>{ex}</li>
                            ))}
                          </ul>
                        </li>
                      );
                    }

                    return <li key={key}>{g.explanation[key]}</li>;
                  })}
                </ul>
              )}
            </div>
          ))}
        </div>
      </>
    );

  return (
    <div className="relative fredoka-font min-h-screen bg-gradient-to-br from-sky-200 via-blue-100 to-white pt-16 overflow-hidden">
      <div className="absolute top-24 left-24 w-80 h-80 bg-sky-300 rounded-full blur-3xl opacity-30"></div>
      <div className="absolute bottom-24 right-24 w-80 h-80 bg-blue-300 rounded-full blur-3xl opacity-30"></div>

      <Navbar toggleSidebar={toggleSidebar} zIndex="z-50" />
      <Sidebar
        isOpen={sidebarOpen}
        toggleMenu={toggleSidebar}
        customColor="bg-sky-100"
      />

      <main
        className={`relative z-10 transition-transform duration-300 ${
          sidebarOpen ? "translate-x-64" : "translate-x-0"
        } p-4`}
      >
        <div className="max-w-7xl mx-auto px-3 lg:px-6">
          <h1 className="text-4xl font-bold mb-8 text-gray-800">
            Text Simplifier Tool
          </h1>

          <div className="flex flex-col lg:flex-row gap-8">
            <div className="w-full lg:w-[60%] space-y-6">
              <div className="bg-white/80 backdrop-blur-xl min-h-[12rem] p-6 rounded-2xl shadow-xl border border-white/40 leading-7">
                {data.original ? (
                  <TooltipText
                    tokens={data.tokens?.original}
                    vocabulary={data.vocabulary}
                    alignment={data.alignment}
                    structure={data.structure?.original}
                    highlights={data.highlights}
                    mode="original"
                    hoveredWord={hoveredWord}
                    onHover={setHoveredWord}
                  />
                ) : (
                  "กำลังโหลด..."
                )}
              </div>

              <div className="flex justify-end">
                <button
                  onClick={handleReset}
                  className="px-6 py-2 bg-sky-500 text-white rounded-xl shadow-md hover:bg-sky-600 hover:scale-105 transition-all duration-200"
                >
                  Reset
                </button>
              </div>

              <div className="bg-white/80 backdrop-blur-xl min-h-[12rem] p-6 rounded-2xl shadow-xl border border-white/40 leading-7">
                {data.simplified ? (
                  <TooltipText
                    tokens={data.tokens?.simplified}
                    vocabulary={data.vocabulary}
                    alignment={data.alignment}
                    highlights={data.highlights}
                    mode="simplified"
                    hoveredWord={hoveredWord}
                    onHover={setHoveredWord}
                  />
                ) : (
                  "กำลังโหลด..."
                )}
              </div>
            </div>

            <div className="w-full lg:w-[40%] lg:sticky lg:top-24 h-fit">
              <div className="text-center mb-4">
                <button
                  onClick={() => setShowSuggestions(!showSuggestions)}
                  className="px-6 py-2 bg-sky-500 text-white rounded-full shadow-md hover:bg-sky-600 hover:scale-105 transition-all duration-200"
                >
                  {showSuggestions
                    ? "Hide Suggestions ▲"
                    : "Show Suggestions ▼"}
                </button>
              </div>

              {showSuggestions && (
                <div className="p-6 bg-white/70 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/40 lg:max-h-[calc(100vh-140px)] lg:overflow-y-auto">
                  {loading ? (
                    <div className="flex flex-col items-center justify-center py-12 space-y-4">
                      <div className="w-10 h-10 border-4 border-sky-300 border-t-sky-600 rounded-full animate-spin"></div>
                      <p className="text-gray-700 font-medium">
                        กำลังโหลดคำอธิบาย...
                      </p>
                      <p className="text-sm text-gray-500">กรุณารอสักครู่</p>
                    </div>
                  ) : (
                    <>
                      <div className="flex justify-center gap-3 mb-6">
                        <button
                          className={`px-6 py-2 rounded-full transition-all duration-200 ${
                            viewMode === "original"
                              ? "bg-sky-500 text-white shadow-md"
                              : "bg-white border border-white/40 hover:bg-white"
                          }`}
                          onClick={() => setViewMode("original")}
                        >
                          Original
                        </button>
                        <button
                          className={`px-6 py-2 rounded-full transition-all duration-200 ${
                            viewMode === "simplified"
                              ? "bg-sky-500 text-white shadow-md"
                              : "bg-white border border-white/40 hover:bg-white"
                          }`}
                          onClick={() => setViewMode("simplified")}
                        >
                          Simplified
                        </button>
                      </div>

                      {renderTranslation()}
                      {renderVocabulary()}
                      {renderGrammar()}
                    </>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Result;
