// pdf-wait-mermaid.js — init + interceptor PDF unificados

document.addEventListener("DOMContentLoaded", function () {

  // 1. Inicializar y renderizar Mermaid
  window.mermaidReady = new Promise((resolve) => {
    mermaid.initialize({ startOnLoad: false, theme: "default" });

    const elements = document.querySelectorAll(".mermaid");
    if (elements.length === 0) { resolve(); return; }

    mermaid.run({ nodes: elements })
      .then(resolve)
      .catch((err) => { console.warn("Mermaid error:", err); resolve(); });
  });

  // 2. Interceptar botón de exportar PDF
  const waitForButton = setInterval(() => {
    const pdfButton = document.querySelector(".print-page-button, [data-print-page]");
    if (pdfButton) {
      clearInterval(waitForButton);
      pdfButton.addEventListener("click", async (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (window.mermaidReady) await window.mermaidReady;
        await new Promise((r) => setTimeout(r, 200));
        window.print();
      });
    }
  }, 300);
});