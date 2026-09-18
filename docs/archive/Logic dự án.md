# LOGIC DỰ ÁN MÔ PHỎNG CHƯNG CẤT

**Tên tệp:** Logic dự án.md\
**Vai trò:** Tài liệu logic lõi dùng làm nguồn chuẩn để viết tài liệu dự
án và triển khai phần mềm về sau.\
**Cơ sở chốt:** Phiếu trả lời của chuyên gia Quá trình -- Thiết bị / Máy
hóa (Anh Đại):\
**1A, 2A, 3B, 4A, 5B, 6B, 7C, 8C, 9A, 10A, 11B, 12A, 13A, 14A, 15A, 16C,
17B, 18D, 19C, 20A.**

> **Nguyên tắc:** Tài liệu này ghi lại đúng các lựa chọn đã được chốt.
> Không tự mở rộng phạm vi hoặc thay thế phương pháp nếu chưa có quyết
> định mới của GVHD/chuyên gia.

------------------------------------------------------------------------

## 1. Mục tiêu của phiên bản V1

Xây dựng một phần mềm **mô phỏng chưng cất hệ nhị phân ở trạng thái ổn
định**, đủ đơn giản để sinh viên có thể triển khai nhưng vẫn có logic
chuyên môn rõ ràng, có khả năng chạy mô phỏng, khảo sát ảnh hưởng của
các thông số vận hành và kiểm chứng bằng dữ liệu thực nghiệm.

V1 không đặt mục tiêu trở thành phần mềm mô phỏng quá trình tổng quát
như Aspen Plus/HYSYS.

Mục tiêu trước mắt là:

-   xây dựng và chạy ổn định mô hình chưng cất nhị phân;
-   sử dụng **Ethanol -- Water** làm hệ chất đầu tiên;
-   triển khai phương pháp tính đã được chuyên gia chốt;
-   tính được các đại lượng sản phẩm và năng lượng chính;
-   khảo sát ảnh hưởng của một số thông số vận hành;
-   kiểm chứng kết quả bằng dữ liệu thực nghiệm;
-   chưa thực hiện bài toán tối ưu hóa ở V1.

------------------------------------------------------------------------

## 2. Phạm vi mô hình

### 2.1. Loại hệ

-   Hệ **nhị phân**.
-   Trạng thái **ổn định (steady-state)**.
-   Hệ chất đầu tiên: **Ethanol -- Water**.
-   Giai đoạn đầu **chưa cần hệ chất thứ hai**, ưu tiên làm chắc một hệ
    trước.

### 2.2. Phương pháp mô phỏng tháp

Phương pháp được chọn cho V1:

**McCabe -- Thiele cho hệ nhị phân.**

Đây là phương pháp lõi dùng để mô tả và tính toán quá trình phân riêng
trong tháp ở V1.

### 2.3. Áp suất tháp

Giả thiết:

**Áp suất không đổi trong toàn tháp.**

V1 không yêu cầu tính sụt áp theo chiều cao tháp hoặc tính thủy lực mâm
chi tiết.

------------------------------------------------------------------------

## 3. Cân bằng hơi -- lỏng và nhiệt động

### 3.1. Mô hình cân bằng hơi -- lỏng cơ sở

Lựa chọn đã chốt:

**Raoult + phương trình Antoine.**

Trong đó:

-   phương trình Antoine dùng để xác định áp suất hơi bão hòa;
-   định luật Raoult được sử dụng trong mô hình cân bằng hơi -- lỏng cơ
    sở.

### 3.2. Hệ số hoạt độ

Trong trường hợp sử dụng mô hình có hiệu chỉnh hệ số hoạt độ cho hệ
không lý tưởng, lựa chọn đã chốt là:

**Wilson.**

### 3.3. Quy tắc triển khai

Hai lựa chọn trên phải được giữ trong tài liệu dự án đúng theo phiếu
chuyên gia:

-   mô hình VLE cơ sở: **Raoult + Antoine**;
-   khi sử dụng hệ số hoạt độ: **Wilson**.

Việc quyết định chính xác Wilson được kích hoạt ở chế độ nào, dữ liệu
tham số Wilson lấy từ đâu và cách ghép Wilson với mô hình VLE cần được
đặc tả ở bước thiết kế thuật toán/dữ liệu, nếu dự án triển khai phần
này.

------------------------------------------------------------------------

## 4. Dòng nhập liệu

Trạng thái nhiệt của dòng nhập liệu được mô tả bằng:

**q-value.**

Do đó dữ liệu đầu vào của mô hình cần có khả năng xác định hoặc cho phép
nhập giá trị `q`.

Các thông tin cơ bản của dòng nhập liệu dự kiến gồm:

-   lưu lượng nguyên liệu `F`;
-   thành phần nguyên liệu `zF`;
-   trạng thái nhiệt thông qua `q`;
-   áp suất làm việc.

Các đại lượng bổ sung chỉ đưa vào khi cần cho thuật toán đã được chốt.

------------------------------------------------------------------------

## 5. Cấu hình tháp

Các thông số cấu hình chính gồm:

-   số mâm;
-   vị trí mâm nhập liệu;
-   hiệu suất mâm;
-   loại bình ngưng;
-   mô hình nồi đun đáy.

### 5.1. Bình ngưng

Phần mềm cho phép lựa chọn:

1.  **ngưng tụ toàn phần (Total condenser)**;
2.  **ngưng tụ một phần (Partial condenser)**.

### 5.2. Nồi đun đáy

Nồi đun đáy được mô hình hóa:

**đơn giản theo tải nhiệt.**

Không đặt yêu cầu xây dựng mô hình reboiler phức tạp ở V1.

### 5.3. Hiệu suất mâm

Theo lựa chọn 10A:

**Mâm lý thuyết 100%.**

Do đó V1 mặc định sử dụng mâm lý thuyết, không bắt buộc triển khai hiệu
suất Murphree hoặc cho người dùng nhập hiệu suất mâm.

### 5.4. Tổn thất nhiệt

Theo lựa chọn 11B:

**Cho phép nhập hệ số hoặc tỷ lệ tổn thất nhiệt.**

Logic triển khai cần có biến đầu vào thể hiện mức tổn thất nhiệt. Công
thức cụ thể để đưa tổn thất này vào cân bằng năng lượng cần được định
nghĩa trong đặc tả thuật toán trước khi code.

------------------------------------------------------------------------

## 6. Điều kiện vận hành chính

Cặp biến vận hành chính đã được chốt là:

-   **Tỷ số hồi lưu `R`**;
-   **Lưu lượng sản phẩm đỉnh `D`**.

Trong đó:

`R = L / D`

với:

-   `L`: lưu lượng dòng hồi lưu;
-   `D`: lưu lượng sản phẩm đỉnh.

Đây là cặp biến vận hành chính dùng để xác định bài toán mô phỏng V1.

------------------------------------------------------------------------

## 7. Đầu vào lõi của phần mềm

Từ các quyết định đã chốt, bộ đầu vào tối thiểu cần xem xét khi xây dựng
phần mềm gồm:

### Dòng nguyên liệu

-   hệ cấu tử: Ethanol -- Water;
-   lưu lượng nguyên liệu `F`;
-   thành phần nguyên liệu `zF`;
-   `q-value`;
-   áp suất.

### Cấu hình tháp

-   số mâm;
-   vị trí mâm nhập liệu;
-   lựa chọn loại bình ngưng;
-   mâm lý thuyết 100%;
-   thông số/tỷ lệ tổn thất nhiệt.

### Điều kiện vận hành

-   tỷ số hồi lưu `R`;
-   lưu lượng sản phẩm đỉnh `D`.

### Nhiệt động

-   Antoine;
-   Raoult;
-   Wilson khi áp dụng hiệu chỉnh hệ số hoạt độ.

------------------------------------------------------------------------

## 8. Kết quả bắt buộc

Theo lựa chọn 14A, phần mềm phải xuất tối thiểu:

-   `xD`: thành phần/độ tinh khiết sản phẩm đỉnh;
-   `xB`: thành phần/độ tinh khiết sản phẩm đáy;
-   `D`: lưu lượng sản phẩm đỉnh;
-   `B`: lưu lượng sản phẩm đáy;
-   `Recovery`: độ thu hồi cấu tử mục tiêu;
-   `QC`: tải nhiệt bình ngưng;
-   `QR`: tải nhiệt nồi đun đáy.

Đây là **bộ kết quả bắt buộc của V1**.

Các profile nhiệt độ, thành phần, lưu lượng lỏng/hơi theo từng mâm không
được xem là đầu ra bắt buộc theo phiếu đã chốt. Chỉ bổ sung nếu sau này
cần cho phương pháp hoặc mục tiêu trình bày.

------------------------------------------------------------------------

## 9. Logic cân bằng vật chất cơ bản

Phần mềm phải bảo đảm cân bằng vật chất tổng thể:

`F = D + B`

Đối với từng cấu tử, phải bảo đảm cân bằng cấu tử tương ứng giữa:

-   dòng nguyên liệu;
-   sản phẩm đỉnh;
-   sản phẩm đáy.

Các kết quả không thỏa mãn điều kiện cân bằng trong giới hạn sai số cho
phép không được coi là kết quả mô phỏng hợp lệ.

------------------------------------------------------------------------

## 10. Logic McCabe -- Thiele

Phần lõi V1 phải tổ chức được chuỗi tính toán phù hợp với phương pháp
McCabe -- Thiele cho hệ nhị phân, bao gồm tối thiểu:

1.  nhận dữ liệu hệ và điều kiện vận hành;
2.  xây dựng quan hệ cân bằng hơi -- lỏng;
3.  xác định đường chéo `y = x`;
4.  xác định đường vận hành đoạn luyện;
5.  xác định q-line của dòng nhập liệu;
6.  xác định đường vận hành đoạn chưng;
7.  thực hiện bước mâm theo McCabe -- Thiele;
8.  xác định/đánh giá số mâm và vị trí nhập liệu theo bài toán;
9.  tính các đại lượng sản phẩm;
10. tính/ước lượng các đại lượng năng lượng cần thiết theo mô hình V1;
11. kiểm tra sai số;
12. trả kết quả hoặc thông báo trường hợp không tính được.

Chi tiết phương trình và thuật toán số sẽ được viết trong **đặc tả thuật
toán** dựa trên logic lõi này.

------------------------------------------------------------------------

## 11. Khảo sát độ nhạy

V1 phải cho phép khảo sát ảnh hưởng của ba biến:

1.  **Tỷ số hồi lưu `R`;**
2.  **Số mâm;**
3.  **Vị trí mâm nhập liệu.**

Nguyên tắc khảo sát:

-   thay đổi một biến trong một khoảng xác định;
-   giữ các điều kiện còn lại theo case cơ sở;
-   chạy lại mô hình;
-   lưu kết quả;
-   so sánh ảnh hưởng lên các đầu ra chính.

Tối thiểu phải có khả năng tạo bảng hoặc dữ liệu phục vụ vẽ đồ thị khảo
sát.

V1 **không bắt buộc** khảo sát áp suất hoặc reboiler duty như biến độc
lập.

------------------------------------------------------------------------

## 12. Tiêu chí hội tụ/sai số

Ngưỡng đã được chốt:

**Sai số \< 10⁻⁴.**

Bộ giải phải có cơ chế:

-   tính sai số;
-   xác định đạt/không đạt ngưỡng;
-   không báo "thành công" nếu điều kiện sai số chưa thỏa mãn.

Định nghĩa chính xác residual nào được dùng để đánh giá ngưỡng `10⁻⁴`
cần được ghi rõ trong đặc tả thuật toán khi triển khai.

------------------------------------------------------------------------

## 13. Kiểm chứng mô hình

Phương pháp kiểm chứng được chọn:

**Dữ liệu thực nghiệm.**

Do đó dự án cần chuẩn bị ít nhất một bộ dữ liệu thực nghiệm phù hợp với
hệ Ethanol -- Water và miền điều kiện đang mô phỏng.

Quy trình validation dự kiến:

**Dữ liệu đầu vào thực nghiệm → chạy mô phỏng → lấy kết quả → đối chiếu
dữ liệu thực nghiệm → tính sai lệch → nhận xét.**

Dữ liệu kiểm chứng, nguồn dữ liệu, điều kiện thí nghiệm và chỉ tiêu sai
lệch chấp nhận được phải được lưu rõ trong tài liệu validation.

------------------------------------------------------------------------

## 14. Tối ưu hóa

Theo lựa chọn 18D:

**V1 chưa cần tối ưu hóa.**

Vì vậy không đưa các nội dung sau thành yêu cầu bắt buộc:

-   tìm điểm vận hành tối ưu;
-   tối thiểu hóa năng lượng;
-   tối ưu đa mục tiêu;
-   thuật toán AI/ML tối ưu;
-   optimizer tự động.

Phần mềm chỉ cần **mô phỏng + khảo sát độ nhạy + kiểm chứng**.

Tối ưu hóa được xem là hướng phát triển sau V1.

------------------------------------------------------------------------

## 15. Điều kiện nghiệm thu chuyên môn

Theo lựa chọn 19C, mức đạt chuyên môn cuối cùng được xác định là:

**2 hệ + validation + đề xuất vùng vận hành.**

Điều này được giữ nguyên theo phiếu chuyên gia.

Tuy nhiên, lựa chọn 3B đồng thời xác định rằng **giai đoạn đầu chưa cần
hệ thứ hai, làm thật chắc một hệ trước**.

Vì vậy kế hoạch triển khai được hiểu theo hai mốc, không thay đổi nội
dung đã chốt:

### Mốc triển khai đầu tiên

-   hoàn thiện Ethanol -- Water;
-   mô hình chạy được;
-   kiểm chứng được;
-   có khảo sát độ nhạy.

### Mốc nghiệm thu chuyên môn theo lựa chọn 19C

-   mở rộng sang hệ thứ hai;
-   có validation;
-   có cơ sở đề xuất vùng vận hành.

**Hệ chất thứ hai chưa được phiếu hiện tại xác định.** Không tự chọn hệ
thứ hai nếu chưa có quyết định bổ sung.

------------------------------------------------------------------------

## 16. Giao diện V1

Giao diện phải phục vụ logic lõi, không dẫn dắt dự án mở rộng ngoài phạm
vi.

### Màn hình mô phỏng chính

Nên gồm ba khu vực:

**Đầu vào → Sơ đồ tháp → Kết quả**

Đầu vào chỉ hiển thị các biến thực sự cần thiết cho mô hình.

Kết quả ưu tiên bộ output bắt buộc:

`xD, xB, D, B, Recovery, QC, QR`.

### Màn hình khảo sát

Cho phép chọn một trong ba biến:

-   `R`;
-   số mâm;
-   vị trí mâm nhập liệu.

Người dùng nhập miền khảo sát và chạy các case.

### Không bắt buộc trong V1

-   màn hình tối ưu hóa;
-   dashboard phức tạp;
-   mô phỏng động;
-   thủy lực tháp chi tiết;
-   nhiều mô hình nhiệt động cho người dùng tùy ý lựa chọn;
-   AI/ML.

------------------------------------------------------------------------

## 17. Luồng xử lý lõi của phần mềm

``` text
Người dùng nhập dữ liệu
        ↓
Kiểm tra dữ liệu đầu vào
        ↓
Nạp dữ liệu Ethanol – Water
        ↓
Tính tính chất/VLE
Antoine → Raoult
(+ Wilson khi chế độ này được áp dụng)
        ↓
Thiết lập q-line
        ↓
Thiết lập đường vận hành
        ↓
McCabe – Thiele
        ↓
Cân bằng vật chất
        ↓
Tính xD, xB, D, B, Recovery
        ↓
Tính QC, QR theo mô hình năng lượng V1
        ↓
Kiểm tra sai số < 10^-4
        ↓
┌──────────────────────┐
│ Đạt                  │ → Xuất kết quả
│ Không đạt            │ → Báo lỗi/không hội tụ
└──────────────────────┘
```

------------------------------------------------------------------------

## 18. Cấu trúc module đề xuất để triển khai

Tài liệu này không bắt buộc ngôn ngữ lập trình. Khi triển khai, nên tách
logic thành các module độc lập:

``` text
data/
    component-data
    experimental-data

thermodynamics/
    antoine
    raoult
    wilson

distillation/
    material-balance
    q-line
    operating-lines
    mccabe-thiele
    condenser
    reboiler
    energy

solver/
    calculation
    convergence
    validation

sensitivity/
    reflux-ratio
    number-of-stages
    feed-stage

ui/
    simulation
    sensitivity
    results

tests/
    unit-tests
    reference-cases
    experimental-validation
```

Tên thư mục thực tế có thể thay đổi theo công nghệ được chọn; **ranh
giới chức năng nên được giữ** để tránh trộn giao diện với logic khoa
học.

------------------------------------------------------------------------

## 19. Nguyên tắc triển khai cho sinh viên

1.  **Logic khoa học tách khỏi giao diện.**
2.  Không hard-code kết quả để phục vụ demo.
3.  Mọi kết quả phải sinh từ dữ liệu đầu vào và mô hình.
4.  Các hằng số Antoine/Wilson phải có nguồn và đơn vị rõ ràng.
5.  Mọi đại lượng phải khai báo đơn vị.
6.  Có kiểm tra miền hợp lệ của input.
7.  Có kiểm tra cân bằng vật chất.
8.  Có kiểm tra sai số `< 10⁻⁴`.
9.  Có test case cố định để phát hiện code thay đổi làm sai kết quả.
10. Dữ liệu thực nghiệm dùng validation phải được lưu riêng, không trộn
    vào dữ liệu tính toán.
11. Không thêm tính năng ngoài phạm vi V1 nếu logic lõi chưa ổn định.
12. Mỗi thay đổi phương pháp chuyên môn phải được GVHD/chuyên gia chốt
    trước khi thay đổi tài liệu này.

------------------------------------------------------------------------

## 20. Những vấn đề chưa được phiếu hiện tại chốt

Các nội dung sau **không được tự suy diễn thành quyết định chuyên môn**:

-   hệ chất thứ hai là hệ nào;
-   nguồn và bộ hằng số Antoine chính thức;
-   nguồn và bộ tham số Wilson chính thức;
-   miền nhiệt độ/áp suất hợp lệ của dữ liệu;
-   cách cụ thể ghép Wilson vào VLE trong phiên bản triển khai;
-   công thức cụ thể tính `QC`, `QR` trong mô hình đơn giản;
-   cách đưa tỷ lệ tổn thất nhiệt vào cân bằng năng lượng;
-   định nghĩa residual cụ thể cho tiêu chí `< 10⁻⁴`;
-   bộ dữ liệu thực nghiệm dùng validation;
-   mức sai lệch validation được coi là chấp nhận được;
-   chi tiết công nghệ lập trình và kiến trúc phần mềm.

Các nội dung này phải được giải quyết trong **tài liệu đặc tả kỹ
thuật/thuật toán**, nhưng không được làm thay đổi 20 quyết định chuyên
môn gốc nếu chưa được phê duyệt.

------------------------------------------------------------------------

## 21. Trạng thái quyết định

    STT  Câu trả lời  Quyết định lõi
  ----- ------------- --------------------------------------------------------
      1       A       Nhị phân, steady-state, mâm cân bằng/phạm vi cơ sở
      2       A       Ethanol -- Water
      3       B       Làm chắc 1 hệ trước
      4       A       Raoult + Antoine
      5       B       Wilson nếu dùng hệ số hoạt độ
      6       B       McCabe -- Thiele
      7       C       Cho phép total/partial condenser
      8       C       Reboiler đơn giản theo tải nhiệt
      9       A       Áp suất không đổi
     10       A       Mâm lý thuyết 100%
     11       B       Cho nhập hệ số/tỷ lệ tổn thất nhiệt
     12       A       q-value
     13       A       R + D
     14       A       xD, xB, D, B, recovery, QC, QR
     15       A       Khảo sát R, số mâm, vị trí feed
     16       C       Sai số \< 10⁻⁴
     17       B       Validation bằng dữ liệu thực nghiệm
     18       D       Chưa tối ưu ở V1
     19       C       Mục tiêu nghiệm thu: 2 hệ + validation + vùng vận hành
     20       A       Không có yêu cầu bổ sung trước khi bắt đầu code

------------------------------------------------------------------------

## 22. Quy tắc quản lý tài liệu

**`Logic dự án.md` là tài liệu nguồn về quyết định logic lõi.**

Khi viết các tài liệu tiếp theo như:

-   `Mục tiêu dự án.md`;
-   `Đặc tả thuật toán.md`;
-   `Kiến trúc phần mềm.md`;
-   `Yêu cầu giao diện.md`;
-   `Kế hoạch triển khai.md`;
-   `Validation.md`;
-   `README.md`;

các tài liệu đó phải tham chiếu và **không được mâu thuẫn với Logic dự
án.md**.

Nếu GVHD hoặc chuyên gia thay đổi một quyết định lõi:

1.  cập nhật `Logic dự án.md` trước;
2.  ghi rõ quyết định nào thay đổi;
3.  sau đó mới cập nhật code và các tài liệu phụ thuộc.

------------------------------------------------------------------------

**Trạng thái:** Baseline logic V1\
**Nguồn quyết định:** Phiếu chốt logic lõi -- Anh Đại\
**Mục đích sử dụng:** Viết tài liệu dự án, phân công sinh viên, thiết kế
thuật toán, phát triển phần mềm và kiểm thử.
