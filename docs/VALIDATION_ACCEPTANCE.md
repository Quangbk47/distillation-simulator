# Validation acceptance decision

Ngày quyết định: 2026-09-18.

Để hoàn tất phần còn bỏ ngỏ của câu 10A, dự án chấp nhận cấu hình validation V1 sau:

```text
validation_primary_metric = MAE_xD_xB_percentage_points
validation_acceptance_threshold_pct = 5
```

`MAE_xD_xB_percentage_points` là mean absolute error của các giá trị `xD` và `xB` so với dataset tham chiếu, biểu diễn theo điểm phần trăm. Ví dụ sai số thành phần `0.03` tương đương `3` điểm phần trăm. Validation PASS khi MAE của dataset không vượt quá `5` điểm phần trăm.

Ngưỡng này không thay thế các gate kỹ thuật: residual cân bằng tổng/cấu tử và residual solver vẫn phải nhỏ hơn `1e-4`. Không được tuyên bố một dataset PASS nếu citation, điều kiện mapping hoặc dữ liệu nguồn chưa được review đầy đủ.

Tài liệu `EXPERT_CONFIRMATION.md` và phiếu ký trong `docs/archive/` giữ nguyên nội dung xác nhận ban đầu, trong đó câu 10A chưa có con số. File này là quyết định cập nhật của dự án sau đó.
