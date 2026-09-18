# Contributing

Đọc `README.md` và các tài liệu trong `docs/` trước khi thay đổi engine. Giữ engine khoa học độc lập với API/UI, không hard-code số mô phỏng và không đưa Wilson vào runtime V1.

Mọi thay đổi thermo/enthalpy/validation phải kèm provenance, test regression và ghi chú trong `docs/PROGRESS.md`. Không tự điền metric hoặc threshold của câu 10A; dùng `PENDING_EXPERT_THRESHOLD` cho đến khi được xác nhận.

Trước khi mở pull request, chạy toàn bộ lệnh kiểm tra trong README. PR vào `main` phải qua CI và review phù hợp; thay đổi khoa học cần scientific lead review.
