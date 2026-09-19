# Handover

Đọc `README.md`, `PROJECT_AUDIT.md`, `PROJECT_RULES.md`,
`EXPERT_DECISIONS.md`, `ALGORITHM_SPEC.md`, `CALCULATION_FORMULAS.md` và
`PROGRESS.md`. Phiếu trong `docs/archive/` chỉ là lịch sử. Không đổi giả thiết
chuyên môn mà không cập nhật source-of-truth, calculation contract, tests và
version.

Roadmap hiện hành là `docs/ROADMAP.md`: bắt đầu Phase 0/1, kết nối Firebase
Hosting sớm ở Phase 2, chạy Calculation Closure Gate trước Phase 4, deploy lại
ở Phase 5 và production ở Phase 10. Firebase Hosting chỉ host frontend/static
assets; backend Python phải có runtime riêng.

Total-condenser closure đã được document: outer unknown là `xD`, `xB` suy ra
từ balance, bottom residual là `y_N-y_eq(xB,P)`, và `NF` mismatch trả
`INCONSISTENT_FEED_STAGE`. Partial condenser vẫn OPEN/BLOCKING và phải trả
`NOT_IMPLEMENTED`; enthalpy review chỉ chặn Phase 6.

Nếu gặp login Firebase/GitHub hoặc thao tác deployment ảnh hưởng tài khoản,
dừng tại bước đó và yêu cầu chủ repo đăng nhập/xác nhận. Không tự tạo project,
không lưu credential, không force-push.
