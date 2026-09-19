# Expert Confirmation Final

Ngày chốt: 2026-09-18. Trả lời của Anh Đại: 1A, 2C, 3B, 4A, 5B, 6A, 7A, 8C, 9C, 10A, 11B, 12C, 13B.

| Câu | Quyết định triển khai |
|---|---|
| 1 | VLE kết quả chính V1: Raoult + Antoine |
| 2 | Nhóm chọn nguồn Antoine/Wilson, bắt buộc có citation, đơn vị, miền áp dụng và GVHD duyệt |
| 3 | Ngoài miền dữ liệu: cho ngoại suy nhưng phải cảnh báo rõ trong kết quả/log |
| 4 | N chỉ đếm mâm lý thuyết trong thân tháp; condenser/reboiler không tính vào N |
| 5 | Hỗ trợ total và partial condenser; phải có test cả hai |
| 6 | Người dùng nhập trực tiếp q-value |
| 7 | QC/QR dùng mô hình enthalpy đơn giản, Cp và ẩn nhiệt có nguồn rõ |
| 8 | Tổn thất nhiệt là giá trị tải nhiệt tuyệt đối do người dùng nhập, đơn vị kW |
| 9 | Thành công khi residual cân bằng tổng/cấu tử và residual solver đều < 1e-4 |
| 10 | Validation phải có ngưỡng pass/fail; số % và chỉ tiêu cụ thể chưa được điền trong câu trả lời |
| 11 | Chưa chọn hệ thứ hai; chỉ hoàn thành Ethanol-Water trước |
| 12 | Validation dùng dataset/bài báo khi chưa có thí nghiệm |
| 13 | Deploy web app có backend/API cho engine/dữ liệu |

## Một trường cần điền cuối
`validation_acceptance_threshold_pct` và `validation_primary_metric` phải được GVHD/Anh Đại ghi rõ trước khi tuyên bố validation PASS/FAIL. Không tự gán giá trị số.

**Lịch sử quyết định:** nội dung trên ghi lại phiếu xác nhận ngày 2026-09-18.
Sau đó, `docs/VALIDATION_ACCEPTANCE.md` đã ghi quyết định cập nhật cho riêng
metric/ngưỡng validation: `MAE_xD_xB_percentage_points`, threshold `5` điểm
phần trăm. Không dùng dòng lịch sử này để mở lại quyết định đã cập nhật.
