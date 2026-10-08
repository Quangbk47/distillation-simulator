const tabs = document.querySelectorAll("[data-tab]");
const panels = document.querySelectorAll("[data-panel]");
const form = document.querySelector("#simulation-form");
const formError = document.querySelector("#form-error");
const resetButton = document.querySelector("#reset-button");
const diagramNLabel = document.querySelector("#diagram-n-label");
const diagramFeedLabel = document.querySelector("#diagram-feed-label");

function selectTab(name) {
  tabs.forEach((tab) => tab.classList.toggle("is-active", tab.dataset.tab === name));
  panels.forEach((panel) => panel.classList.toggle("is-active", panel.dataset.panel === name));
}

tabs.forEach((tab) => tab.addEventListener("click", () => selectTab(tab.dataset.tab)));

function numberValue(name) {
  return Number(form.elements[name].value);
}

function updateDiagramLabels() {
  const n = form.elements.N.value || "—";
  const nf = form.elements.NF.value || "—";
  const f = form.elements.F_kmol_h.value || "—";
  const zf = form.elements.zF_ethanol.value || "—";
  diagramNLabel.textContent = `N = ${n}`;
  diagramFeedLabel.innerHTML = `Feed F=${f}<br />zF=${zf} · NF=${nf}`;
}

["N", "NF", "F_kmol_h", "zF_ethanol"].forEach((name) => {
  form.elements[name].addEventListener("input", updateDiagramLabels);
});
updateDiagramLabels();

function validateForm() {
  const f = numberValue("F_kmol_h");
  const zf = numberValue("zF_ethanol");
  const n = numberValue("N");
  const nf = numberValue("NF");
  const d = numberValue("D_kmol_h");
  const values = [f, zf, numberValue("P_bar"), numberValue("q"), n, nf, numberValue("R"), d, numberValue("heatLoss_kW")];
  if (values.some((value) => !Number.isFinite(value))) return "Vui lòng nhập các giá trị số hợp lệ.";
  if (f <= 0 || zf <= 0 || zf >= 1 || numberValue("P_bar") <= 0 || n < 1 || !Number.isInteger(n)) return "Kiểm tra F, zF, P và N theo miền hợp lệ.";
  if (nf < 1 || nf > n || !Number.isInteger(nf)) return "NF phải là số nguyên trong khoảng 1..N.";
  if (numberValue("R") < 0 || d <= 0 || d >= f || numberValue("heatLoss_kW") < 0) return "Kiểm tra R, D và heatLoss_kW.";
  return "";
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  formError.textContent = validateForm();
  if (formError.textContent) return;

  const payload = Object.fromEntries(new FormData(form).entries());
  for (const key of ["F_kmol_h", "zF_ethanol", "q", "P_bar", "N", "NF", "R", "D_kmol_h", "heatLoss_kW"]) {
    payload[key] = Number(payload[key]);
  }
  payload.condenser = form.elements.condenser.value;

  setResultStatus("CALCULATING");
  document.querySelector("#connection-status").textContent = "ENGINE CONNECTING";
  fetch("/api/simulations", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
    .then(async (response) => {
      const body = await response.json();
      if (!response.ok) throw new Error(body.detail || "API calculation failed");
      return body;
    })
    .then(renderResult)
    .catch((error) => {
      setResultStatus("FAILED");
      document.querySelector("#connection-status").textContent = "ENGINE ERROR";
      document.querySelector("#warning-text").textContent = error.message;
      document.querySelector("#stage-table").innerHTML = `<div class="table-empty">FAILED · ${escapeHtml(error.message)}</div>`;
      renderEmptyPlot("FAILED · Không có dữ liệu đồ thị");
    });
});

function formatNumber(value, digits = 4) {
  return typeof value === "number" && Number.isFinite(value) ? value.toFixed(digits) : "—";
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function setResultStatus(status) {
  const badge = document.querySelector("#result-status");
  badge.textContent = status;
  badge.dataset.status = status.toLowerCase();
}

function renderResult(result) {
  document.querySelector("#connection-status").textContent = "ENGINE CONNECTED";
  setResultStatus(result.status.toUpperCase());
  document.querySelector("#result-xd").textContent = formatNumber(result.xD);
  document.querySelector("#result-xb").textContent = formatNumber(result.xB);
  document.querySelector("#result-recovery").textContent = formatNumber(result.recovery_ethanol_percent, 2);
  document.querySelector("#result-d").textContent = formatNumber(result.D_kmol_h, 2);
  document.querySelector("#result-b").textContent = formatNumber(result.B_kmol_h, 2);
  document.querySelector("#result-duty").textContent = `${formatNumber(result.QC_kW, 2)} / ${formatNumber(result.QR_kW, 2)}`;
  document.querySelector("#thermo-version").textContent = result.thermoDataVersion;
  document.querySelector("#residuals").textContent = JSON.stringify(result.residuals);
  document.querySelector("#warning-text").textContent = warningText(result);
  if (result.status === "failed") {
    document.querySelector("#stage-table").innerHTML = `<div class="table-empty">FAILED · ${escapeHtml(result.errorCode || "CALCULATION_FAILED")} · Chưa có stage output hợp lệ</div>`;
  } else {
    document.querySelector("#stage-table").innerHTML = `<table><thead><tr><th>Mâm</th><th>Section</th><th>xEtOH</th><th>yEtOH</th><th>T (°C)</th></tr></thead><tbody>${result.stages.map((stage) => `<tr><td>${stage.stage}</td><td>${stage.section}</td><td>${formatNumber(stage.x_ethanol)}</td><td>${formatNumber(stage.y_ethanol)}</td><td>${formatNumber(stage.T_C, 2)}</td></tr>`).join("")}</tbody></table>`;
  }
  updateDiagramLabels();
  renderMcCabePlot(result);
}

function warningText(result) {
  if (result.status === "failed") {
    const code = result.errorCode ? `${result.errorCode}: ` : "";
    return `${code}${result.errorMessage || "Không hội tụ với bộ input hiện tại. Kiểm tra lại D, N/NF, R và quy ước số liệu."}`;
  }
  const details = result.warningDetails ?? [];
  if (details.length) {
    return details.map((detail) => {
      const range = detail.sourceRange;
      return `${detail.code}: ${detail.component} T=${detail.actualTemperature.toFixed(2)} ${detail.temperatureUnit}; source range ${range.min.toFixed(2)}–${range.max.toFixed(2)} ${range.unit}`;
    }).join(" | ");
  }
  return result.warnings.length ? result.warnings.join(", ") : "None";
}

function linePoint(line, x) {
  return line.slope * x + line.intercept;
}

function svgPath(points, sx, sy) {
  return points.map((point, index) => `${index === 0 ? "M" : "L"} ${sx(point.x)} ${sy(point.y)}`).join(" ");
}

function renderMcCabePlot(result) {
  const target = document.querySelector("#mccabe-plot");
  const status = document.querySelector("#plot-status");
  const lines = result.operatingLines;
  if (!lines || !result.stages.length) {
    const message = result.status === "failed" ? "FAILED · Không có dữ liệu đồ thị hợp lệ" : "NO GRAPH DATA";
    status.textContent = result.status === "failed" ? "FAILED" : "NOT CALCULATED";
    renderEmptyPlot(message);
    return;
  }

  const width = 520;
  const height = 360;
  const pad = 38;
  const sx = (x) => pad + x * (width - 2 * pad);
  const sy = (y) => height - pad - y * (height - 2 * pad);
  const equilibrium = lines.equilibriumCurve ?? [];
  const stagePoints = [{ x: result.xD, y: result.xD }];
  let previousY = result.xD;
  for (const stage of result.stages) {
    stagePoints.push({ x: stage.x_ethanol, y: previousY });
    stagePoints.push({ x: stage.x_ethanol, y: stage.y_ethanol });
    previousY = stage.y_ethanol;
  }

  const rectEndX = Math.min(1, Math.max(0, lines.feedIntersection?.x ?? result.xD));
  const rectifying = [
    { x: result.xD, y: result.xD },
    { x: rectEndX, y: linePoint(lines.rectifying, rectEndX) },
  ];
  const stripping = [
    { x: result.xB, y: result.xB },
    { x: rectEndX, y: linePoint(lines.stripping, rectEndX) },
  ];
  const qLine = lines.qLine?.vertical
    ? [
        { x: rectEndX, y: 0 },
        { x: rectEndX, y: 1 },
      ]
    : [
        { x: 0, y: linePoint(lines.qLine, 0) },
        { x: 1, y: linePoint(lines.qLine, 1) },
      ];

  status.textContent = "CALCULATED";
  target.className = "plot-surface";
  target.innerHTML = `
    <svg viewBox="0 0 ${width} ${height}" role="img" aria-label="McCabe-Thiele x-y plot">
      <line class="plot-axis" x1="${pad}" y1="${sy(0)}" x2="${sx(1)}" y2="${sy(0)}"></line>
      <line class="plot-axis" x1="${pad}" y1="${sy(0)}" x2="${pad}" y2="${sy(1)}"></line>
      <path class="plot-diagonal" d="${svgPath([{ x: 0, y: 0 }, { x: 1, y: 1 }], sx, sy)}"></path>
      <path class="plot-equilibrium" d="${svgPath(equilibrium.map((point) => ({ x: point.x_ethanol, y: point.y_ethanol })), sx, sy)}"></path>
      <path class="plot-rectifying" d="${svgPath(rectifying, sx, sy)}"></path>
      <path class="plot-stripping" d="${svgPath(stripping, sx, sy)}"></path>
      <path class="plot-qline" d="${svgPath(qLine, sx, sy)}"></path>
      <path class="plot-stages" d="${svgPath(stagePoints, sx, sy)}"></path>
      <text x="${sx(result.xD)}" y="${sy(result.xD) - 8}">xD</text>
      <text x="${sx(result.xB) + 5}" y="${sy(result.xB) - 8}">xB</text>
      <text x="${sx(0.5)}" y="${height - 8}">x</text>
      <text x="10" y="${sy(0.5)}">y</text>
    </svg>
    <div class="plot-legend"><span>Equilibrium</span><span>Operating</span><span>Stages</span><span>q-line</span></div>
  `;
}

function renderEmptyPlot(message) {
  const target = document.querySelector("#mccabe-plot");
  target.className = "empty-plot";
  target.innerHTML = `<span>${escapeHtml(message)}</span>`;
}

resetButton.addEventListener("click", () => {
  form.reset();
  formError.textContent = "";
  updateDiagramLabels();
});

// Hosting status proves static delivery only; it does not imply an API connection.
fetch("build-info.json", { cache: "no-store" })
  .then((response) => {
    if (!response.ok) throw new Error("Build metadata unavailable");
    return response.json();
  })
  .then((info) => {
    const project = info.project;
    if (typeof project !== "string" || !/^[a-z0-9-]+$/.test(project) || !/^[a-f0-9]{64}$/.test(info.build_id)) return;
    document.querySelector("#build-status").textContent = `Project: ${project} · Build: ${info.build_id.slice(0, 12)} · DEMO`;
    if ([`${project}.web.app`, `${project}.firebaseapp.com`].includes(location.hostname)) {
      document.querySelector("#hosting-status").textContent = "Firebase connection OK · Static Hosting only";
    }
  })
  .catch(() => {});
