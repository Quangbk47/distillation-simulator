# Process Model Final

## Input contract
`F_kmol_h>0`, `zF_ethanol in [0,1]`, `q` do người dùng nhập trực tiếp, `P_bar>0`, `N` là số nguyên mâm trong thân tháp, `NF in [1,N]`, `R>=0`, `D>=0`, `heatLoss_kW>=0`, `condenser in total|partial`.

## VLE và stage convention
Kết quả V1 dùng Raoult + Antoine. Khi nhiệt độ ngoài range nguồn, solver cho ngoại suy và return warning `THERMO_EXTRAPOLATION`; UI bắt buộc hiển thị warning. N không gồm condenser hoặc reboiler. Partial condenser và total condenser đều phải phân nhánh thuật toán/test riêng.

## Cân bằng và năng lượng
`F=D+B`; ethanol: `F*zF=D*xD+B*xB`. `Recovery=100*D*xD/(F*zF)`. QC/QR dùng cân bằng enthalpy đơn giản với Cp, latent heat và mọi constant có citation. `heatLoss_kW` là tải nhiệt tuyệt đối; energy module phải định nghĩa rõ nó cộng/trừ vào QR/QC theo convention được ghi trong code và test.
