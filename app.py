from flask import Flask, render_template, request
import datetime
from collections import Counter

app = Flask(__name__)

# 这里粘贴之前的命理算法函数（简化版）
heavenly_stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
earthly_branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
# ...（复制之前定义的算法函数）

def get_year_bazi(year):
    base_year = 1984
    offset = year - base_year
    tg_index = offset % 10
    db_index = offset % 12
    return heavenly_stems[tg_index], earthly_branches[db_index]

def get_month_bazi(year, month):
    month_tg_index = (year * 12 + month) % 10
    month_db_index = (month + 2) % 12
    return heavenly_stems[month_tg_index], earthly_branches[month_db_index]

def get_day_bazi(birthday):
    days_since_base = (birthday - datetime.date(1900,1,1)).days
    tg_index = days_since_base % 10
    db_index = days_since_base % 12
    return heavenly_stems[tg_index], earthly_branches[db_index]

def get_hour_bazi(hour):
    index = (hour + 1) // 2
    tg_index = index % 10
    db_index = index % 12
    return heavenly_stems[tg_index], earthly_branches[db_index]

def analyze_five_elements(bazi):
    def get_element_from_tg(tg):
        if tg in ['甲', '乙']: return '木'
        elif tg in ['丙', '丁']: return '火'
        elif tg in ['戊', '己']: return '土'
        elif tg in ['庚', '辛']: return '金'
        elif tg in ['壬', '癸']: return '水'

    def get_element_from_db(db):
        if db in ['子', '亥']: return '水'
        elif db in ['丑', '未', '辰', '戌']: return '土'
        elif db in ['寅', '卯']: return '木'
        elif db in ['巳', '午']: return '火'
        elif db in ['申', '酉']: return '金'

    elements = []
    for tg, db in bazi:
        elements.append(get_element_from_tg(tg))
        elements.append(get_element_from_db(db))
    counts = Counter(elements)
    return counts

def get_liunian(year, birth_year):
    diff = year - birth_year
    if diff % 10 in [1, 6]:
        return "今年是你的大运之年，运势较佳。"
    elif diff % 10 in [3, 8]:
        return "今年运势平稳，但需注意健康。"
    else:
        return "今年可能遇到一些挑战，要多注意调整。"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        name = request.form['name']
        sex = request.form['sex']
        birthday_str = request.form['birthday']
        time_str = request.form['time']

        try:
            birthday = datetime.datetime.strptime(birthday_str, "%Y-%m-%d").date()
        except:
            result = "日期格式有误！"
            return render_template('index.html', result=result)

        if time_str.strip() == "":
            hour = 12
        else:
            try:
                hour = int(time_str.split(':')[0])
            except:
                result = "时间格式有误！"
                return render_template('index.html', result=result)

        # 计算四柱
        year_tg, year_db = get_year_bazi(birthday.year)
        month_tg, month_db = get_month_bazi(birthday.year, birthday.month)
        day_tg, day_db = get_day_bazi(birthday)
        hour_tg, hour_db = get_hour_bazi(hour)

        bazi = [(year_tg, year_db), (month_tg, month_db), (day_tg, day_db), (hour_tg, hour_db)]
        element_counts = analyze_five_elements(bazi)
        current_year = datetime.datetime.now().year
        prediction = get_liunian(current_year, birthday.year)

        result = {
            'name': name,
            'sex': sex,
            'bazi': bazi,
            'elements': element_counts,
            'prediction': prediction
        }

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
