import pandas as pd

def sort(dataframe, col : str) -> pd.DataFrame:
    if col == "experience_years" or col == 'experience_months':
        dataframe1 = pd.DataFrame(dataframe)
        dataframe1['experience_months'] += dataframe1['experience_years'] * 12
        dataframe1['experience_years'] = 0
        dataframe1 = dataframe1.sort_values(by='experience_months').reset_index(drop=True)
        dataframe1['experience_years'] = dataframe1['experience_months'] // 12
        dataframe1['experience_months'] = dataframe1['experience_months'] % 12
        return dataframe1

    else:
        return pd.DataFrame(sort(dataframe, col).reset_index(drop=True).iloc[0])


def getMax(dataframe, col: str):
    sorted_dataframe = pd.DataFrame(sort(dataframe, col).reset_index(drop=True))
    for i in range(1, len(sorted_dataframe[col])):
        try:
            int(sorted_dataframe[col][i])
        except Exception:
            try:
                return pd.DataFrame(sorted_dataframe.iloc[i - 1])
            except Exception:
                return None
    return pd.DataFrame(sort(dataframe, col).reset_index(drop=True).iloc[0])


def getAverage(dataframe, col: str):
    salary_list = []
    for i in dataframe[col]:
        try:
            salary_list.append(int(i))
        except Exception:
            continue
    try:
        return str(int(sum(salary_list) / len(salary_list))) + " KZT"
    except ZeroDivisionError:
        return "None"


def getOneRow(dataframe: pd.DataFrame, col, value):
    delete_list = list(i for i in range(
        len(dataframe[col])) if dataframe[col][i] != value)
    return dataframe.drop(delete_list).reset_index(drop=True)


def getSalary(group):
    group = group['salary']
    min = group.min()
    max = group.max()
    mean= group.mean()
    stats = pd.concat([min, max, mean], axis=1)
    stats.cols = ['min', 'max', 'average']

    return stats


def getAge(group):
    group = group['age']
    min = group.min()
    max = group.max()
    mean = group.mean()
    stats = pd.concat([min, max, mean], axis=1)
    stats.cols = ['min', 'max', 'average']

    return stats


def getSex(group):
    group = group['sex'].value_counts().unstack(fill_value=0)
    group = group.rename(cols={True: 'Мужчина', False: 'Женщина'})
    group.cols.name = None
    group.index.name = None

    return group