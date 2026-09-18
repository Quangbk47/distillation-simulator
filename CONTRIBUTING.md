# Contributing

Đọc `README.md` và các tài liệu trong `docs/` trước khi thay đổi engine. Giữ engine khoa học độc lập với API/UI, không hard-code số mô phỏng và không đưa Wilson vào runtime V1.

Mọi thay đổi thermo/enthalpy/validation phải kèm provenance, test regression và ghi chú trong `docs/PROGRESS.md`. Metric và threshold validation V1 hiện hành là `MAE_xD_xB_percentage_points` và `5` điểm phần trăm; nếu thay đổi phải cập nhật `docs/VALIDATION_ACCEPTANCE.md` cùng test liên quan.

Trước khi mở pull request, chạy toàn bộ lệnh kiểm tra trong README. PR vào `main` phải qua CI và review phù hợp; thay đổi khoa học cần scientific lead review.
