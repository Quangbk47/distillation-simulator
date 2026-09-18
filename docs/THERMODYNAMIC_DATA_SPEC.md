# Thermodynamic Data Specification Final

Nguồn Antoine do nhóm chọn, nhưng mỗi record bắt buộc: component, A/B/C, công thức/unit, temperature range, pressure unit, URL/citation, publication/version, reviewer, review date. Raoult + Antoine là model duy nhất tạo kết quả V1.

Ngoài miền T: cho phép extrapolation, gắn `THERMO_EXTRAPOLATION`, lưu `isExtrapolated=true`, source range và actual T trong result/log. Không extrapolate nếu Psat không dương, equilibrium không vật lý hoặc coefficient thiếu provenance. Wilson không phải feature V1; chỉ lưu hướng mở rộng, không expose qua API/UI.
