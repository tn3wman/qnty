# Engineering Calculation Report: Problem 2-12

**Generated:** {{GENERATED_DATETIME}}

## 1. Known Variables

<div align="center">

| Vector | $\|\vec{F}\|$ (N) | $\theta$ (deg) | Reference |
| :--- | ---: | ---: | :--- |
| $\vec{F_B}$ | 6000.0 | 40.0 | $-y$ |

</div>

## 2. Unknown Variables

<div align="center">

| Vector | $\|\vec{F}\|$ (N) | $\theta$ (deg) | Reference |
| :--- | ---: | ---: | :--- |
| $\vec{F_A}$ | 8000.0 | ? | $+y$ |
| $\vec{F_R}$ | ? | 0.0 | $+x$ |

</div>

## 3. Equations Used

1. $\frac{\sin(\angle(\vec{F_A}, \vec{F_R}))}{|\vec{F_B}|} = \frac{\sin(\angle(\vec{F_A}, \vec{F_B}))}{|\vec{F_A}|}$

2. $|\vec{F_R}|^2 = |\vec{F_A}|^2 + |\vec{F_B}|^2 - 2 \cdot |\vec{F_A}| \cdot |\vec{F_B}| \cdot \cos(\angle(\vec{F_A}, \vec{F_B}))$

## 4. Step-by-Step Solution

**Step 1: Solve for $\angle(\vec{F_A}, \vec{F_R})$ using Eq 1**

$$
\begin{aligned}
\angle(\vec{F_A}, \vec{F_R}) &= \sin^{-1}(6000.0\ \text{N} \cdot \frac{\sin(50.0^{\circ})}{8000.0\ \text{N}}) \\
&= 35.1^{\circ} \\
\end{aligned}
$$

**Step 2: Solve for $\angle(y, \vec{F_A})$ with respect to +y**

$$
\begin{aligned}
\angle(y, \vec{F_A}) &= 90^{\circ} - \angle(\vec{F_R}, \vec{F_A}) \\
&= 90^{\circ} - 35.1^{\circ} \\
&= 54.9^{\circ} \\
\end{aligned}
$$

**Step 3: Solve for $Interior angle opposite F_R$**

$$
\begin{aligned}
180° - 50.0^{\circ} - 35.1^{\circ} = 94.9^{\circ} \\
\end{aligned}
$$

**Step 4: Solve for $|\vec{F_R}|$ using Eq 2**

$$
\begin{aligned}
|\vec{F_R}| &= \sqrt{(8000.0\ \text{N})^2 + (6000.0\ \text{N})^2 - 2(8000.0\ \text{N})(6000.0\ \text{N})\cos(94.9^{\circ})} \\
&= 10404.6\ \text{N} \\
\end{aligned}
$$

## 5. Summary of Results

<div align="center">

| Vector | $\|\vec{F}\|$ (N) | $\theta$ (deg) | Reference |
| :--- | ---: | ---: | :--- |
| $\vec{F_A}$ | 8000.0 | 305.1 | $+y$ |
| $\vec{F_R}$ | 10404.6 | 0.0 | $+x$ |

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