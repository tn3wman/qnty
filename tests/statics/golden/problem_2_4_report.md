# Engineering Calculation Report: Problem 2-4

**Generated:** {{GENERATED_DATETIME}}

## 1. Known Variables

<div align="center">

| Vector | $\|\vec{F}\|$ (N) | $\theta$ (deg) | Reference |
| :--- | ---: | ---: | :--- |
| $\vec{F_R}$ | 500.0 | 0.0 | -y |

</div>

## 2. Unknown Variables

<div align="center">

| Vector | $\|\vec{F}\|$ (N) | $\theta$ (deg) | Reference |
| :--- | ---: | ---: | :--- |
| $\vec{F_{AB}}$ | ? | -45.0 | -y |
| $\vec{F_{AC}}$ | ? | -30.0 | +x |

</div>

## 3. Equations Used

1. $\frac{|\vec{F_{AC}}|}{\sin(\angle(\vec{F_{AB}}, \vec{F_R}))} = \frac{|\vec{F_R}|}{\sin(\angle(\vec{F_{AC}}, \vec{F_{AB}}))}$

2. $\frac{|\vec{F_{AB}}|}{\sin(\angle(\vec{F_{AC}}, \vec{F_R}))} = \frac{|\vec{F_R}|}{\sin(\angle(\vec{F_{AC}}, \vec{F_{AB}}))}$

## 4. Step-by-Step Solution

**Step 1: Solve for $|\vec{F_{AC}}|$ using Eq 1**

$$
\begin{aligned}
|\vec{F_{AC}}| &= 500.0\ \text{N} \cdot \frac{\sin(45.0^{\circ})}{\sin(75.0^{\circ})} \\
&= 366.0\ \text{N} \\
\end{aligned}
$$

**Step 2: Solve for $|\vec{F_{AB}}|$ using Eq 2**

$$
\begin{aligned}
|\vec{F_{AB}}| &= 500.0\ \text{N} \cdot \frac{\sin(60.0^{\circ})}{\sin(75.0^{\circ})} \\
&= 448.3\ \text{N} \\
\end{aligned}
$$

## 5. Summary of Results

<div align="center">

| Vector | $\|\vec{F}\|$ (N) | $\theta$ (deg) | Reference |
| :--- | ---: | ---: | :--- |
| $\vec{F_{AB}}$ | 448.3 | -45.0 | -y |
| $\vec{F_{AC}}$ | 366.0 | -30.0 | +x |

</div>


---

## Disclaimer

While every effort has been made to ensure the accuracy and reliability of the calculations provided, we do not guarantee that the information is complete, up-to-date, or suitable for any specific purpose. Users must independently verify the results and assume full responsibility for any decisions or actions taken based on its output. Use of this calculator is entirely at your own risk, and we expressly disclaim any liability for errors or omissions in the information provided.

**Report Details:**
- **Generated Date:** {{GENERATED_DATE}}
- **Generated Using:** Qnty Library
- **Version:** Beta (Independent verification required for production use)

**Signatures:**

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Calculated By | _________________ | _________________ | _______ |
| Reviewed By | _________________ | _________________ | _______ |
| Approved By | _________________ | _________________ | _______ |

*Report generated using qnty library*