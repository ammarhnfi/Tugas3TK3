# ==========================================
# Script R untuk Tugas 3 Epidemiologi
# Kasus Kelompok A: Wabah H1N1 1918 Baltimore
# ==========================================
library(EpiEstim)
library(incidence)
library(ggplot2)

# ----- Bagian A: Akses & Eksplorasi Data -----
data("Flu1918")
cases <- Flu1918$incidence
dates <- seq(as.Date("1918-09-01"), by = "days", length.out = length(cases))
df <- data.frame(Date = dates, I = cases)

# Plot Epidemi
p_inc <- ggplot(df, aes(x = Date, y = I)) +
  geom_col(fill = "steelblue") +
  theme_minimal() +
  labs(
    title = "Kurva Insidensi: Wabah Flu 1918 Baltimore",
    y = "Kasus Baru Dirawat",
    x = "Hari"
  )
ggsave("figures/kurva_insidensi.png", p_inc, width = 8, height = 4, dpi = 300)

# ----- Bagian B: Estimasi Euler-Lotka (R0) -----
# Sub-jendela eksponensial awal (Misal index hari 10-16)
early_data <- df[10:16, ]
early_data$Day <- seq_len(nrow(early_data))

fit <- glm(I ~ Day, family = poisson(link = "log"), data = early_data)
r_growth <- coef(fit)["Day"]  # Ekstrak laju r
cat("Laju Eksponensial (r):", round(r_growth, 3), "\n")

# Persamaan Euler Log-Gamma. Asumsi SI: mean=2.6, sd=1.5
mu_si <- 2.6
sd_si <- 1.5
k <- (mu_si / sd_si)^2
theta <- (sd_si^2) / mu_si
r0_euler <- (1 + r_growth * theta)^k
cat("Estimasi R0 (Euler-Lotka):", round(r0_euler, 2), "\n")

# ----- Bagian C: Cohort Reproduction Number (Rc) -----
t_start <- seq(2, length(cases) - 6)
t_end <- seq(8, length(cases))

res_rc <- suppressWarnings(
  wallinga_teunis(
    cases,
    method = "parametric_si",
    config = list(mean_si = 2.6, std_si = 1.5, t_start = t_start, t_end = t_end)
  )
)

# Plot Rc
png("figures/plot_rc.png", width = 8, height = 8, units = "in", res = 300)
plot(res_rc, "all")
dev.off()

# ----- Bagian D: Instantaneous Reproduction Number (Rt) -----
res_rt <- estimate_R(
  cases,
  method = "parametric_si",
  config = make_config(
    list(mean_si = 2.6, std_si = 1.5, t_start = t_start, t_end = t_end)
  )
)

# Plot Rt
png("figures/plot_rt.png", width = 8, height = 4, units = "in", res = 300)
p_rt <- plot(res_rt, "R") +
  labs(title = "Estimated Instantaneous Reproduction Number (Rt)")
print(p_rt)
dev.off()
