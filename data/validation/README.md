# Validation data

Validation cases phải lưu citation đầy đủ, loại nguồn, điều kiện gốc, mapping
input/units, observed values và assumptions. Nguồn literature/dataset được phép
ở giai đoạn hiện tại. V1 dùng MAE của xD/xB theo điểm phần trăm với ngưỡng `5`;
không được gắn nhãn PASS khi case chưa được review và đánh giá.

Schema nằm tại `schema.json`. Case mẫu pending nằm tại `cases/ethanol-water.pending.json`.

## Quy trình tối thiểu cho case chuẩn

1. Xin GVHD/source cung cấp một case Ethanol-Water có đủ input và kết quả tham
   chiếu.
2. Điền `sourceCitation`, `sourceConditions`, `mappedInput` và `observed` trong
   `cases/ethanol-water.pending.json`.
3. Chỉ đổi `validationAcceptance.status` sang `EVALUATED` sau khi đã chạy engine
   và tính MAE thật.
4. Không tự suy diễn xD/xB hoặc số mâm từ ảnh minh họa UI; ảnh giao diện chỉ là
   tham khảo trình bày, không phải dữ liệu validation.
