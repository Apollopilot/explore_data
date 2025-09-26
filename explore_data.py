import pandas as pd  
import matplotlib.pyplot as plt 
import seaborn as sns 

#load your dataset
df = pd.read_csv("/Users/austenrussell/Desktop/Python sterrf/cognitive_overload_ai/data/simulated_cognitive_data.csv")

#check the first few rows (sanity check)
print(df.head())

#plot distribution of mental effort
sns.set(style="whitegrid")
plt.figure(figsize=(8,5))
sns.histplot(data=df, x= 'mental_effort', kde=True, bins=20, color='royalblue')
plt.title('Distribution of Reported Mental Effort')
plt.xlabel('Mental Effort (1-10 scale)')
plt.ylabel('Count')
plt.tight_layout()
plt.show()
