# Expert Decisions Final

Nguồn chuẩn mới: `EXPERT_CONFIRMATION.md`. Các quyết định trước đây chỉ còn giá trị lịch sử khi mâu thuẫn với xác nhận này.

V1 dùng Raoult + Antoine làm mô hình kết quả chính; Wilson không dùng để tạo kết quả chính. Nhóm được phép chọn nguồn dữ liệu nhưng phải review provenance. Ngoại suy dữ liệu nhiệt động được phép khi có warning. N là số mâm thân tháp. Total và partial condenser đều thuộc V1. q được nhập trực tiếp. QC/QR dùng enthalpy đơn giản; heat loss nhập tuyệt đối kW. Thành công cần đồng thời đạt residual balance và solver <1e-4. Validation dùng dataset/bài báo nếu chưa có thí nghiệm. Kiến trúc production là web app có backend/API.
