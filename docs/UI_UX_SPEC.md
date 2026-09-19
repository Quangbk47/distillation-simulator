# UI/UX Specification — V1

## 1. Product behavior

The V1 UI is a small teaching tool, not an enterprise dashboard. The primary
flow is:

```text
enter input → Run simulation → backend calculates → render output
```

The browser never calculates VLE, balances, operating lines, energy or
sensitivity. It sends a typed request to the backend and renders the response.

Desktop layout uses three columns:

```text
LEFT: input        CENTER: process visualization        RIGHT: results
```

The top-level tabs are:

1. `Mô phỏng`
2. `Khảo sát độ nhạy`

The layout must remain usable on a narrow screen by stacking LEFT, CENTER and
RIGHT vertically. No 3D or animation is required.

## 2. Input panel — LEFT

System is fixed to `Ethanol–Water`; it is displayed as read-only text, not a
selectable V1 input.

| Label shown to user | Symbol/API field | Unit | Type | Range | Default | Validation/help |
|---|---|---|---|---|---|---|
| Thành phần nhẹ trong feed | `zF` / `zF_ethanol` | mol/mol | decimal | `0 < zF < 1` | `0.50` | Ethanol mole fraction; display as decimal or mol%. |
| Lưu lượng feed | `F` / `F_kmol_h` | kmol/h | decimal | `> 0` | `100` | Total feed flow. |
| Áp suất tháp | `P` / `P_bar` | bar | decimal | `> 0` | `1.0` (UI default only) | Must use the same pressure unit as reviewed Antoine data after conversion; not a validation case. |
| Trạng thái nhiệt feed | `q` | — | decimal | finite | `1.0` | Direct q input; do not infer it from temperature. Tooltip explains q=1 saturated liquid. |
| Số mâm lý thuyết thân tháp | `N` | mâm | integer | `>= 1` | `10` | Does not include condenser or reboiler. |
| Vị trí mâm nhập liệu | `NF` | mâm | integer | `1..N` | `5` | Count from the top body tray. It is enforced, not auto-corrected. |
| Tỷ số hồi lưu | `R` | — | decimal | `>= 0` | `2.0` | `R=L/D`. |
| Lưu lượng sản phẩm đỉnh | `D_kmol_h` | kmol/h | decimal | `0 < D < F` | `20` | Product flow; xD is calculated, not entered. |
| Loại condenser | `condenser` | — | select | `total`, `partial` | `total` | Partial is disabled/NOT_IMPLEMENTED until its contract is approved. |
| Tổn thất nhiệt | `heatLoss_kW` | kW | decimal | `>= 0` | `0` | Absolute heat load, not a percentage. |

The UI must show a short help note: `xD` and `xB` are outputs. No tray
efficiency input is shown; V1 uses theoretical stages/effectiveness 1. No
reboiler selector is shown because V1 has one convention. `Tfeed` is omitted
from the minimum UI because q is authoritative and it is not required by the
current energy contract.

Buttons and states:

- `Chạy mô phỏng`: disabled while invalid or while a request is pending;
- `Đặt lại`: restores documented defaults;
- inline validation: field-level Vietnamese message with symbol/unit;
- request pending: show `Đang tính...` and preserve entered values;
- failure: show error code/message and trace summary, never stale output;
- partial before closure: show `PARTIAL_CONDENSER_CONTRACT_OPEN` and
  `NOT_IMPLEMENTED`, with no scientific result cards.

## 3. Process visualization — CENTER

Render a simple 2D diagram with labeled nodes and arrows:

```text
                    condenser
                 ↗ reflux L/xD
 vapor/top  ────┤
                │ column (N body trays)
 feed F/zF ────▶│ tray NF
                │
             reboiler
          ↙ bottoms B/xB
```

The actual drawing may use HTML/CSS/SVG. It must visibly include:

- condenser;
- reflux and distillate `D/xD`;
- column/body trays and feed location `F/zF` at `NF`;
- reboiler;
- bottoms `B/xB`;
- `QC` and `QR` labels when energy is available.

The diagram is a visualization of returned data. It must not invent tray
temperatures, compositions or duties. If a temperature gradient is drawn, use
returned `stages[].T_C`; otherwise omit it.

The center may also contain a McCabe–Thiele x-y plot with diagonal,
equilibrium curve, rectifying line, q-line, stripping line and stage steps when
the backend returns them. A missing/pending plot must say `NOT CALCULATED`.

## 4. Results panel — RIGHT

### Summary cards

Display these labels exactly enough to prevent ambiguity:

- `xD — Ethanol trong sản phẩm đỉnh`;
- `xB — Ethanol trong sản phẩm đáy`;
- `Recovery ethanol`;
- `D — Lưu lượng sản phẩm đỉnh`;
- `B — Lưu lượng sản phẩm đáy`;
- `QC — Nhiệt tải condenser`;
- `QR — Nhiệt tải reboiler`.

Do not label xB as “bottom purity” because that can be misunderstood as water
purity. When percentage is shown, use `mol% ethanol = 100*x`.

### Metadata and quality

Always show:

- status and error code if any;
- `Mô hình VLE: Raoult + Antoine`;
- thermo data version;
- warnings, persistently and above/near the results;
- `totalMass`, `ethanolBalance`, `outer`, and `solver` residuals;
- NF requested and NF geometric result when provided.

A success badge must never hide a warning. `THERMO_EXTRAPOLATION` must name
component, actual temperature and source range.

### Stage table

Columns:

| Column | Meaning |
|---|---|
| `stage` | Body tray number, top to bottom |
| `T_C` | VLE-derived bubble temperature |
| `x_ethanol` | Liquid ethanol mole fraction |
| `y_ethanol` | Vapor ethanol mole fraction |
| `section` | `rectifying` or `stripping` |

Condenser/reboiler boundary rows, if shown, must be explicitly labeled and
must not be counted as body stages.

### Graphs

Required: `Temperature vs Stage`. Optional if simple: composition profile and
McCabe–Thiele plot. Empty/pending graph state is labeled `NOT CALCULATED`; no
placeholder curve may look scientific.

## 5. Sensitivity tab

The user selects exactly one parameter: `R`, `N` or `NF`, enters a list/range,
and clicks `Chạy khảo sát`. The UI must display:

- selected parameter and values;
- fixed base-case summary;
- result table/series;
- one simple chart for key outputs;
- failed points with their error code.

The UI must state that q, condenser, heat loss and every non-selected input are
held fixed. No optimization controls or multi-variable sweep are shown.

## 6. Demo and pending states

Before the engine/data is ready, the Firebase UI shell may show layout and
interaction using only labels/placeholders:

```text
DEMO
NOT CALCULATED
ENGINE NOT CONNECTED
```

It must not show plausible-looking xD/xB/QC/QR values. A demo layout is not a
scientific result and must be visually labeled as such.

## 7. Accessibility and error semantics

- Every input has a visible label, unit and keyboard-accessible control.
- Errors are adjacent to the field and summarized at the top of the panel.
- Color is not the only warning/error signal; use text and icons/labels.
- Loading/failure states preserve user input and never display stale results as
  if they belong to the new request.
- The backend error/status is rendered verbatim enough for debugging and
  handover; the UI may add Vietnamese guidance but not change the code.
