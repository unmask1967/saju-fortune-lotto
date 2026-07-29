import datetime
from korean_lunar_calendar import KoreanLunarCalendar

# ---------------------------------------------------------
# 1. 천간/지지 오행 및 한자/한글 매핑
# ---------------------------------------------------------
GAN_INFO = {
    "갑": ("목", True),  "甲": ("목", True),
    "을": ("목", False), "乙": ("목", False),
    "병": ("화", True),  "丙": ("화", True),
    "정": ("화", False), "丁": ("화", False),
    "무": ("토", True),  "戊": ("토", True),
    "기": ("토", False), "己": ("토", False),
    "경": ("금", True),  "庚": ("금", True),
    "신": ("금", False), "辛": ("금", False),
    "임": ("수", True),  "壬": ("수", True),
    "계": ("수", False), "癸": ("수", False)
}

ZI_ELEMENT = {
    "자": "수", "子": "수", "축": "토", "丑": "토",
    "인": "목", "寅": "목", "묘": "목", "卯": "목",
    "진": "토", "辰": "토", "사": "화", "巳": "화",
    "오": "화", "午": "화", "미": "토", "未": "토",
    "신": "금", "申": "금", "유": "금", "酉": "금",
    "술": "토", "戌": "토", "해": "수", "亥": "수"
}

OVERCOMES = {"목": "토", "토": "수", "수": "화", "화": "금", "금": "목"}

CHEON_EUL = {
    "갑": ["축", "미", "丑", "未"], "甲": ["축", "미", "丑", "未"],
    "을": ["자", "신", "子", "申"], "乙": ["자", "신", "子", "申"],
    "병": ["해", "유", "亥", "酉"], "丙": ["해", "유", "亥", "酉"],
    "정": ["해", "유", "亥", "酉"], "丁": ["해", "유", "亥", "酉"],
    "무": ["축", "미", "丑", "未"], "戊": ["축", "미", "丑", "未"],
    "기": ["자", "신", "子", "申"], "己": ["자", "신", "子", "申"],
    "경": ["축", "미", "丑", "未"], "庚": ["축", "미", "丑", "未"],
    "신": ["인", "오", "寅", "午"], "辛": ["인", "오", "寅", "午"],
    "임": ["사", "묘", "巳", "卯"], "壬": ["사", "묘", "巳", "卯"],
    "계": ["사", "묘", "巳", "卯"], "癸": ["사", "묘", "巳", "卯"]
}

ZI_CHUNG = {
    "자": "오", "子": "午", "오": "자", "午": "子",
    "축": "미", "丑": "未", "미": "축", "未": "丑",
    "인": "신", "寅": "申", "신": "인", "申": "寅",
    "묘": "유", "卯": "酉", "유": "묘", "酉": "卯",
    "진": "술", "辰": "戌", "술": "진", "戌": "辰",
    "사": "해", "巳": "亥", "해": "사", "亥": "巳"
}

calendar = KoreanLunarCalendar()

def get_exact_ganji(date_obj):
    """한글 간지 반환 메서드 사용"""
    calendar.setSolarDate(date_obj.year, date_obj.month, date_obj.day)
    ganji_str = calendar.getGapJaString()  # 한글 간지 반환 ("OO년 OO월 OO일")
    day_part = ganji_str.split()[-1]       # "OO일"
    return day_part[0], day_part[1]

# ---------------------------------------------------------
# 2. 맞춤형 특수 가중치 적용 평가 엔진
# ---------------------------------------------------------
def evaluate_day_custom(my_gan, my_zi, t_gan, t_zi, target_date):
    score = 0
    reasons = []

    my_elem, my_is_yang = GAN_INFO[my_gan]
    t_elem, t_is_yang = GAN_INFO[t_gan]
    t_zi_elem = ZI_ELEMENT[t_zi]

    # [기본 명리 평가]
    # 1. 천간 편재
    if OVERCOMES[my_elem] == t_elem and my_is_yang == t_is_yang:
        score += 35
        reasons.append("천간 편재(횡재수)")
    elif OVERCOMES[my_elem] == t_elem:
        score += 20
        reasons.append("천간 정재(재물운)")

    # 2. 지지 재성 & 천을귀인
    if OVERCOMES[my_elem] == t_zi_elem:
        score += 15
        reasons.append("지지 재성")
    if t_zi in CHEON_EUL.get(my_gan, []):
        score += 20
        reasons.append("천을귀인")

    # [★ 장인어른 사주 맞춤형 특수 로직 (갑목 일간 / 오화 일지 기준)]
    if my_gan in ["갑", "甲"]:
        # 조건 A: 戊申일 - 무토 편재 + 시주(壬申) 완벽 동착 (★최고 길일)
        if t_gan in ["무", "戊"] and t_zi in ["신", "申"]:
            score += 50
            reasons.append("★시주(壬申) 완벽 동착 + 편재 결합(최고 길일)")

        # 조건 B: 丙午일 - 일지 오화와 월지 미토의 오미합(午未合)으로 재물창고 활성화
        elif t_gan in ["병", "丙"] and t_zi in ["오", "午"]:
            score += 40
            reasons.append("오미합(午未合) 재물창고 활성화 + 丙火 직관력")

        # 조건 C: 癸卯일 / 입추 절입 - 계수(癸水) 정인으로 뇌식힘 및 수기 보충
        elif t_gan in ["계", "癸"] and t_zi in ["묘", "卯"]:
            score += 35
            reasons.append("癸水 정인 차가운 단비 + 입추 절입 수기(水氣) 전환")

    # 감점: 일지 충
    if ZI_CHUNG.get(my_zi) == t_zi:
        score -= 40
        reasons.append("일지 충(沖)")

    return score, reasons

# ---------------------------------------------------------
# 3. 메인 실행
# ---------------------------------------------------------
def main():
    print("=" * 65)
    print("  [ 사주 맞춤형 특수 가중치 적용 복권 길일 추출기 ]")
    print("=" * 65)

    my_gan = input("본인의 일간을 입력하세요 (예: 갑): ").strip()
    my_zi = input("본인의 일지를 입력하세요 (예: 오): ").strip()

    if my_gan not in GAN_INFO or my_zi not in ZI_ELEMENT:
        print("\n[오류] 올바른 천간/지지를 입력해주세요.")
        return

    today = datetime.date.today()
    results = []

    # 향후 60일 분석
    for i in range(60):
        target_date = today + datetime.timedelta(days=i)
        t_gan, t_zi = get_exact_ganji(target_date)
        score, reasons = evaluate_day_custom(my_gan, my_zi, t_gan, t_zi, target_date)

        if score > 0:
            results.append({
                'date': target_date,
                'ganji': f"{t_gan}{t_zi}",
                'score': score,
                'reasons': reasons
            })

    results.sort(key=lambda x: x['score'], reverse=True)

    print("\n" + "-" * 70)
    print(f"{'순위':^4} | {'날짜':^12} | {'일진':^6} | {'점수':^6} | {'운세 분석 핵심 요약'}")
    print("-" * 70)

    for rank, item in enumerate(results[:10], 1):
        date_str = item['date'].strftime("%Y-%m-%d")
        reasons_str = ", ".join(item['reasons'])
        print(f"{rank:^4} | {date_str} |  {item['ganji']}일  | {item['score']:^6}점 | {reasons_str}")

    print("-" * 70)

if __name__ == "__main__":
    main()