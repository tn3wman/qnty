# Engineering Calculation Report: Problem 2-6

**Generated:** {{GENERATED_DATETIME}}

## 1. Known Variables

<div align="center">

| Vector | $\|\vec{F}\|$ (N) | $\theta$ (deg) | Reference |
| :--- | ---: | ---: | :--- |
| $\vec{F_1}$ | 4000.0 | -30.0 | $+v$ |
| $\vec{F_2}$ | 6000.0 | -30.0 | $+u$ |

</div>

## 2. Unknown Variables

<div align="center">

| Vector | $\|\vec{F}\|$ (N) | $\theta$ (deg) | Reference |
| :--- | ---: | ---: | :--- |
| $\vec{F_R}$ | ? | ? | $+u$ |

</div>

## 3. Equations Used

1. $|\vec{F_R}|^2 = |\vec{F_1}|^2 + |\vec{F_2}|^2 - 2 \cdot |\vec{F_1}| \cdot |\vec{F_2}| \cdot \cos(\angle(\vec{F_1}, \vec{F_2}))$

2. $\frac{\sin(\angle(\vec{F_1}, \vec{F_R}))}{|\vec{F_2}|} = \frac{\sin(\angle(\vec{F_1}, \vec{F_2}))}{|\vec{F_R}|}$

## 4. Step-by-Step Solution

**Step 1: Solve for $\angle(\vec{F_1}, \vec{F_2})$**

$$
\begin{aligned}
\angle(\vec{F_1}, \vec{F_2}) &= |\angle(\vec{v}, \vec{F_1})| + |\angle(\vec{u}, \vec{F_2})| \\
&= |(-30^{\circ})| + |(-30^{\circ})| \\
&= 30^{\circ} + 30^{\circ} \\
&= 105^{\circ} \\
\end{aligned}
$$

**Step 2: Solve for $|\vec{F_R}|$ using Eq 1**

$$
\begin{aligned}
|\vec{F_R}| &= \sqrt{(4000.0\ \text{N})^2 + (6000.0\ \text{N})^2 - 2(4000.0\ \text{N})(6000.0\ \text{N})\cos(105.0^{\circ})} \\
&= 8026.4\ \text{N} \\
\end{aligned}
$$

**Step 3: Solve for $\angle(\vec{F_1}, \vec{F_R})$ using Eq 2**

$$
\begin{aligned}
\angle(\vec{F_1}, \vec{F_R}) &= \sin^{-1}(6000.0\ \text{N} \cdot \frac{\sin(105.0^{\circ})}{8026.4\ \text{N}}) \\
&= 46.2^{\circ} \\
\end{aligned}
$$

**Step 4: Solve for $\angle(\vec{u}, \vec{F_R})$ with respect to +u**

$$
\begin{aligned}
\angle(\vec{u}, \vec{F_R}) &= \angle(\vec{u}, \vec{F_1}) - \angle(\vec{F_1}, \vec{F_R}) \\
&= 45.0^{\circ} - 46.2^{\circ} \\
&= -1.2^{\circ} \\
\end{aligned}
$$

## 5. Summary of Results

<div align="center">

| Vector | $\|\vec{F}\|$ (N) | $\theta$ (deg) | Reference |
| :--- | ---: | ---: | :--- |
| $\vec{F_R}$ | 8026.4 | -1.2 | $+u$ |

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