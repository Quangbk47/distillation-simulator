const tabs = document.querySelectorAll("[data-tab]");
const panels = document.querySelectorAll("[data-panel]");
const form = document.querySelector("#simulation-form");
const formError = document.querySelector("#form-error");
const resetButton = document.querySelector("#reset-button");

function selectTab(name) {
  tabs.forEach((tab) => tab.classList.toggle("is-active", tab.dataset.tab === name));
  panels.forEach((panel) => panel.classList.toggle("is-active", panel.dataset.panel === name));
}

tabs.forEach((tab) => tab.addEventListener("click", () => selectTab(tab.dataset.tab)));

function numberValue(name) {
  return Number(form.elements[name].value);
}

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
  document.querySelector("#result-status").textContent = "NOT CALCULATED";
  document.querySelector("#connection-status").textContent = "ENGINE NOT CONNECTED";
  document.querySelector("#warning-text").textContent = "Backend/API chưa được kết nối; không có kết quả khoa học.";
});

resetButton.addEventListener("click", () => {
  form.reset();
  formError.textContent = "";
});

// Hosting status proves static delivery only; it does not imply an API connection.
fetch("build-info.json", { cache: "no-store" })
  .then((response) => {
    if (!response.ok) throw new Error("Build metadata unavailable");
    return response.json();
  })
  .then((info) => {
    const project = "distillation-simulator";
    if (info.project !== project || !/^[a-f0-9]{64}$/.test(info.build_id)) return;
    document.querySelector("#build-status").textContent = `Project: ${project} · Build: ${info.build_id.slice(0, 12)} · DEMO`;
    if ([`${project}.web.app`, `${project}.firebaseapp.com`].includes(location.hostname)) {
      document.querySelector("#hosting-status").textContent = "Firebase connection OK · Static Hosting only";
    }
  })
  .catch(() => {});
