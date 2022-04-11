###
### Validation of data : Rules are based on the documentation provided along with the data
###

def validate_df(df_in):
    # Import libraries
    from collections import defaultdict
    from datetime import datetime
        
    # Try catch-block-1
    def tryconvert(value,func,valid_only=True):
        ret = True
        try:
            # if valid_only is true, function is only checking the error and not returning the output
            if valid_only==True :
                func(value)
            else :
                ret = func(value)
        except:
            ret = False
        return ret
       
    
    # Indexes
    ALL_index = set(df_in.index)
    valid_data_index = set()
    invalid_index = set()
    invalid_data_index = set()
    exception_index = defaultdict(set)
    
    # Take a copy
    df = df_in.copy()
        
    # Validate vru
    df['vru'] = df['vru+line'].apply(lambda x : x[0:4])
    valid_vru = ['AA01','AA02','AA03','AA04','AA05','AA06']
    invalid_index = set(df[~df['vru'].astype(str).isin(valid_vru)].index)
    invalid_data_index.update(invalid_index)
    exception_index['Invalid vru'] = invalid_index
        
    # validate line
    df['line'] = df['vru+line'].apply(lambda x : x[4:])
    valid_line = [str(r).zfill(2) for r in range(1,17,1)]
    invalid_index = set(df[~df['line'].astype(str).isin(valid_line)].index)
    invalid_data_index.update(invalid_index)
    exception_index['Invalid line'] = invalid_index
    
    #validate call_id
    invalid_index = set(df[~df['call_id'].astype(str).str.isdigit()].index)
    invalid_data_index.update(invalid_index)
    exception_index['Invalid call id'] = invalid_index
    
    #validate priority
    valid_priority = ['0','1','2']
    invalid_index = set(df[~df['priority'].astype(str).str.isdigit()].index)
    invalid_index.update(df[~df['priority'].astype(str).isin(valid_priority)].index)
    invalid_data_index.update(invalid_index)
    exception_index['Invalid priority'] = invalid_index
    
    #validate type
    valid_priority = ['PS','PE','IN','NE','NW','TT']
    invalid_index = set(df[~df['type'].astype(str).isin(valid_priority)].index)
    invalid_data_index.update(invalid_index)
    exception_index['Invalid type'] = invalid_index
    
    #validate date
    # date format check yymmdd
    invalid_index = set(df[~df.apply(lambda y: tryconvert(y,lambda x: \
                                  datetime.strptime(str(x['date']),'%y%m%d').date()\
                                 ),axis=1)].index)
    invalid_data_index.update(invalid_index)
    exception_index['Invalid date'] = invalid_index
    
    # Validate all time columns 
    time_columns = ['vru_entry', 'vru_exit','q_start', 'q_exit','ser_start', 'ser_exit',]
    for col in time_columns:
        # time format check HH:MM:SS
        invalid_index = set(df[~df.apply(lambda y: tryconvert(y,lambda x: \
                                  datetime.strptime(str(x[col]),'%H:%M:%S').time()\
                                 ),axis=1)].index)
        invalid_data_index.update(invalid_index)
        exception_index['Invalid '+ col] = invalid_index
    
    # validate all duration columns
    dur_columns = {'vru_time':['vru_entry', 'vru_exit'],'q_time':['q_start', 'q_exit'],'ser_time':['ser_start', 'ser_exit']}
    for col, [start,end] in dur_columns.items():   
        # check if time = duration (i.e. exit - start/entry) and duration is not negative
        invalid_index = set(df[~df.apply(lambda y: tryconvert(y, (lambda x: \
                                 ((datetime.strptime(str(x[end]),'%H:%M:%S') \
                - datetime.strptime(str(x[start]),'%H:%M:%S')).total_seconds()==float(x[col]))),valid_only=False)\
                                ,axis=1)].index)
        invalid_index.update(set(df[~df.apply(lambda y : tryconvert(y,(lambda x: float(x[col])>=0),valid_only=False),axis=1)].index))
        # [col].astype(float)<0    
        invalid_data_index.update(invalid_index)
        exception_index['Invalid '+ col] = invalid_index

    
    
    #validate outcome
    valid_outcome = ['AGENT','HANG','PHANTOM']
    invalid_index = set(df[~df['outcome'].astype(str).isin(valid_outcome)].index)
    invalid_data_index.update(invalid_index)
    exception_index['Invalid outcome'] = invalid_index
    
    #validate server
    # No validation rule identified
    

    
    # Indexes of valid data
    valid_data_index = set(ALL_index) - set(invalid_data_index) 
    
    return df_in.iloc[list(valid_data_index)], df_in.iloc[list(invalid_data_index)], exception_index



###
### Data Clean rules are based on the validation errors. The rules would be build in a iterative process.
### Data would cleaned first and then validated. Based on the errors, the cleaning rules would be revised. 
###

def clean_df(df):
    # Data Clean rules
    
    # priority : Strip leading blanks
    df['priority'] = df['priority'].astype(str).str.lstrip()
    
    
    # type : Strip leading blanks
    df['type'] = df['type'].astype(str).str.lstrip()
    
    return(df)


###
### Transformation - rules 01
###

def transform_df(df):
    # Import required package
    import calendar
    from datetime import datetime
    
    # time column    
    time_columns = ['vru_entry', 'vru_exit','q_start', 'q_exit','ser_start', 'ser_exit']
    for time_col in time_columns :
        df.loc[:,time_col] = df.apply(lambda x: datetime.strptime(str(x['date']) + ' ' + str(x[time_col]),'%y%m%d %H:%M:%S'),axis=1)
    
    # Call-Hour
    df.loc[:,'call_hour_start'] = df.apply(lambda x : x['vru_entry'].hour,axis=1)#dt.floor(str(t)+'S').apply(lambda x: x.time())
    
    # Call-Hour
    df.loc[:,'call_datehour_start'] = df.apply(lambda x: datetime.strptime(str(x['date']) + ' ' + str(x['vru_entry'].hour),\
                                                                           '%y%m%d %H'),axis=1)
    
    # Vru & time
    df['vru'] = df['vru+line'].apply(lambda x : x[0:4])
    df['line'] = df['vru+line'].apply(lambda x : x[5:])
        
    # Date
    df.loc[:,'date'] = df.apply(lambda x: datetime.strptime(str(x['date']),'%y%m%d'),axis=1)
    
    # Weekday
    df.loc[:,'Weekday'] = df.apply(lambda x: calendar.day_name[x['date'].weekday()],axis=1)
    
    #Week-no
    df.loc[:,'Weekno'] = df.apply(lambda x: x['date'].strftime("%U"),axis=1)
    
    #Month
    df.loc[:,'Month'] = df.apply(lambda x: x['date'].month,axis=1)

    
    return(df)