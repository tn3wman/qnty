# Engineering Calculation Report: DynamicProblem

**Generated:** 2025-11-26 16:41:29

## 1. Known Variables

| Symbol | X (N) | Y (N) | Magnitude (N) | Angle (deg) | Reference |
| :--- | ---: | ---: | ---: | ---: | :--- |
| F_1 | 225 | 389.711 | 450 | 60 | +x |
| F_2 | -676.148 | -181.173 | 700 | 15 | -x |

## 2. Unknown Variables

| Symbol | X (N) | Y (N) | Magnitude (N) | Angle (deg) | Reference |
| :--- | ---: | ---: | ---: | ---: | :--- |
| F_R | ? | ? | ? | ? | +x |

## 3. Equations Used

1. F_R² = F_1² + F_2² + 2·F_1·F_2·cos(θ)

2. sin(φ)/F_2 = sin(θ)/F_R

3. θ_F_R = θ_F_1 + φ

## 4. Step-by-Step Solution

### Step 1: Solve for |F_R|

    **Equation:**
    ```
    F_R² = F_1² + F_2² + 2·F_1·F_2·cos(θ)
    ```

    **Substitution:**
    ```
    F_R² = (450.000)² + (700.000)² + 2(450.000)(700.000)cos(45.0°)
    ```

    **Result:**
    ```
    |F_R| = 497.014 N
    ```

### Step 2: Solve for φ

    **Equation:**
    ```
    sin(φ)/F_2 = sin(θ)/F_R
    ```

    **Substitution:**
    ```
    sin(φ)/700.000 = sin(45.0°)/497.014
    ```

    **Result:**
    ```
    φ = 95.192 °
    ```

### Step 3: Solve for θ_F_R

    **Equation:**
    ```
    θ_F_R = θ_F_1 + φ
    ```

    **Substitution:**
    ```
    θ_F_R = 60.0° + (95.192°)
    ```

    **Result:**
    ```
    θ_F_R = 155.192 °
    ```

## 5. Summary of Results

| Symbol | Magnitude (N) | Angle (deg) | F_x (N) | F_y (N) |
| :--- | ---: | ---: | ---: | ---: |


---

## Disclaimer

While every effort has been made to ensure the accuracy and reliability of the calculations provided, we do not guarantee that the information is complete, up-to-date, or suitable for any specific purpose. Users must independently verify the results and assume full responsibility for any decisions or actions taken based on its output. Use of this calculator is entirely at your own risk, and we expressly disclaim any liability for errors or omissions in the information provided.

**Report Details:**
- **Generated Date:** November 26, 2025
- **Generated Using:** Qnty Library
- **Version:** Beta (Independent verification required for production use)

**Signatures:**

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Calculated By | _________________ | _________________ | _______ |
| Reviewed By | _________________ | _________________ | _______ |
| Approved By | _________________ | _________________ | _______ |

*Report generated using qnty library*