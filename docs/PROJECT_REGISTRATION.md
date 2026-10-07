# Project registration note

## Vietnamese registration title

**Xây dựng mô hình tính toán và mô phỏng quá trình chưng cất**

If the registration form needs a narrower title, use:

**Xây dựng mô hình tính toán và mô phỏng quá trình chưng cất nhị phân**

## Working interpretation

This repository implements a calculation and simulation tool for distillation.
The current approved scientific scope is intentionally narrow:

- Binary distillation.
- Ethanol-Water as the reviewed V1 chemical system.
- Raoult + Antoine VLE using reviewed NIST Chemistry WebBook SRD 69 Antoine
  records.
- Total condenser as the implemented condenser path.
- McCabe-Thiele calculation and visualization for the base simulation flow.

The wider registration title describes the research direction. It does not
authorize adding new chemical systems, thermodynamic models, partial-condenser
behavior, energy correlations or backend architecture before those items are
reviewed and approved.

## Current deliverables

- Reviewed Ethanol-Water Antoine provenance and runtime dataset.
- Local API calculation flow:
  input -> VLE -> xD/xB/recovery/D/B -> stage table -> McCabe-Thiele plot data.
- Web UI connected to the local engine.
- Controlled thermodynamic warning behavior, including
  `THERMO_EXTRAPOLATION` with component, actual temperature and source range.
- Validation request template for asking the supervisor for a reference case.

## Validation still needed

Before claiming scientific validation, a reviewed reference case is required:

- Input data: system, pressure, feed composition, flow, q, R, D, N, NF and
  condenser type.
- Reference outputs: xD, xB, recovery and, if available, tray/stage data.
- Source/citation, reviewer and review date.

The validation source must not be inferred from a UI screenshot.

## Suggested short description

Đề tài xây dựng mô hình tính toán và phần mềm mô phỏng quá trình chưng cất,
trước mắt triển khai cho hệ nhị phân Ethanol-Water. Mô hình sử dụng cân bằng
lỏng-hơi Raoult + Antoine với dữ liệu hệ số đã được duyệt, tính các kết quả
cơ bản như thành phần sản phẩm đỉnh/đáy, độ thu hồi, bảng mâm và đồ thị
McCabe-Thiele. Các phần mở rộng như hệ cấu tử khác, partial condenser và cân
bằng năng lượng chỉ thực hiện sau khi có dữ liệu và quyết định khoa học được
duyệt.
