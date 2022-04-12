# Call-centre-timeseries-data-analysis
Here we are analyzing incoming call records recorded over 12 month (from 1/01/99 till 31/12/99), at the telephone call-center of “Anonymous Bank” in Israel. Please check the documentation provided in the "data" folder that has more details on the source of the data, and its general description.

The data is free for use and you may also refer to below link to download directly from the site.

Data location : https://iew.technion.ac.il/serveng/callcenterdata/index.html

To start with, we would understand the data, try to figure out any trend. We would also try to fnd anything in the data that could indicate a problem and might need resolution. This is covered in detail in the notebook "01 Analyze Call logs" which was intially developed using matpltolib however use of plotlty appeared reasonable later, so you have both the next books. 

Once you go through the above notebook, you would notice that there are significant number of call drops , and we have also done a root cause analysis to understand the problem and potential solution.

Then we would see if we could analyze the calls received by the bank , recorded at each hour could be analyzed and forecasted. This is covered in the 2nd notebook "02 Time series forecasting - No of customer calls".

**Future work** : This repository would be updated as and when the work progress. Upcoming work/updates would involve
1) Use deep learning models to forecast customer calls 
2) Use of Linear programming to find best utilisation of agents time in order to reduce the call drops. Understand if call drops can be reduced by better shift allocation strategy assuming the same workforce to be available or alternatively if we are to reduce the overall call drops by x %, what would be an ideal shift allocation and whether we would need to increase the number of agents working in the call centre to meet the additional call volume.
