"""
AI 命理解读模块
调用 DeepSeek API 对八字进行解读
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


def build_prompt(bazi_info: dict, user_name: str = "", extra_question: str = "") -> str:
    """构建发给 AI 的 prompt"""
    si_zhu = bazi_info["四柱"]
    wx_stat = bazi_info["五行统计"]
    yinli = bazi_info["阴历"]

    # 五行统计格式化
    wx_str = " | ".join([f"{k}:{v}" for k, v in wx_stat.items()])

    name_part = f"命主：{user_name}\n" if user_name else ""

    question_part = f"\n用户追问：{extra_question}" if extra_question else ""

    prompt = f"""你是一位精通中国传统命理学的大师，擅长八字分析、五行调候，语言生动有趣、温暖积极。

{name_part}【八字四柱】
年柱：{si_zhu['年柱']}　月柱：{si_zhu['月柱']}　日柱：{si_zhu['日柱']}　时柱：{si_zhu['时柱']}

【基本信息】
- 农历：{yinli['年']}年 {yinli['月']}月 {yinli['日']}日
- 生肖：{yinli['生肖']}
- 星座：{yinli['星座']}
- 日主：{bazi_info['日主']}（{bazi_info['日主五行']}）
- 五行分布：{wx_str}
- 最旺五行：{bazi_info['最旺五行']}　最弱五行：{bazi_info['最弱五行']}

请按以下结构给出分析（每段 2-4 句，语气轻松，适合 95/00 后年轻人阅读）：

🌟 **命格概述**
（整体格局评价，一句话点明命主特质）

💡 **性格特质**
（根据日主五行分析性格优势和潜在挑战）

🚀 **事业学业**
（适合的方向和领域，给出具体建议）

💰 **财运分析**
（财运走势和理财建议）

❤️ **感情缘分**
（感情风格和缘分特点）

🌈 **近期运势**
（当前流年运势提示，积极引导）

✨ **开运建议**
（根据五行缺失给出颜色、方向、数字等开运小技巧）

注意：
- 以娱乐和正能量为主，不做恐吓式预测
- 语气活泼，可以适当用 emoji
- 不超过 600 字{question_part}"""

    return prompt


def analyze_bazi(bazi_info: dict, user_name: str = "", extra_question: str = "") -> str:
    """
    调用 DeepSeek API 分析八字
    返回 AI 生成的命理解读文本
    """
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("未配置 DEEPSEEK_API_KEY，请在 .env 文件中设置")

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
    )

    prompt = build_prompt(bazi_info, user_name, extra_question)

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "你是一位专业的命理分析师，擅长将传统八字命理用现代年轻人喜欢的方式表达。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.8,   # 稍高一些，让回答更有趣味性
        max_tokens=1000,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    # 测试（需要配置好 .env）
    from bazi_calc import get_bazi
    bazi = get_bazi(1999, 8, 15, 10)
    result = analyze_bazi(bazi, user_name="小明")
    print(result)
