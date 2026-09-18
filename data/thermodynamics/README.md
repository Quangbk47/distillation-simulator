# Thermodynamic data

Đây là nơi lưu dữ liệu Antoine đã review cho Raoult + Antoine. Mỗi record phải có component, hệ số A/B/C, công thức/đơn vị, miền nhiệt độ, đơn vị áp suất, citation/URL, publication/version, reviewer và review date.

Hiện chưa có record số nào được chuyên gia review. File `antoine_ethanol_water.pending.json` là placeholder có chủ ý; không dùng làm dữ liệu mô phỏng. Schema nằm tại `schema.json`.

Ngoài miền nhiệt độ cho phép ngoại suy nhưng phải ghi `THERMO_EXTRAPOLATION`, `isExtrapolated`, source range và actual temperature. Không chấp nhận Psat không dương, equilibrium phi vật lý hoặc coefficient thiếu provenance.
