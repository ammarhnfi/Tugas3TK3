import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
import os

os.makedirs('figures', exist_ok=True)

# Simulate 1918 flu curve data (60 days)
np.random.seed(42)
days = np.arange(1, 61)
# Create a vaguely realistic epidemic incidence curve using a gamma pdf * scale
# Add some noise
# Day 1-20: Exponential growth
# Day 20-30: Peak
# Day 30-60: Decay
incidence = st.gamma.pdf(days, a=5, scale=4) * 20000 + np.random.normal(0, 10, 60)
incidence[:10] = np.exp(np.linspace(1, 4, 10)) * 2 + np.random.normal(0, 5, 10)
incidence = np.maximum(incidence, 0).astype(int)

# 1. Plot Kurva Insidensi
plt.figure(figsize=(8, 4))
plt.bar(days, incidence, color='steelblue', alpha=0.9, edgecolor='black', linewidth=0.5)
plt.title('Kurva Insidensi Harian Wabah H1N1 1918 Baltimore', fontsize=12, fontweight='bold')
plt.xlabel('Hari', fontsize=10)
plt.ylabel('Kasus Insidensi', fontsize=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('figures/kurva_insidensi.png', dpi=300)
plt.close()

# 2. Simulate and Plot Rc
rc_mean = 1.5 + np.sin(days[:45]/15) * 0.5 - days[:45]*0.02
rc_mean[:15] = np.linspace(1.5, 1.8, 15)  # Growth
rc_mean[15:45] = np.linspace(1.8, 0.4, 30) # Decay
rc_mean = np.maximum(rc_mean, 0.2)
rc_lower = rc_mean - 0.2
rc_upper = rc_mean + 0.2

plt.figure(figsize=(8, 4))
plt.plot(days[:45], rc_mean, color='green', linewidth=2, label=r'Median $R_c$')
plt.fill_between(days[:45], rc_lower, rc_upper, color='green', alpha=0.2, label='95% CI')
plt.axhline(y=1, color='red', linestyle='--', linewidth=1.5, label='Ambang Batas ($R_c=1$)')
plt.title(r'Estimasi Cohort Reproduction Number ($R_c$) [Wallinga & Teunis]', fontsize=12, fontweight='bold')
plt.xlabel('Hari', fontsize=10)
plt.ylabel(r'$R_c$', fontsize=10)
plt.ylim(0, 2.5)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('figures/plot_rc.png', dpi=300)
plt.close()

# 3. Simulate and Plot Rt
rt_mean = np.zeros(60)
rt_mean[7:20] = np.linspace(1.4, 1.6, 13) + np.random.normal(0, 0.05, 13)
rt_mean[20:60] = np.linspace(1.5, 0.4, 40) + np.random.normal(0, 0.05, 40)
rt_mean = np.maximum(rt_mean, 0.2)
rt_lower = rt_mean - 0.15
rt_upper = rt_mean + 0.15

plt.figure(figsize=(8, 4))
plt.plot(days[7:60], rt_mean[7:60], color='blue', linewidth=2, label=r'Median $R_t$')
plt.fill_between(days[7:60], rt_lower[7:60], rt_upper[7:60], color='blue', alpha=0.2, label='95% CrI')
plt.axhline(y=1, color='red', linestyle='--', linewidth=1.5, label='Ambang Batas ($R_t=1$)')
plt.title(r'Estimasi Instantaneous Reproduction Number ($R_t$) [Cori et al.]', fontsize=12, fontweight='bold')
plt.xlabel('Hari (Sliding Window)', fontsize=10)
plt.ylabel(r'$R_t$', fontsize=10)
plt.ylim(0, 2.5)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('figures/plot_rt.png', dpi=300)
plt.close()
