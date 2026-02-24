# 文档引用：PROJECT_SPEC.md - 1562行
# 奇门常量（八门、九星、八神等）

# 八门（人盘）
EIGHT_DOORS = [
    "开门", "休门", "生门", "伤门",
    "杜门", "景门", "死门", "惊门"
]

# 九星（天盘）
NINE_STARS = [
    "天蓬星", "天任星", "天冲星", "天辅星",
    "天英星", "天芮星", "天柱星", "天心星", "天禽星"
]

# 八神（神盘）
EIGHT_GODS = [
    "值符", "腾蛇", "太阴", "六合",
    "白虎", "玄武", "九地", "九天"
]

# 八宫（地盘）
EIGHT_PALACES = [
    {"name": "坎1", "direction": "正北", "position": 1},
    {"name": "坤2", "direction": "西南", "position": 2},
    {"name": "震3", "direction": "正东", "position": 3},
    {"name": "巽4", "direction": "东南", "position": 4},
    {"name": "中5", "direction": "中央", "position": 5},
    {"name": "乾6", "direction": "西北", "position": 6},
    {"name": "兑7", "direction": "正西", "position": 7},
    {"name": "艮8", "direction": "东北", "position": 8},
    {"name": "离9", "direction": "正南", "position": 9}
]

# 天干
STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

# 地支
BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 12时辰及时间范围
SHICHEN = [
    {"name": "子时", "time_range": "23:00-01:00", "hour": 23},
    {"name": "丑时", "time_range": "01:00-03:00", "hour": 1},
    {"name": "寅时", "time_range": "03:00-05:00", "hour": 3},
    {"name": "卯时", "time_range": "05:00-07:00", "hour": 5},
    {"name": "辰时", "time_range": "07:00-09:00", "hour": 7},
    {"name": "巳时", "time_range": "09:00-11:00", "hour": 9},
    {"name": "午时", "time_range": "11:00-13:00", "hour": 11},
    {"name": "未时", "time_range": "13:00-15:00", "hour": 13},
    {"name": "申时", "time_range": "15:00-17:00", "hour": 15},
    {"name": "酉时", "time_range": "17:00-19:00", "hour": 17},
    {"name": "戌时", "time_range": "19:00-21:00", "hour": 19},
    {"name": "亥时", "time_range": "21:00-23:00", "hour": 21}
]

# 吉凶等级
FORTUNE_LEVELS = {
    "大吉": 5.0,
    "中吉": 4.0,
    "平": 3.0,
    "凶": 2.0,
    "大凶": 1.0
}

# 节气列表（24节气）
SOLAR_TERMS = [
    "立春", "雨水", "惊蛰", "春分", "清明", "谷雨",
    "立夏", "小满", "芒种", "夏至", "小暑", "大暑",
    "立秋", "处暑", "白露", "秋分", "寒露", "霜降",
    "立冬", "小雪", "大雪", "冬至", "小寒", "大寒"
]
