# Expert Decisions Final

Nguồn quyết định chuyên môn gốc là `EXPERT_CONFIRMATION.md`; quyết định
validation cập nhật là `VALIDATION_ACCEPTANCE.md`. Các quyết định lịch sử trong
`docs/archive/` không override các file này.

V1 dùng Raoult + Antoine làm model runtime chính; Wilson không chạy runtime.
Nhóm được chọn nguồn dữ liệu nhưng phải có provenance/reviewer. Ngoại suy được
phép với warning. `N` là body stages; total và partial condenser thuộc V1; q
nhập trực tiếp; QC/QR dùng enthalpy đơn giản; heat loss là kW tuyệt đối;
success cần các balance/outer/solver residual gates `<1e-4`; validation dùng literature/dataset;
production là web app có backend/API.

Các chi tiết cần code được khóa trong `PROCESS_MODEL.md`, đặc biệt outer solve
cho xD/xB và NF consistency. Partial-condenser equations vẫn OPEN/BLOCKING vì
phiếu quyết định chưa đủ để xác định duy nhất phase/product convention,
equilibrium stage, flow equations và golden case. Không tự bịa phần này.
