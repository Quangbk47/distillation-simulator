# Yêu cầu dữ liệu validation tối thiểu

Mục tiêu: xin một case chuẩn Ethanol-Water để kiểm tra kết quả Phase 3/4, không
tự bổ sung mô hình hoặc tự suy diễn số liệu từ ảnh minh họa.

## Thông tin cần xin GVHD/source

- Hệ cấu tử: Ethanol-Water.
- Mô hình hoặc giả thiết dùng để so: nếu có, ghi rõ Raoult + Antoine hay nguồn
  khác.
- Áp suất tháp và đơn vị.
- Thành phần feed ethanol và đơn vị.
- Lưu lượng feed.
- Trạng thái feed: q hoặc cách quy đổi sang q.
- Tỷ số hồi lưu R, định nghĩa R = L/D.
- Lưu lượng sản phẩm đỉnh D, nếu source có.
- Số mâm N và quy ước đếm mâm.
- Vị trí mâm feed NF và quy ước đếm từ trên hay dưới.
- Loại bình ngưng: total condenser hay partial condenser.
- Kết quả tham chiếu cần so:
  - xD ethanol.
  - xB ethanol.
  - recovery ethanol nếu có.
  - bảng mâm/nhiệt độ/thành phần nếu có.
- Citation/nguồn, ngày review và người duyệt.

## Tin nhắn ngắn có thể gửi thầy

> Em đã có local flow Ethanol-Water chạy được: input → Raoult + Antoine →
> xD/xB/recovery → bảng mâm → đồ thị McCabe-Thiele. Để hoàn tất validation,
> thầy cho em xin một case chuẩn có input và kết quả tham chiếu xD/xB được không
> ạ? Nếu có thêm bảng mâm/nhiệt độ theo mâm thì em sẽ dùng để kiểm tra sâu hơn.

## Nguyên tắc

- Không dùng ảnh UI làm số liệu validation.
- Không đổi contract partial condenser khi chưa được duyệt.
- Không claim `PASS` nếu chưa tính MAE thật từ case đã review.
