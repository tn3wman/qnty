# Engineering Calculation Report: PipeBends

**Generated:** 2025-09-26 17:43:54

## 1. Known Variables

| Symbol | Name | Value | Unit |
|--------|------|-------|------|
| s_D | Outside Diameter (S) | 0.84 | in |
| s_E | Quality Factor (S) | 0.8 |  |
| s_P | Design Pressure (S) | 90 | psi |
| s_S | Allowable Stress (S) | 20000 | psi |
| s_T_bar | Nominal Wall Thickness (S) | 0.147 | in |
| s_U_m | Mill Undertolerance (S) | 0.125 |  |
| s_W | Weld Joint Strength Reduction Factor (S) | 1 |  |
| s_Y | Y Coefficient (S) | 0.4 |  |
| s_c | Mechanical Allowances (S) | 0 | in |
| R_1 | Bend Radius | 5 | in |

## 2. Unknown Variables (To Calculate)

| Symbol | Name | Unit |
|--------|------|------|
| s_P_max | Pressure, Maximum (S) | Pa |
| s_T | Wall Thickness (S) | m |
| s_d | Inside Diameter (S) | m |
| s_t | Pressure Design Thickness (S) | m |
| s_t_m | Minimum Required Thickness (S) | m |
| I_e | Extrados Correction Factor |  |
| I_i | Intrados Correction Factor |  |
| P_max | Maximum Allowable Pressure | Pa |
| P_max_e | Maximum Pressure, Outside Bend | Pa |
| P_max_i | Maximum Pressure, Inside Bend | Pa |
| t_e | Design Thickness, Outside Bend | m |
| t_i | Design Thickness, Inside Bend | m |
| t_m_e | Minimum Required Thickness, Outside Bend | m |
| t_m_i | Minimum Required Thickness, Inside Bend | m |

## 3. Equations Used

1. `s_T = s_T_bar * (1  - s_U_m)`
2. `I_e = (4  * R_1 / s_D + 1 ) / (4  * R_1 / s_D + 2 )`
3. `I_i = (4  * R_1 / s_D - 1 ) / (4  * R_1 / s_D - 2 )`
4. `s_t = s_P * s_D / (2  * (s_S * s_E * s_W + s_P * s_Y))`
5. `s_P_max = 2  * (s_T - s_c) * s_S * s_E * s_W / (s_D - 2  * (s_T - s_c) * s_Y)`
6. `s_d = s_D - 2  * s_T`
7. `t_e = s_P * s_D / (2  * (s_S * s_E * s_W / I_e + s_P * s_Y))`
8. `t_i = s_P * s_D / (2  * (s_S * s_E * s_W / I_i + s_P * s_Y))`
9. `P_max_i = 2  * s_E * s_S * s_W * s_T / (I_i * (s_D - 2  * s_Y * s_T))`
10. `P_max_e = 2  * s_E * s_S * s_W * s_T / (I_e * (s_D - 2  * s_Y * s_T))`
11. `s_t_m = s_t + s_c`
12. `t_m_e = t_e + s_c`
13. `P_max = if(if(P_max_i < P_max_e, P_max_i, P_max_e) < s_P_max, if(P_max_i < P_max_e, P_max_i, P_max_e), s_P_max)`
14. `t_m_i = t_i + s_c`
15. `s_Y = if(s_t < s_D / 6 , s_Y, if(s_t >= s_D / 6 , (s_d + 2  * s_c) / (s_D + s_d + 2  * s_c), s_Y))`

## 4. Step-by-Step Solution

### Step 1: Solve for s_T

    **Equation:**
    ```
    s_T = s_T_bar * (1  - s_U_m)
    ```

    **Substitution:**
    ```
    s_T = 0.147 in * (1  - 0.125 )
    ```

    **Result:**
    ```
    s_T = 0.00326707 m
    ```

### Step 2: Solve for I_e

    **Equation:**
    ```
    I_e = (4  * R_1 / s_D + 1 ) / (4  * R_1 / s_D + 2 )
    ```

    **Substitution:**
    ```
    I_e = (4  * 5 in / 0.84 in + 1 ) / (4  * 5 in / 0.84 in + 2 )
    ```

    **Result:**
    ```
    I_e = 0.961255 rad
    ```

### Step 3: Solve for I_i

    **Equation:**
    ```
    I_i = (4  * R_1 / s_D - 1 ) / (4  * R_1 / s_D - 2 )
    ```

    **Substitution:**
    ```
    I_i = (4  * 5 in / 0.84 in - 1 ) / (4  * 5 in / 0.84 in - 2 )
    ```

    **Result:**
    ```
    I_i = 1.04585 rad
    ```

### Step 4: Solve for s_t

    **Equation:**
    ```
    s_t = s_P * s_D / (2  * (s_S * s_E * s_W + s_P * s_Y))
    ```

    **Substitution:**
    ```
    s_t = 90 psi * 0.84 in / (2  * (20000 psi * 0.8  * 1  + 90 psi * 0.4 ))
    ```

    **Result:**
    ```
    s_t = 5.98728e-05 m
    ```

### Step 5: Solve for s_P_max

    **Equation:**
    ```
    s_P_max = 2  * (s_T - s_c) * s_S * s_E * s_W / (s_D - 2  * (s_T - s_c) * s_Y)
    ```

    **Substitution:**
    ```
    s_P_max = 2  * (0.00326707 - 0 in) * 20000 psi * 0.8  * 1  / (0.84 in - 2  * (0.00326707 - 0 in) * 0.4 )
    ```

    **Result:**
    ```
    s_P_max = 3.85006e+07 Pa
    ```

### Step 6: Solve for s_d

    **Equation:**
    ```
    s_d = s_D - 2  * s_T
    ```

    **Substitution:**
    ```
    s_d = 0.84 in - 2  * 0.00326707
    ```

    **Result:**
    ```
    s_d = 0.0148018 m
    ```

### Step 7: Solve for t_e

    **Equation:**
    ```
    t_e = s_P * s_D / (2  * (s_S * s_E * s_W / I_e + s_P * s_Y))
    ```

    **Substitution:**
    ```
    t_e = 90 psi * 0.84 in / (2  * (20000 psi * 0.8  * 1  / 0.961255 + 90 psi * 0.4 ))
    ```

    **Result:**
    ```
    t_e = 5.7558e-05 m
    ```

### Step 8: Solve for t_i

    **Equation:**
    ```
    t_i = s_P * s_D / (2  * (s_S * s_E * s_W / I_i + s_P * s_Y))
    ```

    **Substitution:**
    ```
    t_i = 90 psi * 0.84 in / (2  * (20000 psi * 0.8  * 1  / 1.04585 + 90 psi * 0.4 ))
    ```

    **Result:**
    ```
    t_i = 6.26116e-05 m
    ```

### Step 9: Solve for P_max_i

    **Equation:**
    ```
    P_max_i = 2  * s_E * s_S * s_W * s_T / (I_i * (s_D - 2  * s_Y * s_T))
    ```

    **Substitution:**
    ```
    P_max_i = 2  * 0.8  * 20000 psi * 1  * 0.00326707 / (1.04585 * (0.84 in - 2  * 0.4  * 0.00326707))
    ```

    **Result:**
    ```
    P_max_i = 3.68127e+07 Pa
    ```

### Step 10: Solve for P_max_e

    **Equation:**
    ```
    P_max_e = 2  * s_E * s_S * s_W * s_T / (I_e * (s_D - 2  * s_Y * s_T))
    ```

    **Substitution:**
    ```
    P_max_e = 2  * 0.8  * 20000 psi * 1  * 0.00326707 / (0.961255 * (0.84 in - 2  * 0.4  * 0.00326707))
    ```

    **Result:**
    ```
    P_max_e = 4.00525e+07 Pa
    ```

### Step 11: Solve for s_t_m

    **Equation:**
    ```
    s_t_m = s_t + s_c
    ```

    **Substitution:**
    ```
    s_t_m = 5.98728e-05 + 0 in
    ```

    **Result:**
    ```
    s_t_m = 5.98728e-05 m
    ```

### Step 12: Solve for t_m_e

    **Equation:**
    ```
    t_m_e = t_e + s_c
    ```

    **Substitution:**
    ```
    t_m_e = 5.7558e-05 + 0 in
    ```

    **Result:**
    ```
    t_m_e = 5.7558e-05 m
    ```

### Step 13: Solve for P_max

    **Equation:**
    ```
    P_max = if(if(P_max_i < P_max_e, P_max_i, P_max_e) < s_P_max, if(P_max_i < P_max_e, P_max_i, P_max_e), s_P_max)
    ```

    **Substitution:**
    ```
    P_max = if(if(3.68127e+07 < 4.00525e+07, 3.68127e+07, 4.00525e+07) < 3.85006e+07, if(3.68127e+07 < 4.00525e+07, 3.68127e+07, 4.00525e+07), 3.85006e+07)
    ```

    **Result:**
    ```
    P_max = 3.68127e+07 Pa
    ```

### Step 14: Solve for t_m_i

    **Equation:**
    ```
    t_m_i = t_i + s_c
    ```

    **Substitution:**
    ```
    t_m_i = 6.26116e-05 + 0 in
    ```

    **Result:**
    ```
    t_m_i = 6.26116e-05 m
    ```

## 5. Summary of Results

| Variable | Name | Final Value | Unit |
|----------|------|-------------|------|
| s_P_max | Pressure, Maximum (S) | 3.85006e+07 | Pa |
| s_T | Wall Thickness (S) | 0.00326707 | m |
| s_d | Inside Diameter (S) | 0.0148018 | m |
| s_t | Pressure Design Thickness (S) | 5.98728e-05 | m |
| s_t_m | Minimum Required Thickness (S) | 5.98728e-05 | m |
| I_e | Extrados Correction Factor | 0.961255 |  |
| I_i | Intrados Correction Factor | 1.04585 |  |
| P_max | Maximum Allowable Pressure | 3.68127e+07 | Pa |
| P_max_e | Maximum Pressure, Outside Bend | 4.00525e+07 | Pa |
| P_max_i | Maximum Pressure, Inside Bend | 3.68127e+07 | Pa |
| t_e | Design Thickness, Outside Bend | 5.7558e-05 | m |
| t_i | Design Thickness, Inside Bend | 6.26116e-05 | m |
| t_m_e | Minimum Required Thickness, Outside Bend | 5.7558e-05 | m |
| t_m_i | Minimum Required Thickness, Inside Bend | 6.26116e-05 | m |

---

## Disclaimer

While every effort has been made to ensure the accuracy and reliability of the calculations provided, we do not guarantee that the information is complete, up-to-date, or suitable for any specific purpose. Users must independently verify the results and assume full responsibility for any decisions or actions taken based on its output. Use of this calculator is entirely at your own risk, and we expressly disclaim any liability for errors or omissions in the information provided.

**Report Details:**
- **Generated Date:** September 26, 2025
- **Generated Using:** Qnty Library
- **Version:** Beta (Independent verification required for production use)

**Signatures:**

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Calculated By | _________________ | _________________ | _______ |
| Reviewed By | _________________ | _________________ | _______ |
| Approved By | _________________ | _________________ | _______ |

*Report generated using qnty library*