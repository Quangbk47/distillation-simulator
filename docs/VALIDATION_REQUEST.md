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

## Candidate case đã nhập từ form GVHD

Các giá trị từ form minh họa/GVHD đã được nhập vào
`data/validation/cases/ethanol-water.pending.json` để chờ review:

- Ethanol-Water, P = 1 bar, zF ethanol = 50 mol%, F = 100 kmol/h.
- q = 1, R = 2, D = 45.2 kmol/h, N = 20, NF = 10, total condenser.
- xD ethanol = 95.0 mol%.
- Độ tinh khiết đáy 94.8 mol% được hiểu theo hướng hợp lý là water-rich
  bottoms, nên map thành xB ethanol = 5.2 mol%.
- Recovery ethanol = 90.4%.

Khi chạy engine hiện tại, candidate này chưa hội tụ (`NON_CONVERGED`), nên vẫn
cần thầy xác nhận lại quy ước số mâm, D, NF và ý nghĩa độ tinh khiết đáy trước
khi claim validation PASS.

## Điểm cần hỏi lại thầy sau khi kiểm tra cân bằng vật chất

Nếu hiểu hợp lý rằng đáy giàu nước, tức `xB_ethanol = 1 - 0.948 = 0.052`, thì
các số trong form chưa tự khớp cân bằng vật chất ethanol:

- Với `F = 100`, `zF = 0.50`, `xD = 0.95`, `xB_ethanol = 0.052`, cân bằng yêu
  cầu `D ≈ 49.89 kmol/h`, không phải `45.2 kmol/h`.
- Nếu giữ `D = 45.2 kmol/h` và `xD = 0.95`, cân bằng cho `xB_ethanol ≈ 0.1288`,
  tức đáy khoảng 87.12 mol% water, không phải 94.8 mol% water.
- Nếu giữ `recovery = 90.4%` và `xD = 0.95`, cân bằng cho `D ≈ 47.58 kmol/h`.

Câu hỏi ngắn cần xác nhận: trong form này, `D`, `xD`, độ tinh khiết đáy và
recovery có phải là số liệu minh họa giao diện không, hay là một case chuẩn đã
cân bằng? Nếu là case chuẩn, thầy cho biết giá trị nào là giá trị chính xác để
em dùng làm validation.
