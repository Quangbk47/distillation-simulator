# CALCULATION_FORMULAS.md

## Distillation Simulator V1 --- Calculation Specification

**Mục đích:** Tài liệu này là contract tính toán để sinh viên triển khai
mô phỏng chưng cất nhị phân Ethanol--Water. V1 ưu tiên: nhập số liệu →
tính → trả kết quả → vẽ sơ đồ/đồ thị. Không nhằm thay thế Aspen/HYSYS.

------------------------------------------------------------------------

## 1. Phạm vi và giả thiết V1

-   Hệ nhị phân: **Ethanol (cấu tử nhẹ) -- Water (cấu tử nặng)**.
-   Trạng thái ổn định (steady state).
-   Áp suất tháp `P` coi như không đổi.
-   Cân bằng hơi--lỏng (VLE): **Raoult + Antoine**.
-   Phương pháp xác định số mâm/thành phần theo mâm: **McCabe--Thiele**.
-   `N` là số mâm lý thuyết trong **thân tháp**, không tính condenser và
    reboiler.
-   `NF` là vị trí mâm nhập liệu, `1 <= NF <= N`.
-   V1 bao gồm **total condenser và partial condenser**. Total condenser có
    thể được triển khai trước để có vertical slice sớm; partial condenser là
    một nhánh thuật toán riêng và chỉ được bật sau khi có test/reference case
    riêng. Không dùng total-condenser equation rồi chỉ đổi nhãn UI.
-   `q` được nhập trực tiếp.
-   Nhiệt tải `QC`, `QR` dùng cân bằng enthalpy đơn giản; không cần mô
    hình nhiệt động công nghiệp phức tạp.

> Lưu ý khoa học: hệ Ethanol--Water có tính không lý tưởng và azeotrope.
> Raoult lý tưởng là mô hình đơn giản hóa phục vụ V1/giảng dạy; giao
> diện phải nêu rõ mô hình đang dùng.

------------------------------------------------------------------------

## 2. Ký hiệu và đơn vị chuẩn

  Ký hiệu   Ý nghĩa                                Đơn vị
  --------- -------------------------------------- --------------------------------------
  `F`       Lưu lượng feed                         kmol/h
  `D`       Lưu lượng sản phẩm đỉnh                kmol/h
  `B`       Lưu lượng sản phẩm đáy                 kmol/h
  `zF`      Phần mol ethanol trong feed            mol/mol
  `xD`      Phần mol ethanol trong sản phẩm đỉnh   mol/mol
  `xB`      Phần mol ethanol trong sản phẩm đáy    mol/mol
  `x`       Phần mol ethanol pha lỏng              mol/mol
  `y`       Phần mol ethanol pha hơi               mol/mol
  `P`       Áp suất tổng                           bar (convert thống nhất với Antoine)
  `T`       Nhiệt độ                               °C
  `R`       Tỷ số hồi lưu `L/D`                    không thứ nguyên
  `q`       Trạng thái nhiệt của feed              không thứ nguyên
  `N`       Số mâm lý thuyết thân tháp             mâm
  `NF`      Vị trí mâm feed                        mâm
  `QC`      Nhiệt tải condenser                    kW
  `QR`      Nhiệt tải reboiler                     kW
  `Qloss`   Tổn thất nhiệt                         kW

**Quy tắc nội bộ:** mọi thành phần dùng `0..1`; chỉ nhân `100` khi hiển
thị `%`.

------------------------------------------------------------------------

## 3. Kiểm tra input

Tối thiểu:

``` text
F > 0
0 <= zF <= 1 (pure-component limits chỉ dùng cho sanity/input tests; recovery
  phải báo không xác định khi feed ethanol bằng 0)
P > 0
N >= 1 và là số nguyên
1 <= NF <= N
R >= 0
0 <= D <= F
heatLoss_kW >= 0
q là số hữu hạn
```

Nếu người dùng nhập `D`, tính `B = F - D`. Nếu `D = F` thì không thể có
dòng đáy hữu hạn cho bài toán thông thường → báo input không vật lý.

Không âm thầm sửa input sai.

------------------------------------------------------------------------

## 4. Phương trình Antoine

Cho mỗi cấu tử `i`:

``` text
log10(Psat_i) = A_i - B_i / (C_i + T)
```

Suy ra:

``` text
Psat_i(T) = 10^(A_i - B_i/(C_i + T))
```

**Bắt buộc:** `A, B, C`, đơn vị áp suất của `Psat`, miền nhiệt độ và
nguồn dữ liệu phải đi cùng nhau. Không trộn coefficient của một hệ đơn
vị với công thức khác.

Nếu `T` nằm ngoài miền nguồn nhưng vẫn cho kết quả vật lý, V1 có thể
tính ngoại suy nhưng phải trả warning:

``` text
THERMO_EXTRAPOLATION
```

Nếu `Psat <= 0`, NaN/Inf hoặc nghiệm không vật lý → dừng calculation.

------------------------------------------------------------------------

## 5. Raoult và quan hệ VLE

Với dung dịch lý tưởng:

``` text
y_i * P = x_i * Psat_i(T)
```

Đối với ethanol:

``` text
yE = xE * Psat_E(T) / P
```

Đối với water:

``` text
yW = xW * Psat_W(T) / P
```

với:

``` text
xW = 1 - xE
yW = 1 - yE
```

### 5.1 Bubble temperature tại `x`

Tìm `T` thỏa:

``` text
x * Psat_E(T) + (1-x) * Psat_W(T) = P
```

Đây là bài toán tìm nghiệm một biến.

Sau khi tìm được `T`:

``` text
y = x * Psat_E(T) / P
```

Hàm engine nên có dạng:

``` text
bubble_temperature(x, P) -> T
equilibrium_y(x, P) -> (y, T)
```

Nên dùng bisection/Brent hoặc phương pháp tìm nghiệm có bracket; không
cần solver phức tạp.

### 5.2 Tạo đường cân bằng

Chọn grid, ví dụ:

``` text
x = 0.00, 0.01, ..., 1.00
```

Với mỗi `x`, tính `T` và `y`. Dùng các điểm `(x,y)` để vẽ equilibrium
curve và nội suy khi stepping McCabe--Thiele.

------------------------------------------------------------------------

## 6. Cân bằng vật chất toàn tháp

### 6.1 Cân bằng tổng

``` text
F = D + B
```

Nếu `F` và `D` là input:

``` text
B = F - D
```

### 6.2 Cân bằng ethanol

``` text
F*zF = D*xD + B*xB
```

Nếu đã biết `F, D, zF, xD`:

``` text
xB = (F*zF - D*xD) / B
```

Nếu đã biết `xD, xB`:

``` text
D = F*(zF-xB)/(xD-xB)
B = F-D
```

Luôn kiểm tra:

``` text
0 <= xB <= zF <= xD <= 1
```

cho bài toán tách ethanol về đỉnh thông thường. Nếu không thỏa, đánh dấu
kết quả không vật lý.

------------------------------------------------------------------------

## 7. Recovery ethanol

Recovery ethanol về đỉnh:

``` text
Recovery_E = D*xD / (F*zF)
```

Hiển thị:

``` text
Recovery_E_percent = 100 * Recovery_E
```

Không dùng `D/F` thay cho recovery cấu tử.

------------------------------------------------------------------------

## 8. Đường chéo McCabe--Thiele

``` text
y = x
```

Dùng làm đường tham chiếu trên đồ thị `x-y`.

------------------------------------------------------------------------

## 9. Đường vận hành đoạn luyện (rectifying line)

Với total condenser và constant molar overflow:

``` text
R = L/D
```

Đường luyện:

``` text
y = (R/(R+1))*x + xD/(R+1)
```

Đặt:

``` text
mR = R/(R+1)
bR = xD/(R+1)
```

thì:

``` text
yR(x) = mR*x + bR
```

------------------------------------------------------------------------

## 10. q-line

Với `q != 1`:

``` text
y = [q/(q-1)]*x - zF/(q-1)
```

### Trường hợp `q = 1`

Feed là saturated liquid:

``` text
x = zF
```

q-line là đường thẳng đứng. **Không** đưa `q=1` vào công thức trên vì
chia cho zero.

Các trường hợp tham khảo:

``` text
q = 1      saturated liquid
q = 0      saturated vapor
q > 1      subcooled liquid
0 < q < 1  partially vaporized feed
q < 0      superheated vapor
```

------------------------------------------------------------------------

## 11. Giao điểm q-line và rectifying line

### Với `q != 1`

Giải:

``` text
mR*x + bR = [q/(q-1)]*x - zF/(q-1)
```

thu được `(xq, yq)`.

### Với `q = 1`

``` text
xq = zF
yq = yR(zF)
```

Điểm này được dùng để xây dựng stripping line.

------------------------------------------------------------------------

## 12. Đường vận hành đoạn chưng (stripping line)

Trong McCabe--Thiele đơn giản, stripping line đi qua:

``` text
(xB, xB)
```

và giao điểm feed:

``` text
(xq, yq)
```

Do đó:

``` text
mS = (yq - xB)/(xq - xB)
bS = xB - mS*xB
```

và:

``` text
yS(x) = mS*x + bS
```

Nếu `xq ≈ xB`, phải xử lý singularity thay vì chia trực tiếp.

------------------------------------------------------------------------

## 13. Stepping McCabe--Thiele

Với total condenser, bắt đầu gần:

``` text
(xD, xD)
```

Mỗi mâm gồm hai bước:

1.  **Horizontal:** từ operating line sang equilibrium curve.
2.  **Vertical:** từ equilibrium curve về operating line.

Cách code ổn định:

``` text
current_y = xD

for stage in 1..N:
    # horizontal to equilibrium curve:
    find x_stage such that y_eq(x_stage, P) = current_y

    # lưu x_stage và bubble T tương ứng

    # chọn operating line
    if stage thuộc đoạn luyện:
        next_y = yR(x_stage)
    else:
        next_y = yS(x_stage)

    current_y = next_y
```

Việc chuyển rectifying → stripping phải nhất quán với `NF`/feed
intersection. Trong V1 khi `NF` là input, engine phải kiểm tra `NF` có
phù hợp với stepping/feed intersection; không âm thầm thay đổi `NF`.

### Điều kiện dừng/lỗi

Dừng và trả `non_converged` nếu:

-   không tìm được nghiệm equilibrium;
-   bước lặp đi ra ngoài `[0,1]` đáng kể;
-   xuất hiện NaN/Inf;
-   lặp không tiến triển (pinch);
-   vượt giới hạn iteration;
-   kết quả cuối không thỏa residual.

------------------------------------------------------------------------

## 14. Nhiệt độ theo mâm

Sau khi có `x_stage`:

``` text
T_stage = bubble_temperature(x_stage, P)
```

Lưu:

``` text
stage
T_C
x_ethanol
y_ethanol
```

Đây là dữ liệu dùng cho bảng và đồ thị `T` theo số mâm.

Không nội suy nhiệt độ tuyến tính từ đỉnh xuống đáy nếu engine đã có
VLE; phải tính từ bubble-point relation.

------------------------------------------------------------------------

## 15. Total condenser

Trong total condenser, hơi đỉnh được ngưng tụ hoàn toàn. Với giả thiết
không có subcooling đáng kể:

``` text
xD ≈ y_top
```

Reflux và distillate có cùng composition `xD`.

Nếu:

``` text
R = L/D
```

thì:

``` text
L = R*D
V = L + D = (R+1)*D
```

Các quan hệ này tạo rectifying line ở Mục 9.

------------------------------------------------------------------------

## 16. Partial condenser

Partial condenser là **nhánh thuật toán riêng**, vì condenser có thể
đóng vai trò một equilibrium stage. Không được dùng total-condenser
equation rồi chỉ đổi nhãn UI.

Total condenser được phép triển khai trước trong roadmap, nhưng partial
condenser vẫn là deliverable bắt buộc của V1 theo quyết định chuyên gia. Chỉ
bật partial condenser sau khi nhánh equilibrium-stage và reference case của
nó đã được kiểm thử. Trong thời gian chưa hoàn tất, API/UI phải báo
`NOT_IMPLEMENTED`; không trả số giả và không được tuyên bố V1 hoàn chỉnh.

------------------------------------------------------------------------

## 17. Reboiler

V1 có thể dùng reboiler kiểu equilibrium/simple energy boundary.
Reboiler **không tính vào `N`** theo convention của dự án.

Dòng đáy:

``` text
B = F-D
```

và composition đáy lấy từ nghiệm toàn tháp/stepping đã kiểm tra cân
bằng.

------------------------------------------------------------------------

## 18. Cân bằng năng lượng đơn giản

Đây là mô hình giáo dục, không phải rigorous enthalpy package.

Định nghĩa enthalpy tương đối với nhiệt độ tham chiếu `Tref`.

### 18.1 Liquid sensible enthalpy

Cho cấu tử `i`:

``` text
hL_i(T) = CpL_i * (T-Tref)
```

Mixture:

``` text
hL_mix(T,x) = x*hL_E(T) + (1-x)*hL_W(T)
```

### 18.2 Vapor enthalpy đơn giản

``` text
hV_i(T) = CpL_i*(Tb_i-Tref) + Hvap_i + CpV_i*(T-Tb_i)
```

hoặc một convention đơn giản tương đương, **nhưng toàn engine phải dùng
duy nhất một convention** và constants phải có nguồn.

Mixture:

``` text
hV_mix(T,y) = y*hV_E(T) + (1-y)*hV_W(T)
```

### 18.3 Quy đổi công suất

Nếu lưu lượng là `kmol/h` và enthalpy là `kJ/kmol`:

``` text
Q_kW = flow_kmol_h * delta_h_kJ_kmol / 3600
```

### 18.4 Condenser duty

Chọn convention hiển thị:

-   `QC < 0`: nhiệt lấy ra khỏi hệ.
-   `QR > 0`: nhiệt cấp vào hệ.

Ví dụ total condenser:

``` text
QC = D*(R+1)*(hL_top - hV_top)/3600
```

nên thường `QC < 0`.

### 18.5 Reboiler duty từ overall energy balance

Dùng convention:

``` text
F*hF + QR + QC = D*hD + B*hB + Qloss
```

suy ra:

``` text
QR = D*hD + B*hB + Qloss - F*hF - QC
```

Trong đó `Qloss >= 0` là nhiệt thất thoát ra môi trường. Theo convention
này, tăng `Qloss` làm tăng `QR` cần cấp.

**Đây là convention bắt buộc cho V1** để tránh sinh viên tự chọn dấu
khác nhau.

------------------------------------------------------------------------

## 19. Feed enthalpy và q

Trong V1, `q` dùng trực tiếp để tạo q-line. Không bắt buộc suy `q` từ
`Tfeed`.

Nếu UI vẫn cho nhập `Tfeed`, nhiệt độ này dùng cho energy
calculation/hiển thị, không được âm thầm ghi đè `q`.

Nếu muốn tránh mâu thuẫn ở V1 tối giản, UI có thể chỉ dùng `q` và bỏ
`Tfeed` khỏi calculation McCabe--Thiele.

------------------------------------------------------------------------

## 20. Residuals và điều kiện success

### 20.1 Total mass residual

Dùng normalized residual:

``` text
r_mass = abs(F-D-B) / max(F, eps)
```

### 20.2 Ethanol component residual

``` text
r_ethanol =
abs(F*zF - D*xD - B*xB) / max(F*zF, eps)
```

### 20.3 Solver residual

Tùy root solver:

``` text
r_solver = max(abs(f(root)))
```

hoặc residual tương đương đã được document.

### Success gate

``` text
success =
    r_mass < 1e-4
    AND r_ethanol < 1e-4
    AND r_solver < 1e-4
    AND all physical checks pass
```

Không hiển thị "thành công" chỉ vì solver trả về một số.

------------------------------------------------------------------------

## 21. Output tối thiểu

Engine trả ít nhất:

``` text
status
D_kmol_h
B_kmol_h
xD
xB
recovery_ethanol_percent
QC_kW
QR_kW
residuals
warnings
thermoModel = "raoult-antoine"
thermoDataVersion
stages[]
```

Mỗi phần tử `stages[]`:

``` text
stage
T_C
x_ethanol
y_ethanol
section = rectifying | feed | stripping
```

UI nhân `xD`, `xB`, `x`, `y` với `100` khi muốn hiển thị mol%.

------------------------------------------------------------------------

## 22. Sensitivity

Khảo sát đúng **một biến tại một thời điểm**:

``` text
R
hoặc N
hoặc NF
```

Các input khác giữ nguyên.

Pseudo-code:

``` text
for value in sweep:
    input2 = copy(base_input)
    input2[target] = value
    result = simulate(input2)
    store(value, result)
```

Không cần optimization algorithm trong V1.

------------------------------------------------------------------------

## 23. Pseudocode tổng thể

``` text
simulate(input):

    validate(input)

    thermo = load_reviewed_antoine_data()

    build_or_prepare_VLE(P)

    B = F - D

    establish total-condenser rectifying line
    establish q-line
    determine feed intersection

    solve/iterate composition boundary consistently
    establish stripping line

    perform McCabe-Thiele stepping
    calculate xD, xB and stage profiles

    for each stage:
        calculate bubble temperature
        calculate equilibrium vapor composition

    calculate recovery

    calculate simple enthalpies
    calculate QC
    calculate QR using overall energy balance

    calculate residuals
    run physical checks

    status = success only if all gates pass

    return result + warnings + thermo data version
```

------------------------------------------------------------------------

## 24. Golden sanity checks bắt buộc

Trước khi coi engine hoàn thành, test ít nhất:

### Case A --- Material balance identity

Cho bất kỳ kết quả hợp lệ:

``` text
F ≈ D+B
F*zF ≈ D*xD+B*xB
```

đến tolerance `<1e-4` normalized.

### Case B --- Pure-component limits

``` text
x = 0  -> water limit
x = 1  -> ethanol limit
```

VLE không được trả NaN/Inf.

### Case C --- q = 1

q-line phải là:

``` text
x = zF
```

và không xảy ra division-by-zero.

### Case D --- Reflux line

Khi `R` tăng, slope:

``` text
R/(R+1)
```

tiến gần `1`.

### Case E --- Energy sign

Với condenser/reboiler thông thường:

``` text
QC < 0
QR > 0
```

và tăng `Qloss` (giữ các đại lượng khác cố định trong energy test) phải
làm `QR` tăng đúng bằng phần tổn thất bổ sung.

### Case F --- Invalid input

``` text
F <= 0
zF ngoài [0,1]
NF > N
D > F
heatLoss < 0
```

phải bị reject.

------------------------------------------------------------------------

## 25. Ví dụ kiểm tra cân bằng vật chất

Ví dụ chỉ nhằm kiểm tra code balance, **không phải nghiệm chuẩn của toàn
mô phỏng**:

``` text
F = 100 kmol/h
zF = 0.50
D = 45.2 kmol/h
xD = 0.95
B = 54.8 kmol/h
```

Từ cân bằng ethanol:

``` text
xB = (100*0.50 - 45.2*0.95)/54.8
   = 0.128832...
```

Recovery ethanol:

``` text
Recovery = 100*(45.2*0.95)/(100*0.50)
         = 85.88 %
```

Vì vậy, **không được** lấy các con số minh họa trên mockup UI làm đáp án
khoa học nếu chúng không thỏa cân bằng vật chất. Mockup chỉ là tham
chiếu bố cục.

------------------------------------------------------------------------

## 26. Những điều sinh viên không được tự thay đổi

Không tự ý:

-   đổi Raoult + Antoine sang Wilson/NRTL;
-   thay convention `N`;
-   tính recovery bằng `D/F`;
-   thay `q` bằng một dropdown rồi bỏ giá trị số mà không mapping rõ;
-   dùng nhiệt độ tuyến tính giả theo số mâm;
-   thay dấu `QC/QR`;
-   dùng Antoine constants không rõ đơn vị/nguồn;
-   coi mockup UI là dữ liệu validation;
-   trả kết quả khi residual không đạt;
-   thêm AI/ML, optimization hoặc kiến trúc phức tạp ngoài scope.

Nếu cần thay đổi mô hình khoa học, phải cập nhật specification và test
trước.

------------------------------------------------------------------------

## 27. Definition of Done cho calculation engine

Calculation engine V1 được coi là đủ để nối UI khi:

1.  Input validation hoạt động.
2.  Antoine/Raoult tạo được VLE Ethanol--Water ở áp suất yêu cầu.
3.  Bubble temperature và equilibrium inversion có test.
4.  Rectifying line, q-line và stripping line có unit test.
5.  McCabe--Thiele stepping trả stage profile hữu hạn/vật lý.
6.  Cân bằng tổng và ethanol đạt residual `<1e-4`.
7.  Recovery được tính đúng.
8.  Stage temperature lấy từ VLE, không phải dữ liệu giả.
9.  `QC/QR` dùng cùng một enthalpy/sign convention.
10. Warning ngoại suy hoạt động.
11. Có ít nhất một reference/golden case được chuyên gia hoặc nguồn tin
    cậy xác nhận.
12. UI có thể nhận output và vẽ sơ đồ/bảng/đồ thị mà không tự tính lại
    khoa học ở frontend.

------------------------------------------------------------------------

## 28. Nguyên tắc triển khai

**Keep it simple.** V1 cần:

``` text
INPUT
  ↓
Raoult + Antoine / VLE
  ↓
McCabe–Thiele + balances
  ↓
Simple energy balance
  ↓
OUTPUT
  ├─ số liệu
  ├─ bảng theo mâm
  ├─ sơ đồ tháp
  └─ đồ thị
```

Không overengineering. Ưu tiên kết quả đúng, dễ kiểm tra và giao diện
trực quan.
