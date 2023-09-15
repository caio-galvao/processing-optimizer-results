install.packages("ggplot2")
install.packages("tidyverse")
library(tidyverse)
library(ggplot2)

od_vs_re <- read_csv("../od_vs_re.csv")
opt_vs_all_od <- read_csv("../opt_vs_all_od.csv")

head(od_vs_re)

# optimal vs all on demand -----------------------------------------------------

df <- opt_vs_all_od %>% dplyr::select(timeId, opt_cost)
df2 <- opt_vs_all_od %>% dplyr::select(timeId, all_od_cost)
df$type <- "Optimal"
df2$type <- "OnDemand"

colnames(df2)[2] <- 'cost'
colnames(df)[2] <- 'cost'

df <- rbind(df, df2)

head(df)
df <- mutate(df, timeId = floor(timeId / 168))
head(df)
summary(df)
table(df$type)
df <- df %>% group_by(timeId, type) %>% summarise(cost = sum(cost))
head(df)

ggplot(df, aes(x=timeId, y = cost, color = type)) +
  geom_line() +
  theme_minimal() +
  labs(x="Time (weeks)", y="Cost in Dollars", color = "Strategy") +
  ggtitle("Cost of optimal solution vs cost of all on demand")

# cumulative

c_df <- df %>% ungroup() %>% group_by(type) %>% mutate(c_cost = cumsum(cost)) %>% mutate(c_cost = c_cost / 1000000)
head(c_df)

ggplot(c_df, aes(x=timeId, y = c_cost, color = type)) +
  scale_x_continuous(breaks=c(0, 53, 105, 157),
                     labels=c("", "First year", "Second year", "Third year")) +
  geom_line() +
  theme_minimal() +
  labs(x="Week", y="Cost (millions of dollars)", color = "Strategy") +
  annotate(geom = "text", x = 160, y = 37, label = round(max(c_df$c_cost), 2)) +
  annotate(geom = "text", x = 160, y = 26, label = round(max(filter(c_df, type == "Optimal")$c_cost), 2)) +
  ggtitle("Cost of optimal solution vs cost of all on demand (cumulative)")


# reserve vs on demand ---------------------------------------------------------

df3 <- od_vs_re %>% dplyr::select(timeId, od_cost)
df4 <- od_vs_re %>% dplyr::select(timeId, res_cost)
df3$type <- "OnDemand"
df4$type <- "Reserve"

colnames(df3)[2] <- 'cost'
colnames(df4)[2] <- 'cost'

new_df <- rbind(df3, df4)

head(new_df)
new_df <- mutate(new_df, timeId = floor(timeId / 168))
head(new_df)
summary(new_df)
table(new_df$type)
new_df <- new_df %>% group_by(timeId, type) %>% summarise(cost = sum(cost))
head(new_df)

ggplot(new_df, aes(x=timeId, y = cost, color = type)) +
  geom_line() +
  theme_minimal() +
  labs(x="Time (weeks)", y="Cost in Dollars", color = "Market") +
  ggtitle("Cost of on demand vs cost of reserves in the optimal solution")

# cumulative

c_df2 <- new_df %>% ungroup() %>% group_by(type) %>% mutate(c_cost = cumsum(cost)) %>% mutate(c_cost = c_cost / 1000000)
head(c_df2)

ggplot(c_df2, aes(x=timeId, y = c_cost, color = type)) +
  scale_x_continuous(breaks=c(0, 53, 105, 157),
                   labels=c("", "First year", "Second year", "Third year")) +
  geom_line() +
  theme_minimal() +
  labs(x="Week", y="Cost (millions of dollars)", color = "Market") +
  annotate(geom = "text", x = 162, y = 16.5, label = round(max(c_df2$c_cost), 2)) +
  annotate(geom = "text", x = 162, y = 9, label = round(max(filter(c_df2, type == "OnDemand")$c_cost), 2)) +
  ggtitle("Cost of on demand vs cost of reserves in the optimal solution (cumulative)")