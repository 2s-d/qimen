# 文档引用：PROJECT_SPEC.md - 1561行
# 解读模板库（运势解读文案）

from typing import Dict, Any, List
import random
from app.modules.qimen.constants import FORTUNE_LEVELS

# 运势文案模板库（按星级1-5存储各类运势文案模板）
FORTUNE_TEMPLATES = {
    "career": {
        5.0: "事业运势极佳，适合开展新项目，贵人相助，事半功倍。此时正是事业发展的黄金时期，把握机会，勇往直前，必将取得重大突破。",
        4.5: "事业运势良好，工作顺利，团队协作融洽。适合制定长期规划，推进重要项目。保持积极态度，稳扎稳打，定能获得理想成果。",
        4.0: "事业运势良好，适合开展新项目，贵人相助，事半功倍。工作中遇到困难时，会有贵人及时相助，化解危机。",
        3.5: "事业运势平稳，工作按部就班，没有太大起伏。保持现状，稳步发展即可。注意与同事沟通，避免不必要的误会。",
        3.0: "事业运势平稳，按部就班，没有太大起伏。适合处理日常事务，不宜进行重大决策。保持耐心，等待更好的时机。",
        2.5: "事业运势欠佳，工作中可能遇到阻碍。需要谨慎行事，避免冲动决策。多听取他人意见，寻求帮助。",
        2.0: "事业运势欠佳，需谨慎行事，避免重大决策。工作中可能遇到阻碍，需要保持冷静，寻找解决方案。",
        1.5: "事业运势不佳，工作中困难较多。宜守不宜攻，保持低调，等待时机。避免与人发生冲突，注意人际关系。",
        1.0: "事业运势不佳，宜守不宜攻。此时不宜进行重大决策或开展新项目。保持低调，等待更好的时机到来。"
    },
    "wealth": {
        5.0: "财运极佳，正财偏财皆有收获。适合进行投资理财，但需谨慎选择项目。把握机会，合理规划，财富将稳步增长。",
        4.5: "财运良好，收入稳定增长。适合进行小额投资，但需做好风险评估。保持理性消费，积累财富。",
        4.0: "财运良好，收入稳定，适合进行理财规划。可以适当进行小额投资，但需谨慎选择项目，避免高风险操作。",
        3.5: "财运平稳，收支平衡。适合进行储蓄规划，不宜大额投资。保持理性消费，避免不必要的开支。",
        3.0: "财运平稳，不宜大额投资，可小额理财。保持收支平衡，避免冲动消费。适合进行长期理财规划。",
        2.5: "财运一般，需谨慎理财。避免高风险投资，保持理性消费。注意控制开支，做好财务规划。",
        2.0: "财运欠佳，需谨慎理财，避免高风险投资。注意控制开支，避免不必要的消费。保持理性，等待更好的时机。",
        1.5: "财运不佳，需谨慎处理财务问题。避免大额支出，保持理性消费。注意防范财务风险，做好应急准备。",
        1.0: "财运不佳，需谨慎处理财务问题。避免大额投资和支出，保持理性消费。注意防范财务风险，做好应急准备。"
    },
    "love": {
        5.0: "感情运势极佳，单身者有望遇到心仪对象，恋爱中的人感情升温。此时是表白和求婚的好时机，把握机会，勇敢表达心意。",
        4.5: "感情运势良好，单身者桃花运旺盛，恋爱中的人感情稳定。适合与伴侣深入交流，增进感情。保持真诚，收获美好爱情。",
        4.0: "感情运势良好，单身者有望遇到心仪对象，恋爱中的人感情稳定。适合与伴侣深入交流，增进感情。",
        3.5: "感情运势平稳，单身者需主动出击，恋爱中的人保持现状。适合与伴侣沟通，增进了解。保持耐心，等待更好的时机。",
        3.0: "感情运势平稳，单身者需主动出击，恋爱中的人保持现状。适合与伴侣沟通，增进了解。",
        2.5: "感情运势一般，需注意与伴侣的沟通。避免因小事发生争执，保持理解和包容。单身者需耐心等待，不宜强求。",
        2.0: "感情运势欠佳，需注意与伴侣的沟通，避免因小事发生争执。单身者需耐心等待，不宜强求。",
        1.5: "感情运势不佳，需注意与伴侣的关系。避免因小事发生冲突，保持理解和包容。单身者需耐心等待，不宜强求。",
        1.0: "感情运势不佳，需注意与伴侣的关系。避免因小事发生冲突，保持理解和包容。单身者需耐心等待，不宜强求。"
    },
    "health": {
        5.0: "健康运势极佳，身体状态良好，精力充沛。适合进行体育锻炼，增强体质。保持规律作息，健康饮食，身体将更加健康。",
        4.5: "健康运势良好，身体状态稳定。适合进行适度运动，保持身心健康。注意饮食规律，避免过度劳累。",
        4.0: "健康运势良好，身体状态稳定。适合进行适度运动，保持身心健康。注意饮食规律，避免过度劳累。",
        3.5: "健康运势平稳，需注意休息，避免过度劳累。适合进行轻度运动，保持身心健康。注意饮食规律，避免熬夜。",
        3.0: "注意休息，避免过度劳累，适当运动。保持规律作息，健康饮食，身体将保持良好状态。",
        2.5: "健康运势一般，需注意身体保养。避免过度劳累，保持规律作息。如有不适，及时就医。",
        2.0: "健康运势欠佳，需注意身体保养，避免过度劳累。保持规律作息，健康饮食，如有不适，及时就医。",
        1.5: "健康运势不佳，需特别注意身体保养。避免过度劳累，保持规律作息。如有不适，及时就医，不可拖延。",
        1.0: "健康运势不佳，需特别注意身体保养。避免过度劳累，保持规律作息。如有不适，及时就医，不可拖延。"
    }
}

def get_fortune_text(score: float, fortune_type: str) -> str:
    """
    根据星级和类型获取文案
    文档引用：PROJECT_SPEC.md - 1561行
    """
    # 将评分四舍五入到最近的0.5
    rounded_score = round(score * 2) / 2
    
    # 确保评分在1.0-5.0范围内
    if rounded_score < 1.0:
        rounded_score = 1.0
    elif rounded_score > 5.0:
        rounded_score = 5.0
    
    templates = FORTUNE_TEMPLATES.get(fortune_type, {})
    return templates.get(rounded_score, templates.get(3.0, "运势平稳，保持现状即可。"))

def get_overall_fortune(plate_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    根据盘面计算总体运势
    文档引用：PROJECT_SPEC.md - 5.2.1节步骤4
    """
    # 简化计算：根据值符值使和宫位吉凶计算总体评分
    palaces = plate_data.get("palaces", [])
    
    # 计算平均吉凶分数
    fortune_scores = []
    for palace in palaces:
        fortune = palace.get("fortune", "平")
        score = FORTUNE_LEVELS.get(fortune, 3.0)
        fortune_scores.append(score)
    
    if fortune_scores:
        overall_score = sum(fortune_scores) / len(fortune_scores)
    else:
        overall_score = 3.0
    
    # 确定总体吉凶
    if overall_score >= 4.5:
        overall_fortune = "大吉"
    elif overall_score >= 3.5:
        overall_fortune = "中吉"
    elif overall_score >= 2.5:
        overall_fortune = "平"
    elif overall_score >= 1.5:
        overall_fortune = "凶"
    else:
        overall_fortune = "大凶"
    
    return {
        "overall_score": round(overall_score, 1),
        "overall_fortune": overall_fortune
    }

def get_career_fortune(plate_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    计算事业运
    文档引用：PROJECT_SPEC.md - 5.2.1节步骤4
    """
    overall = get_overall_fortune(plate_data)
    score = overall["overall_score"]
    
    # 根据值符值使调整事业运评分
    chief_star = plate_data.get("chief_star", "")
    if "天心" in chief_star or "天辅" in chief_star:
        score = min(5.0, score + 0.5)
    elif "天芮" in chief_star or "天柱" in chief_star:
        score = max(1.0, score - 0.5)
    
    return {
        "score": round(score, 1),
        "text": get_fortune_text(score, "career")
    }

def get_wealth_fortune(plate_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    计算财运
    文档引用：PROJECT_SPEC.md - 5.2.1节步骤4
    """
    overall = get_overall_fortune(plate_data)
    score = overall["overall_score"]
    
    # 根据值使调整财运评分
    chief_door = plate_data.get("chief_door", "")
    if "生门" in chief_door:
        score = min(5.0, score + 0.5)
    elif "死门" in chief_door or "惊门" in chief_door:
        score = max(1.0, score - 0.5)
    
    return {
        "score": round(score, 1),
        "text": get_fortune_text(score, "wealth")
    }

def get_love_fortune(plate_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    计算感情运
    文档引用：PROJECT_SPEC.md - 5.2.1节步骤4
    """
    overall = get_overall_fortune(plate_data)
    score = overall["overall_score"]
    
    # 根据神盘调整感情运评分
    palaces = plate_data.get("palaces", [])
    for palace in palaces:
        if palace.get("god") == "六合":
            score = min(5.0, score + 0.5)
            break
        elif palace.get("god") == "白虎" or palace.get("god") == "玄武":
            score = max(1.0, score - 0.3)
    
    return {
        "score": round(score, 1),
        "text": get_fortune_text(score, "love")
    }

def get_health_fortune(plate_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    计算健康运
    文档引用：PROJECT_SPEC.md - 5.2.1节步骤4
    """
    overall = get_overall_fortune(plate_data)
    score = overall["overall_score"]
    
    # 根据值符调整健康运评分
    chief_star = plate_data.get("chief_star", "")
    if "天心" in chief_star:
        score = min(5.0, score + 0.5)
    elif "天芮" in chief_star:
        score = max(1.0, score - 0.5)
    
    return {
        "score": round(score, 1),
        "text": get_fortune_text(score, "health")
    }

def get_notices(plate_data: Dict[str, Any]) -> List[str]:
    """
    生成注意事项（3-5条）
    文档引用：PROJECT_SPEC.md - 5.2.1节步骤4
    """
    notices = []
    
    # 根据值符值使生成注意事项
    chief_star = plate_data.get("chief_star", "")
    chief_door = plate_data.get("chief_door", "")
    
    if "天蓬" in chief_star:
        notices.append("避免与人争执，保持冷静")
    if "天芮" in chief_star:
        notices.append("注意身体健康，避免过度劳累")
    if "死门" in chief_door:
        notices.append("避免重大决策，宜静不宜动")
    if "惊门" in chief_door:
        notices.append("注意财物安全，谨慎投资")
    
    # 根据宫位吉凶生成注意事项
    palaces = plate_data.get("palaces", [])
    bad_palaces = [p for p in palaces if p.get("fortune") in ["凶", "大凶"]]
    if bad_palaces:
        notices.append("避免前往不利方位，注意安全")
    
    # 确保有3-5条
    default_notices = [
        "保持积极心态，把握机会",
        "注意人际关系，避免冲突",
        "合理安排时间，劳逸结合",
        "谨慎决策，三思而后行",
        "保持耐心，等待更好的时机"
    ]
    
    while len(notices) < 3:
        notice = random.choice(default_notices)
        if notice not in notices:
            notices.append(notice)
    
    if len(notices) > 5:
        notices = notices[:5]
    
    return notices
