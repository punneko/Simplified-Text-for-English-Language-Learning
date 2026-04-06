import React, { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import axios from "axios";
import { DateTime } from "luxon";

const History = () => {
  const [historyData, setHistoryData] = useState([]);
  const [expandedIndex, setExpandedIndex] = useState(null);
  const [viewMode, setViewMode] = useState("original");
  const user_id = localStorage.getItem("user_id");

  const formatDateThai = (dateString) => {
    if (!dateString) return "-";

    let dt = DateTime.fromFormat(dateString, "dd/MM/yyyy HH:mm:ss", {
      zone: "utc",
    });

    dt = dt.setZone("Asia/Bangkok");

    if (!dt.isValid) return "Invalid Datetime";

    return dt.toFormat("dd/MM/yyyy HH:mm");
  };

  useEffect(() => {
    if (!user_id) return;

    axios
      .get("http://localhost:5000/api/history", {
        headers: { "X-User-Id": user_id },
      })
      .then((res) => {
        if (Array.isArray(res.data)) {
          setHistoryData(res.data);
        } else {
          setHistoryData([]);
        }
      })
      .catch((err) => console.error(err));
  }, [user_id]);

  const toggleDetails = (index) => {
    setExpandedIndex(expandedIndex === index ? null : index);
    setViewMode("original");
  };

  return (
    <div className="fredoka-font min-h-screen bg-white pt-16 flex">
      <Sidebar
        isOpen={true}
        alwaysOpen={true}
        customColor="bg-gradient-to-t from-sky-200 to-white"
      />

      <div className="flex-1 flex flex-col">
        <Navbar disableHamburger={true} />

        <main className="flex-1 p-6 overflow-auto max-w-4xl mx-auto w-full ml-80">
          <h1 className="text-4xl font-bold mb-6 text-black">All History</h1>

          {historyData.length === 0 ? (
            <div className="text-center py-20">
              <p className="text-gray-500 text-lg">ยังไม่มีประวัติการใช้งาน</p>
              <p className="text-gray-400 text-sm mt-2">
                ข้อความที่คุณ Simplify จะปรากฏที่นี่
              </p>
            </div>
          ) : (
            historyData.map((entry, index) => {
              const vocabulary = Array.isArray(entry.vocabulary)
                ? entry.vocabulary
                : entry.vocabulary?.[viewMode] || [];

              const grammar = entry.grammar || {
                original: [],
                simplified: [],
              };

              return (
                <div key={index} className="border-b pb-6 mb-6">
                  <div className="flex justify-between items-start mb-2">
                    <div className="max-w-[70%]">
                      <p className="font-medium text-black break-words">
                        {entry.original_text || "-"}
                      </p>
                      <p className="text-gray-600 break-words">
                        {entry.simplified_text || "-"}
                      </p>
                    </div>

                    <div className="text-gray-500 text-sm whitespace-nowrap">
                      {formatDateThai(entry.created_at)}
                    </div>
                  </div>

                  
                  <div className="text-right mt-3">
                    <button
                      onClick={() => toggleDetails(index)}
                      className="px-5 py-2 rounded-full bg-sky-500 text-white shadow-md 
                               hover:bg-sky-600 hover:shadow-lg 
                               transition-all duration-200"
                    >
                      {expandedIndex === index
                        ? "Hide Details ▲"
                        : "Show Details ▼"}
                    </button>
                  </div>

                  
                  {expandedIndex === index && (
                    <div
                      className="mt-5 space-y-6 
                                  bg-sky-50/60 
                                  backdrop-blur-lg 
                                  p-6 
                                  rounded-3xl 
                                  shadow-lg 
                                  border border-sky-100"
                    >
                      
                      <div className="flex justify-center gap-4">
                        <button
                          className={`px-6 py-2 rounded-full font-medium transition-all duration-200 ${
                            viewMode === "original"
                              ? "bg-sky-500 text-white shadow-md"
                              : "bg-white border border-sky-200 text-gray-600"
                          }`}
                          onClick={() => setViewMode("original")}
                        >
                          Original
                        </button>
                        <button
                          className={`px-6 py-2 rounded-full font-medium transition-all duration-200 ${
                            viewMode === "simplified"
                              ? "bg-sky-500 text-white shadow-md"
                              : "bg-white border border-sky-200 text-gray-600"
                          }`}
                          onClick={() => setViewMode("simplified")}
                        >
                          Simplified
                        </button>
                      </div>

                      
                      <div className="bg-white p-5 rounded-2xl shadow-md border border-sky-100">
                        <h2 className="font-bold text-lg mb-3 text-sky-700">
                          Vocabulary
                        </h2>

                        {vocabulary.length > 0 ? (
                          <ul className="list-disc list-inside text-sm space-y-2">
                            {vocabulary.map((v, i) => (
                              <li key={i}>
                                <strong className="text-sky-700">
                                  {v.word}
                                </strong>{" "}
                                ({v.cefr || "-"}) ={" "}
                                {v.definition_th ||
                                  v.translation_th ||
                                  v.definition_en ||
                                  "-"}
                                {v.synonyms?.length > 0 && (
                                  <div className="text-gray-500 ml-5 italic mt-1">
                                    Synonyms:{" "}
                                    {v.synonyms
                                      .map(
                                        (s) => `${s.word} (${s.cefr || "-"})`,
                                      )
                                      .join(", ")}
                                  </div>
                                )}
                              </li>
                            ))}
                          </ul>
                        ) : (
                          <p className="text-sm text-gray-500">
                            No vocabulary info
                          </p>
                        )}
                      </div>

                     
                      <div className="bg-white p-5 rounded-2xl shadow-md border border-sky-100">
                        <h2 className="font-bold text-lg mb-3 text-sky-700">
                          Grammar
                        </h2>

                        <div className="space-y-3">
                          {grammar?.[viewMode]?.length > 0 ? (
                            grammar[viewMode].map((g, i) => (
                              <div
                                key={i}
                                className="bg-sky-50 p-4 rounded-xl shadow-sm"
                              >
                                {g.topic && (
                                  <h4 className="font-semibold mb-2">
                                    {g.topic}
                                  </h4>
                                )}

                                <ul className="list-disc list-inside text-sm space-y-1 whitespace-pre-line">
                                  {g.explanation ? (
                                    Object.values(g.explanation).map(
                                      (v, idx) => <li key={idx}>{v}</li>,
                                    )
                                  ) : g.explanation_th ? (
                                    <li>{g.explanation_th}</li>
                                  ) : (
                                    <li>No explanation available</li>
                                  )}
                                </ul>
                              </div>
                            ))
                          ) : (
                            <p className="text-sm text-gray-500">
                              No grammar info
                            </p>
                          )}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              );
            })
          )}
        </main>
      </div>
    </div>
  );
};

export default History;
