# Engineering Calculation Report: DynamicProblem

**Generated:** 2025-11-26 18:57:42

## 1. Known Variables

| Vector | Fₓ (N) | Fᵧ (N) | |F| (N) | θ (deg) | Reference |
| :--- | ---: | ---: | ---: | ---: | :--- |
| F₁ | 225.0 | 389.7 | 450.0 | 60.0 | +x |
| F₂ | -676.1 | -181.2 | 700.0 | 15.0 | -x |

## 2. Unknown Variables

| Vector | Fₓ (N) | Fᵧ (N) | |F| (N) | θ (deg) | Reference |
| :--- | ---: | ---: | ---: | ---: | :--- |
| Fᵣ | ? | ? | ? | ? | +x |

## 3. Equations Used

1. |Fᵣ|² = |F₁|² + |F₂|² + 2·|F₁|·|F₂|·cos(∠(F₁,F₂))

2. sin(∠(F₁,Fᵣ))/|F₂| = sin(∠(F₁,F₂))/|Fᵣ|

## 4. Step-by-Step Solution

### Step 1: Solve for ∠(F₁,F₂)

    ```
    ∠(F₁,F₂) = |θ_F₁ - θ_F₂|
    = |60° - 15°|
    = 45°
    ```

### Step 2: Solve for |Fᵣ| using Eq 1

    ```
    |Fᵣ| = sqrt((450.0)² + (700.0)² + 2(450.0)(700.0)cos(45°))
    = 497.0 N
    ```

### Step 3: Solve for ∠(F₁,Fᵣ) using Eq 2

    ```
    ∠(F₁,Fᵣ) = sin⁻¹(700.0·sin(45°)/497.0)
    = 95.2°
    ```

### Step 4: Solve for θ_Fᵣ with respect to +x

    ```
    θ_Fᵣ = θ_F₁ + ∠(F₁,Fᵣ)
    = 60.0° + 95.2°
    = 155.2°
    ```

## 5. Summary of Results

| Vector | Fₓ (N) | Fᵧ (N) | |F| (N) | θ (deg) | Reference |
| :--- | ---: | ---: | ---: | ---: | :--- |
| Fᵣ | -451.1 | 208.5 | 497.0 | 155.2 | +x |


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