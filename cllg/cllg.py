import pandas
from thefuzz import fuzz, process

SELECT_COLUMNS = ["UNITID", "CITY", "CONTROL", "CCBASIC", "CCUGPROF", "ADM_RATE_ALL", "SATVR75", "SATMT75", "SATMTMID", "SAT_AVG_ALL", "UGDS", "UGDS_WHITE", "UGDS_ASIAN", "TUITIONFEE_IN", "TUITIONFEE_OUT"]
college_db = pandas.read_csv("cllg/data.csv", low_memory=True)
db_instnm = college_db.set_index("INSTNM")
columns = college_db.iloc[:, 3] # select all columns in row 0

def get_sheet(colleges):
    all_names = list()
    first_college_name = colleges.pop(0)
    first_college_name = process.extractOne(first_college_name, list(columns))[0] # try fuzzy match
    print(f"Matched input to '{first_college_name}'")
    all_names.append(first_college_name)
    main_db = db_instnm.loc[first_college_name, :]
    main_db = main_db.loc[SELECT_COLUMNS]

    for college_name in colleges:
        college_name = process.extractOne(college_name, list(columns))[0]
        print(f"Matched input to '{college_name}'")
        all_names.append(college_name)
        college_info = db_instnm.loc[college_name, :].loc[SELECT_COLUMNS]
        main_db = pandas.merge(main_db, college_info, left_index=True, right_index=True)

    main_db.to_excel("cllg/colleges.xlsx")
    return ", ".join(all_names)