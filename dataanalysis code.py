from pandas.core.describe import DataFrameDescriber
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import traceback
from google.colab import drive


drive.mount('/content/drive/')

dfEducation = pd.read_csv('drive/My Drive/Cameron Summer Research/Data/Final Data/EducationDataFinal.csv')
dfLifestyle = pd.read_csv('drive/My Drive/Cameron Summer Research/Data/Final Data/LifestyleDataFinal.csv')
dfCooking = pd.read_csv('drive/My Drive/Cameron Summer Research/Data/Final Data/CookingDataFinal.csv')
dfGaming = pd.read_csv('drive/My Drive/Cameron Summer Research/Data/Final Data/GamingDataFinal.csv')
dfFitness = pd.read_csv('drive/My Drive/Cameron Summer Research/Data/Final Data/FitnessDataFinal.csv')
'''
dfAsmr = pd.read_csv('drive/My Drive/Cameron Summer Research/Data/Original/youtuberData_asmr_2018_2023.csv')
dfBeauty = pd.read_csv('drive/My Drive/Cameron Summer Research/Data/Original/youtuberData_beauty_2018_2023.csv')
dfReviews = pd.read_csv('drive/My Drive/Cameron Summer Research/Data/Original/youtuberData_reviews_2018_2023.csv')
dfVlog = pd.read_csv('drive/My Drive/Cameron Summer Research/Data/Original/youtuberData_vlog_2018_2023.csv')
'''
#remove vlog outlier
# dfVlog = dfVlog[dfVlog['Subscribers 2023'] < 105000000]

#dfs = [dfEducation, dfLifestyle, dfCooking, dfGaming, dfAsmr, dfBeauty, dfFitness, dfReviews, dfVlog]
dfs = [dfEducation, dfLifestyle, dfCooking, dfGaming, dfFitness]

for i in range(0, len(dfs)):
    dfs[i].dropna(subset=['Channel Name'], inplace=True)
    dfs[i].drop_duplicates(subset=['Channel Name'], inplace=True)
    dfs[i].reset_index(drop=True, inplace=True)

dfEducation['Search'] = 'education'
dfLifestyle['Search'] = 'lifestyle'
dfCooking['Search'] = 'cooking'
dfGaming['Search'] = 'gaming'
dfFitness['Search'] = 'fitness'
'''
dfAsmr['Search'] = 'asmr'
dfBeauty['Search'] = 'beauty'
dfReviews['Search'] = 'reviews'
dfVlog['Search'] = 'vlog'
'''

dfRaw = pd.concat(dfs)
dfRaw.reset_index(drop=True, inplace=True)
dfRaw['Earnings'] = dfRaw['Video Views 2023']*0.004

dfFiltered = dfRaw[dfRaw['User Creation Date'].str.contains("2015|2016|2017|2018") == True]
dfFiltered = dfFiltered[dfFiltered['Video Views 2018'].isnull()]
dfFiltered.reset_index(drop=True, inplace=True)
channelsRemoved = len(dfRaw.index) - len(dfFiltered.index)

dfEducationFiltered = dfFiltered[dfFiltered['Search'] == 'education']
dfLifestyleFiltered = dfFiltered[dfFiltered['Search'] == 'lifestyle']
dfCookingFiltered = dfFiltered[dfFiltered['Search'] == 'cooking']
dfGamingFiltered = dfFiltered[dfFiltered['Search'] == 'gaming']
dfFitnessFiltered = dfFiltered[dfFiltered['Search'] == 'fitness']
'''
dfAsmrFiltered = dfFiltered[dfFiltered['Search'] == 'asmr']
dfBeautyFiltered = dfFiltered[dfFiltered['Search'] == 'beauty']
dfReviewsFiltered = dfFiltered[dfFiltered['Search'] == 'reviews']
dfVlogFiltered = dfFiltered[dfFiltered['Search'] == 'vlog']
'''

#filtered = [dfEducationFiltered, dfLifestyleFiltered, dfCookingFiltered, dfGamingFiltered, dfAsmrFiltered, dfBeautyFiltered, dfFitnessFiltered, dfReviewsFiltered, dfVlogFiltered]
filtered = [dfEducationFiltered, dfLifestyleFiltered, dfCookingFiltered, dfGamingFiltered, dfFitnessFiltered]
for filter in filtered:
    filter.reset_index(drop=True, inplace=True)

dfSuccess = dfFiltered[dfFiltered['Subscribers 2023'] >= 10000000]
dfEducationSuccess = dfEducationFiltered[dfEducationFiltered['Subscribers 2023'] >= 10000000]
dfLifestyleSuccess = dfLifestyleFiltered[dfLifestyleFiltered['Subscribers 2023'] >= 10000000]
dfCookingSuccess = dfCookingFiltered[dfCookingFiltered['Subscribers 2023'] >= 10000000]
dfGamingSuccess = dfGamingFiltered[dfGamingFiltered['Subscribers 2023'] >= 10000000]
dfFitnessSuccess = dfFitnessFiltered[dfFitnessFiltered['Subscribers 2023'] >= 10000000]
'''
dfAsmrSuccess = dfAsmrFiltered[dfAsmrFiltered['Subscribers 2023'] >= 10000000]
dfBeautySuccess = dfBeautyFiltered[dfBeautyFiltered['Subscribers 2023'] >= 10000000]
dfReviewsSuccess = dfReviewsFiltered[dfReviewsFiltered['Subscribers 2023'] >= 10000000]
dfVlogSuccess = dfVlogFiltered[dfVlogFiltered['Subscribers 2023'] >= 10000000]
'''


#successes = [dfSuccess, dfEducationSuccess, dfLifestyleSuccess, dfCookingSuccess, dfGamingSuccess, dfAsmrSuccess, dfBeautySuccess, dfFitnessSuccess, dfReviewsSuccess, dfVlogSuccess]
successes = [dfSuccess, dfEducationSuccess, dfLifestyleSuccess, dfCookingSuccess, dfGamingSuccess, dfGamingSuccess]
for success in successes:
    success.reset_index(drop=True, inplace=True)

dfNotSuccess = dfFiltered[dfFiltered['Subscribers 2023'] <= 10000000]
dfEducationNotSuccess = dfEducationFiltered[dfEducationFiltered['Subscribers 2023'] <= 10000000]
dfLifestyleNotSuccess = dfLifestyleFiltered[dfLifestyleFiltered['Subscribers 2023'] <= 10000000]
dfCookingNotSuccess = dfCookingFiltered[dfCookingFiltered['Subscribers 2023'] <= 10000000]
dfGamingNotSuccess = dfGamingFiltered[dfGamingFiltered['Subscribers 2023'] <= 10000000]
dfFitnessNotSuccess = dfFitnessFiltered[dfFitnessFiltered['Subscribers 2023'] <= 10000000]
'''
dfAsmrNotSuccess = dfAsmrFiltered[dfAsmrFiltered['Subscribers 2023'] <= 10000000]
dfBeautyNotSuccess = dfBeautyFiltered[dfBeautyFiltered['Subscribers 2023'] <= 10000000]
dfReviewsNotSuccess = dfReviewsFiltered[dfReviewsFiltered['Subscribers 2023'] <= 10000000]
dfVlogNotSuccess = dfVlogFiltered[dfVlogFiltered['Subscribers 2023'] <= 10000000]
'''

#notSuccesses = [dfNotSuccess, dfEducationNotSuccess, dfLifestyleNotSuccess, dfCookingNotSuccess, dfGamingNotSuccess, dfAsmrNotSuccess, dfBeautyNotSuccess, dfFitnessNotSuccess, dfReviewsNotSuccess, dfVlogNotSuccess]
notSuccesses = [dfNotSuccess, dfEducationNotSuccess, dfLifestyleNotSuccess, dfCookingNotSuccess, dfFitnessNotSuccess]
for notSuccess in notSuccesses:
    notSuccess.reset_index(drop=True, inplace=True)

successRate = dfSuccess.shape[0]/dfFiltered.shape[0]
educationSuccessRate = dfEducationSuccess.shape[0]/dfEducationFiltered.shape[0]
lifestyleSuccessRate = dfLifestyleSuccess.shape[0]/dfLifestyleFiltered.shape[0]
cookingSuccessRate = dfCookingSuccess.shape[0]/dfCookingFiltered.shape[0]
gamingSuccessRate = dfGamingSuccess.shape[0]/dfGamingFiltered.shape[0]
fitnessSuccessRate = dfFitnessSuccess.shape[0]/dfFitnessFiltered.shape[0]
'''
asmrSuccessRate = len(dfAsmrSuccess.index)/len(dfAsmrFiltered.index)
beautySuccessRate = len(dfBeautySuccess.index)/len(dfBeautyFiltered.index)
reviewsSuccessRate = len(dfReviewsSuccess.index)/len(dfReviewsFiltered.index)
vlogSuccessRate = len(dfVlogSuccess.index)/len(dfVlogFiltered.index)
'''


#dfs = [dfEducation, dfLifestyle, dfCooking, dfGaming, dfAsmr, dfBeauty, dfFitness, dfReviews, dfVlog, dfFiltered]
dfs = [dfEducation, dfLifestyle, dfCooking, dfGaming, dfFitness, dfFiltered]

dfSummary = pd.DataFrame(columns=['Channel Search', 'Probability of Success', 'Average Earnings if Successful',
                                  'Average Earnings if not Successful', 'Number of Channels'])

dfSummary.loc[len(dfSummary.index)] = ['education', educationSuccessRate, dfEducationSuccess['Earnings'].mean(),
                                       dfEducationNotSuccess['Earnings'].mean(), dfEducationFiltered.shape[0]]
dfSummary.loc[len(dfSummary.index)] = ['lifestyle', lifestyleSuccessRate, dfLifestyleSuccess['Earnings'].mean(),
                                       dfLifestyleNotSuccess['Earnings'].mean(), dfLifestyleFiltered.shape[0]]
dfSummary.loc[len(dfSummary.index)] = ['cooking', cookingSuccessRate, dfCookingSuccess['Earnings'].mean(),
                                       dfCookingNotSuccess['Earnings'].mean(), dfCookingFiltered.shape[0]]
dfSummary.loc[len(dfSummary.index)] = ['gaming', gamingSuccessRate, dfGamingSuccess['Earnings'].mean(),
                                       dfGamingNotSuccess['Earnings'].mean(), dfGamingFiltered.shape[0]]
dfSummary.loc[len(dfSummary.index)] = ['fitness', fitnessSuccessRate, dfFitnessSuccess['Earnings'].mean(),
                                       dfFitnessNotSuccess['Earnings'].mean(), dfFitnessFiltered.shape[0]]
'''
dfSummary.loc[len(dfSummary.index)] = ['asmr', asmrSuccessRate, dfAsmrSuccess['Earnings'].mean(),
                                       dfAsmrNotSuccess['Earnings'].mean()]
dfSummary.loc[len(dfSummary.index)] = ['beauty', beautySuccessRate, dfBeautySuccess['Earnings'].mean(),
                                       dfBeautyNotSuccess['Earnings'].mean()]
dfSummary.loc[len(dfSummary.index)] = ['reviews', reviewsSuccessRate, dfReviewsSuccess['Earnings'].mean(),
                                       dfReviewsNotSuccess['Earnings'].mean()]
dfSummary.loc[len(dfSummary.index)] = ['vlog', vlogSuccessRate, dfVlogSuccess['Earnings'].mean(),
                                       dfVlogNotSuccess['Earnings'].mean()]
'''

dfSummary.loc[len(dfSummary.index)] = ['overall', successRate, dfSuccess['Earnings'].mean(),
                                       dfNotSuccess['Earnings'].mean(), dfFiltered.shape[0]]

'''
def create_histogram(df, colName):
    stack = traceback.extract_stack()
    filename, lineno, function_name, code = stack[-2]
    df_name = re.compile(r'\((.*?)\,.*$').search(code).groups()[0]
    df_name = df_name[2: len(df_name)]
    if df_name.find('Filtered') != -1:
        df_name = df_name[0: df_name.find('Filtered')]
    plt.hist(df[colName])
    plt.title('Distribution of ' + colName + ' among ' + df_name + ' channels made bewteen 2015-2018')
    plt.xlabel(colName)
    plt.savefig('drive/My Drive/Data/Graphs/' + df_name + '_' + colName + '.png')
    plt.close()

create_histogram(dfEducationFiltered, 'Earnings')
create_histogram(dfLifestyleFiltered, 'Earnings')
create_histogram(dfCookingFiltered, 'Earnings')
create_histogram(dfGamingFiltered, 'Earnings')
create_histogram(dfAsmrFiltered, 'Earnings')
create_histogram(dfBeautyFiltered, 'Earnings')
create_histogram(dfFitnessFiltered, 'Earnings')
create_histogram(dfReviewsFiltered, 'Earnings')
create_histogram(dfVlogFiltered, 'Earnings')

create_histogram(dfEducationSuccess, 'Earnings')
create_histogram(dfLifestyleSuccess, 'Earnings')
create_histogram(dfCookingSuccess, 'Earnings')
create_histogram(dfGamingSuccess, 'Earnings')
create_histogram(dfAsmrSuccess, 'Earnings')
create_histogram(dfBeautySuccess, 'Earnings')
create_histogram(dfFitnessSuccess, 'Earnings')
create_histogram(dfReviewsSuccess, 'Earnings')
create_histogram(dfVlogSuccess, 'Earnings')

create_histogram(dfEducationNotSuccess, 'Earnings')
create_histogram(dfLifestyleNotSuccess, 'Earnings')
create_histogram(dfCookingNotSuccess, 'Earnings')
create_histogram(dfGamingNotSuccess, 'Earnings')
create_histogram(dfAsmrNotSuccess, 'Earnings')
create_histogram(dfBeautyNotSuccess, 'Earnings')
create_histogram(dfFitnessNotSuccess, 'Earnings')
create_histogram(dfReviewsNotSuccess, 'Earnings')
create_histogram(dfVlogNotSuccess, 'Earnings')


create_histogram(dfEducationFiltered, 'Subscribers 2023')
create_histogram(dfLifestyleFiltered, 'Subscribers 2023')
create_histogram(dfCookingFiltered, 'Subscribers 2023')
create_histogram(dfGamingFiltered, 'Subscribers 2023')
create_histogram(dfAsmrFiltered, 'Subscribers 2023')
create_histogram(dfBeautyFiltered, 'Subscribers 2023')
create_histogram(dfFitnessFiltered, 'Subscribers 2023')
create_histogram(dfReviewsFiltered, 'Subscribers 2023')
create_histogram(dfVlogFiltered, 'Subscribers 2023')


plt.hist(dfFiltered['Earnings'], bins=30)
plt.title('Distribution of Earnings among channels made bewteen 2015-2018')
plt.xlabel('Earnings')
plt.savefig('drive/My Drive/Data/Graphs/Overall_Earnings.png')
plt.close()

plt.hist(dfSuccess['Earnings'], bins=30)
plt.title('Distribution of Earnings among Successful channels made bewteen 2015-2018')
plt.xlabel('Earnings')
plt.savefig('drive/My Drive/Data/Graphs/OverallSuccess_Earnings.png')
plt.close()

plt.hist(dfNotSuccess['Earnings'], bins=30)
plt.title('Distribution of Earnings among Not Successful channels made bewteen 2015-2018')
plt.xlabel('Earnings')
plt.savefig('drive/My Drive/Data/Graphs/OverallNotSuccess_Earnings.png')
plt.close()

plt.hist(dfFiltered['Subscribers 2023'], bins=30)
plt.title('Distribution of Subscribers 2023 among channels made bewteen 2015-2018')
plt.xlabel('Subscribers 2023')
plt.savefig('drive/My Drive/Data/Graphs/Overall_Subscribers 2023.png')
plt.close()

dfFilteredUnder40mil = dfFiltered[dfFiltered['Subscribers 2023'] <= 40000000]
x = np.array(dfFilteredUnder40mil['Subscribers 2023'])
y = np.array(dfFilteredUnder40mil['Earnings'])
a, b = np.polyfit(x, y, 1)
plt.scatter(x, y)
plt.plot(x, a*x+b)
plt.title('Subscribers vs Earnings among channels made between 2015-2018')
plt.xlabel('Subscribers')
plt.ylabel('Earnings')
plt.savefig('drive/My Drive/Data/Graphs/Overall_Subs_vs_Earnings.png')
plt.close()
'''

dfSummary.to_csv("drive/My Drive/Cameron Summer Research/Data/Final Data/SummaryStats.csv")
print('monkey')
