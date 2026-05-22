"""
八字计算模块 — 基于 lunar-python 库
根据阳历生日（年月日时）生成八字四柱
"""

from lunar_python import Solar


# 天干地支常量（用于五行分析）
TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

WUXING_TIANGAN = {
    "甲": "木", "乙": "木",
    "丙": "火", "丁": "火",
    "戊": "土", "己": "土",
    "庚": "金", "辛": "金",
    "壬": "水", "癸": "水",
}

WUXING_DIZHI = {
    "子": "水", "亥": "水",
    "寅": "木", "卯": "木",
    "午": "火", "巳": "火",
    "申": "金", "酉": "金",
    "辰": "土", "戌": "土", "丑": "土", "未": "土",
}


def get_bazi(year: int, month: int, day: int, hour: int) -> dict:
    """
    输入阳历年月日时，返回八字四柱信息
    hour: 0-23，按实际小时输入，内部会转换为时辰
    """
    # 将小时转换为时辰（每两小时一个时辰，子时从23点开始）
    # 保持原始小时，lunar_python 内部会处理
    solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
    lunar = solar.getLunar()
    bazi = lunar.getEightChar()

    # 四柱
    year_pillar = bazi.getYear()    # 年柱（天干+地支）
    month_pillar = bazi.getMonth()  # 月柱
    day_pillar = bazi.getDay()      # 日柱
    hour_pillar = bazi.getTime()    # 时柱

    # 拆分天干地支
    def split_pillar(pillar: str):
        return {"天干": pillar[0], "地支": pillar[1]}

    pillars = {
        "年柱": split_pillar(year_pillar),
        "月柱": split_pillar(month_pillar),
        "日柱": split_pillar(day_pillar),
        "时柱": split_pillar(hour_pillar),
    }

    # 计算五行统计
    wuxing_count = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}
    for pillar_name, pdata in pillars.items():
        tg = pdata["天干"]
        dz = pdata["地支"]
        if tg in WUXING_TIANGAN:
            wuxing_count[WUXING_TIANGAN[tg]] += 1
        if dz in WUXING_DIZHI:
            wuxing_count[WUXING_DIZHI[dz]] += 1

    # 日主（日柱天干）是命主
    ri_zhu = pillars["日柱"]["天干"]
    ri_zhu_wuxing = WUXING_TIANGAN.get(ri_zhu, "未知")

    # 找出最强和最弱五行
    max_wx = max(wuxing_count, key=wuxing_count.get)
    min_wx = min(wuxing_count, key=wuxing_count.get)

    return {
        "四柱": {
            "年柱": year_pillar,
            "月柱": month_pillar,
            "日柱": day_pillar,
            "时柱": hour_pillar,
        },
        "详细": pillars,
        "日主": ri_zhu,
        "日主五行": ri_zhu_wuxing,
        "五行统计": wuxing_count,
        "最旺五行": max_wx,
        "最弱五行": min_wx,
        "阴历": {
            "年": lunar.getYearInChinese(),
            "月": lunar.getMonthInChinese(),
            "日": lunar.getDayInChinese(),
            "生肖": lunar.getYearShengXiao(),
            "星座": solar.getXingZuo(),
        }
    }


if __name__ == "__main__":
    # 快速测试
    result = get_bazi(1999, 8, 15, 10)
    print("=== 八字测试 ===")
    for k, v in result.items():
        print(f"{k}: {v}")
