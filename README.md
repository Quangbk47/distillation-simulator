# Distillation Simulator

Khung nền cho mô phỏng chưng cất nhị phân Ethanol–Water ở trạng thái ổn định, phục vụ học tập, nghiên cứu và validation. V1 không nhằm trở thành bản thu nhỏ của Aspen/HYSYS.

## Phạm vi V1

- Hệ nhị phân Ethanol–Water, steady-state, áp suất không đổi.
- Cân bằng hơi–lỏng chính: Raoult + Antoine.
- Phương pháp tháp: McCabe–Thiele.
- Người dùng nhập trực tiếp `q`; `N` chỉ đếm số mâm trong thân tháp.
- Hỗ trợ đường chạy total condenser. Partial condenser vẫn trả
  `NOT_IMPLEMENTED` cho tới khi GVHD chốt công thức/reference case.
- `QC`/`QR` để pending trong Phase 3/4; Phase 6 chỉ được bật sau khi có dữ liệu
  Cp/ẩn nhiệt và quy ước dấu được review.
- Tổn thất nhiệt là tải nhiệt tuyệt đối `heatLoss_kW`.
- Kết quả chỉ thành công khi residual cân bằng tổng, residual cân bằng cấu tử, residual outer và residual solver đều `< 1e-4`.
- Ngoại suy dữ liệu nhiệt động được phép nhưng phải trả warning `THERMO_EXTRAPOLATION`, nêu nhiệt độ thực tế và miền nguồn.
- Kiến trúc production: web client → backend/API → engine và data repository.

Ngoài V1: optimization, AI/ML, dynamic simulation, thủy lực mâm chi tiết, dashboard phức tạp và Wilson trong đường chạy runtime. Validation V1 dùng MAE của `xD/xB` theo điểm phần trăm, ngưỡng chấp nhận là `5`; quyết định được ghi tại [`docs/VALIDATION_ACCEPTANCE.md`](docs/VALIDATION_ACCEPTANCE.md).

## Logic chuyên môn đã chốt

Nguồn chuẩn là [`docs/EXPERT_CONFIRMATION.md`](docs/EXPERT_CONFIRMATION.md) và [`docs/PROJECT_RULES.md`](docs/PROJECT_RULES.md); quyết định metric/ngưỡng validation mới nhất nằm trong [`docs/VALIDATION_ACCEPTANCE.md`](docs/VALIDATION_ACCEPTANCE.md). Các contract chi tiết nằm trong [`docs/PROCESS_MODEL.md`](docs/PROCESS_MODEL.md), [`docs/ALGORITHM_SPEC.md`](docs/ALGORITHM_SPEC.md), [`docs/CALCULATION_FORMULAS.md`](docs/CALCULATION_FORMULAS.md), [`docs/DATA_MODEL.md`](docs/DATA_MODEL.md) và [`docs/SOFTWARE_ARCHITECTURE.md`](docs/SOFTWARE_ARCHITECTURE.md). Dữ liệu Antoine/enthalpy chưa được coi là reviewed cho đến khi có citation, miền áp dụng, reviewer và ngày review.

Hiện tại bộ Antoine Ethanol–Water NIST SRD 69 đã được GVHD/Anh Đại review ngày
2026-10-04 và nằm tại
[`data/thermodynamics/antoine_ethanol_water.json`](data/thermodynamics/antoine_ethanol_water.json).
Validation khoa học vẫn cần một golden/reference case được GVHD xác nhận.

Audit và execution roadmap nằm trong [`docs/PROJECT_AUDIT.md`](docs/PROJECT_AUDIT.md) và [`docs/ROADMAP.md`](docs/ROADMAP.md). Firebase Hosting chỉ host frontend/static assets; backend Python cần runtime riêng. Nhóm sinh viên có thể dùng hoặc tự tạo Firebase project/site của mình, rồi cập nhật `.firebaserc`/`firebase.json` và ghi URL production thực tế theo deployment runbook.

Quy tắc vận hành team nằm trong [`docs/PROJECT_RULES.md`](docs/PROJECT_RULES.md): **NO WORK IS COMPLETE UNTIL PROGRESS IS UPDATED.** Mỗi checkpoint kỹ thuật theo chuỗi `READ CURRENT STATE → IMPLEMENT → TEST → UPDATE DOCS → COMMIT/PUSH → PR → CI/REVIEW → MERGE MAIN → BUILD PRODUCTION → DEPLOY FIREBASE HOSTING → PRODUCTION SMOKE TEST → UPDATE EVIDENCE → CLOSE PHASE IF DoD PASSES → CONTINUE NEXT PHASE`. Sinh viên tự chủ toàn bộ phần kỹ thuật, gồm Firebase; chỉ dừng khi thiếu một quyết định khoa học mới chưa được chốt. `PROGRESS.md` là nguồn trạng thái hiện tại, `TODO.md` là danh sách việc còn lại và `ROADMAP.md` là kế hoạch.

## Cấu trúc repository

```text
docs/                         Quyết định, spec, kế hoạch và tài liệu gốc đã nhập
data/
  thermodynamics/             Schema và record Antoine có provenance
  validation/                 Schema/case validation, không tự tuyên bố PASS
src/
  thermodynamics/             Raoult–Antoine và contract dữ liệu nhiệt động
  distillation/               McCabe–Thiele, condenser và energy contracts
  solver/                     Residual/convergence gates
  sensitivity/                Khung khảo sát đúng một biến R/N/NF
  api/                        Backend/API contract và FastAPI app skeleton
  ui/                         Boundary notes cho web client
web/                          Static V1 UI shell, không phụ thuộc framework
tests/
  unit/                       Unit tests cho contract và logic nhỏ
  integration/                API/engine boundary tests
  reference/                  Data/schema/provenance checks
  validation/                 Tests giữ trạng thái pending của validation
.github/workflows/            CI lint, type-check, test, build, secret scan
```

## Thứ tự đọc tài liệu

1. [`docs/EXPERT_CONFIRMATION.md`](docs/EXPERT_CONFIRMATION.md)
2. [`docs/PROJECT_RULES.md`](docs/PROJECT_RULES.md)
3. [`docs/PROCESS_MODEL.md`](docs/PROCESS_MODEL.md)
4. [`docs/ALGORITHM_SPEC.md`](docs/ALGORITHM_SPEC.md)
5. [`docs/DATA_MODEL.md`](docs/DATA_MODEL.md)
6. [`docs/SOFTWARE_ARCHITECTURE.md`](docs/SOFTWARE_ARCHITECTURE.md)
7. [`docs/UI_UX_SPEC.md`](docs/UI_UX_SPEC.md)
8. [`docs/TEST_CASES.md`](docs/TEST_CASES.md)
9. [`docs/VALIDATION_ACCEPTANCE.md`](docs/VALIDATION_ACCEPTANCE.md)
10. [`docs/PROJECT_AUDIT.md`](docs/PROJECT_AUDIT.md)
11. [`docs/ROADMAP.md`](docs/ROADMAP.md) và [`docs/TODO.md`](docs/TODO.md)

Calculation closure: in the total-condenser branch, `xD` is the scalar outer
unknown, `xB` is derived from material balance, and the root residual closes
the equilibrium reboiler boundary after exactly `N` body stages. `NF` is never
silently changed; it directly controls the section switch. Q-line geometry is
diagnostic only in V1.
Partial condenser is a V1 deliverable but remains `NOT_IMPLEMENTED` until its
scientific formulation is approved. Enthalpy review blocks only Phase 6, not
the Phase 3/4 VLE/stage work.

Các file markdown, DOCX và hình ảnh đã copy ban đầu được giữ trong [`docs/archive/`](docs/archive/) hoặc [`docs/assets/`](docs/assets/); không file nào bị xóa vì nghi là trùng lặp.

## Phát triển local

Yêu cầu Python 3.11+:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
python -m uvicorn api.app:app --app-dir src --reload --host 127.0.0.1 --port 8000
```

Sau đó mở:

```text
http://127.0.0.1:8000/
```

Giữ cửa sổ terminal chạy Uvicorn mở trong lúc dùng web local. Nếu trình duyệt
báo `ERR_CONNECTION_REFUSED`, nghĩa là backend chưa chạy hoặc terminal đã bị
tắt.

Nếu trình duyệt hiện `{"detail":"Not Found"}`:

- Kiểm tra URL phải là `http://127.0.0.1:8000/`, có dấu `/` cuối, không phải
  route API cũ hoặc tab bị cache.
- Bấm `Ctrl + F5` để hard refresh.
- Nếu vẫn lỗi, chạy lại `python scripts/build_frontend.py` rồi khởi động lại
  Uvicorn bằng lệnh phía trên.

Nếu chỉ cần build static bundle để deploy Hosting:

```powershell
python scripts/build_frontend.py
python -m http.server 5173 --directory build/frontend
```

API có `/health`, `/api/thermo-data/version`, `/api/simulations` và
`/api/sensitivity`. Local FastAPI tại `127.0.0.1:8000` phục vụ cả frontend và
backend tính toán. Firebase Hosting hiện chỉ phục vụ static assets; production
backend cần runtime riêng trước Phase 10.

## Kiểm tra

```powershell
python scripts/run_quality.py
```

Hoặc chạy từng bước:

```powershell
python -m ruff check .
python -m mypy src
python -m pytest --basetemp work/pytest-tmp -p no:cacheprovider
python scripts/smoke_local_api.py
python scripts/check_structure.py
python scripts/build_frontend.py
python -m build
python -m detect_secrets scan --force-use-all-plugins src tests data scripts .github pyproject.toml .env.example
```

Mỗi thay đổi model/dữ liệu khoa học cần cập nhật provenance, test regression và review của scientific lead. Không commit secret; dùng `.env.example` làm danh sách biến môi trường không nhạy cảm.
