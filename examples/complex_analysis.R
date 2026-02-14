library(dplyr)

# Calculate monthly revenue retention and churn flags
customer_metrics <- raw_sales_data %>%
  filter(status == "completed" | status == "refunded", date >= "2023-01-01") %>%
  group_by(customer_id, month = format(date, "%Y-%m")) %>%
  summarize(
    total_spent = sum(amount, na.rm = TRUE),
    purchases = n(),
    .groups = 'drop'
  ) %>%
  arrange(customer_id, month) %>%
  group_by(customer_id) %>%
  mutate(
    previous_month_spend = lag(total_spent, n = 1, default = 0),
    is_churn_risk = if_else(previous_month_spend > 0 & total_spent == 0, TRUE, FALSE),
    customer_lifetime_value = cumsum(total_spent)
  ) %>%
  ungroup() %>%
  arrange(desc(total_spent))