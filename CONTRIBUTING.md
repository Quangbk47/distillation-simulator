# Contributing

Đọc `README.md` và các tài liệu trong `docs/` trước khi thay đổi engine. Giữ engine khoa học độc lập với API/UI, không hard-code số mô phỏng và không đưa Wilson vào runtime V1.

Mọi thay đổi thermo/enthalpy/validation phải kèm provenance, test regression và ghi chú trong `docs/PROGRESS.md`. Metric và threshold validation V1 hiện hành là `MAE_xD_xB_percentage_points` và `5` điểm phần trăm; nếu thay đổi phải cập nhật `docs/VALIDATION_ACCEPTANCE.md` cùng test liên quan.

Trước khi mở pull request, chạy toàn bộ lệnh kiểm tra trong README. Sinh viên
có thể tự thực hiện toàn bộ workflow kỹ thuật mà không cần chờ Owner duyệt từng
Phase. PR vào `main` vẫn phải qua CI và review phù hợp; thay đổi khoa học cần
scientific lead review. Sau khi merge, phải deploy artifact phù hợp, smoke test
và cập nhật evidence trước khi coi checkpoint/release là hoàn tất.
