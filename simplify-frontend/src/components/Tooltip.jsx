import React, { useMemo } from "react";

const buildVocabMap = (vocab = []) => {
  const map = {};
  vocab.forEach((v) => {
    const firstMeaning = v.translation_th?.split(",")[0]?.trim();
    map[v.word.toLowerCase()] = firstMeaning;
  });
  return map;
};

const TooltipText = ({
  tokens = [],
  vocabulary = [],
  structure = null,
  mode = "original",
  hoveredWord,
  onHover,

  highlights = [],
}) => {
  const vocabMap = useMemo(() => buildVocabMap(vocabulary), [vocabulary]);

  const highlightSet = useMemo(() => {
    const set = new Set();

    highlights.forEach((h) => {
      if (
        h.replacement &&
        h.original &&
        h.replacement.toLowerCase() !== h.original.toLowerCase()
      ) {
        set.add(h.original.toLowerCase());
        set.add(h.replacement.toLowerCase());
      }
    });

    return set;
  }, [highlights]);

  const mainStart = structure?.main?.start;
  const mainEnd = structure?.main?.end;
  const subStart = structure?.subordinate?.start;
  const subEnd = structure?.subordinate?.end;
  const rootIndex = structure?.root?.index;

  return (
    <>
      {tokens.map((token, index) => {
        const clean = token.toLowerCase().replace(/[^\w']/g, "");
        const meaning = vocabMap[clean];

        const isHighlighted = highlightSet.has(clean);

        const inMain =
          mainStart !== undefined &&
          mainEnd !== undefined &&
          index >= mainStart &&
          index <= mainEnd;

        const inSub =
          subStart !== undefined &&
          subEnd !== undefined &&
          index >= subStart &&
          index <= subEnd;

        const isRoot = index === rootIndex;

        return (
          <span
            key={index}
            className={`
              relative word-span
              ${meaning ? "word-tooltip" : ""}
              ${isHighlighted ? "highlight-replaced" : ""}
              ${inMain ? "main-clause-underline" : ""}
              ${inSub ? "sub-clause-underline" : ""}
              ${isRoot ? "root-verb-ring" : ""}
            `}
            onMouseEnter={() => onHover?.(clean)}
            onMouseLeave={() => onHover?.(null)}
          >
            {token + " "}

            {meaning && <span className="tooltip">{meaning}</span>}

            {isRoot && structure && (
              <span className="structure-tooltip">
                <strong>โครงสร้างประโยค</strong>
                <hr style={{ margin: "6px 0" }} />

                {structure.root && (
                  <>
                    <strong>กริยาหลัก: </strong>
                    {structure.root.text}
                    <br />
                  </>
                )}

                {structure.main && (
                  <>
                    <strong>ประโยคหลัก: </strong>
                    {structure.main.text}
                    <br />
                  </>
                )}

                {structure.subordinate && (
                  <>
                    <strong>ประโยคขยาย: </strong>
                    {structure.subordinate.text}
                  </>
                )}
              </span>
            )}
          </span>
        );
      })}
    </>
  );
};

export default TooltipText;
