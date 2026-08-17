import datetime
from korean_lunar_calendar import KoreanLunarCalendar

# ---------------------------------------------------------
# 1. 천간/지지 오행 및 매핑 데이터
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

# 내가 극(剋)하는 오행 (재성 관계)
OVERCOMES = {"목": "토", "토": "수", "수": "화", "화": "금", "금": "목"}

# 천을귀인 매핑
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

# 지지 충(沖)
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
    """일진 한글 반환"""
    calendar.setSolarDate(date_obj.year, date_obj.month, date_obj.day)
    ganji_str = calendar.getGapJaString()
    day_part = ganji_str.split()[-1]
    return day_part[0], day_part[1]

# ---------------------------------------------------------
# 2. 명리 평가 엔진 (토요일 추첨일 기준)
# ---------------------------------------------------------
def evaluate_day_general(my_gan, my_zi, t_gan, t_zi, hour_gan=None, hour_zi=None):
    score = 0
    reasons = []

    my_elem, my_is_yang = GAN_INFO[my_gan]
    t_elem, t_is_yang = GAN_INFO[t_gan]
    t_zi_elem = ZI_ELEMENT[t_zi]

    is_pyeonjae = False
    is_cheoneul = False
    is_zi_jaeseong = False

    # 1. 천간 재성 (편재 vs 정재)
    if OVERCOMES[my_elem] == t_elem:
        if my_is_yang == t_is_yang:
            score += 35
            is_pyeonjae = True
            reasons.append("천간 편재(횡재수)")
        else:
            score += 20
            reasons.append("천간 정재(재물운)")

    # 2. 지지 재성
    if OVERCOMES[my_elem] == t_zi_elem:
        score += 15
        is_zi_jaeseong = True
        reasons.append("지지 재성(결실/재물창고)")

    # 3. 천을귀인
    if t_zi in CHEON_EUL.get(my_gan, []):
        score += 20
        is_cheoneul = True
        reasons.append("천을귀인(길신 작용)")

    # 4. 일지 동착
    if my_zi == t_zi:
        score += 15
        reasons.append("일지 동착(기운 증폭)")

    # 5. [선택] 시주 완벽 동착 (시간/시지 입력 시)
    if hour_zi and t_zi == hour_zi:
        score += 50
        reasons.append(f"★시주({hour_gan or ''}{hour_zi}) 완벽 동착 + 결합(최고 당첨일)")

    # 6. 감점 요인 (일지 충)
    if ZI_CHUNG.get(my_zi) == t_zi:
        score -= 30
        reasons.append("일지 충(기운 산란)")

    # 최고 길일 멘트 정리
    if (is_pyeonjae and (is_cheoneul or is_zi_jaeseong)) or score >= 70:
        if not any("★" in r for r in reasons):
            reasons.insert(0, "★[최고 당첨 길일]")

    return score, reasons

# ---------------------------------------------------------
# 3. 메인 실행
# ---------------------------------------------------------
def main():
    print("=" * 65)
    print("  [ 사주 맞춤형 로초 추첨일(토요일) 당첨 길운 추출기 ]")
    print("=" * 65)

    my_gan = input("본인의 일간을 입력하세요 (예: 갑): ").strip()
    my_zi = input("본인의 일지를 입력하세요 (예: 오): ").strip()
    
    # 선택 입력: 시주 (엔터 치면 스킵)
    hour_gan = input("본인의 시간을 입력하세요 (선택, 없으면 Enter): ").strip()
    hour_zi = input("본인의 시지를 입력하세요 (선택, 없으면 Enter/예: 신): ").strip()

    if my_gan not in GAN_INFO or my_zi not in ZI_ELEMENT:
        print("\n[오류] 올바른 천간/지지를 입력해주세요.")
        return

    today = datetime.date.today()
    results = []

    # 향후 180일 동안의 '토요일'만 탐색 (약 25개 주말)
    for i in range(180):
        target_date = today + datetime.timedelta(days=i)
        
        # target_date.weekday() == 5 이면 '토요일'
        if target_date.weekday() == 5:
            t_gan, t_zi = get_exact_ganji(target_date)
            score, reasons = evaluate_day_general(my_gan, my_zi, t_gan, t_zi, hour_gan, hour_zi)

            if score > 0:
                results.append({
                    'date': target_date,
                    'ganji': f"{t_gan}{t_zi}",
                    'score': score,
                    'reasons': reasons
                })

    # 점수 높은 순 정렬
    results.sort(key=lambda x: x['score'], reverse=True)

    print("\n" + "-" * 70)
    print(f"{'순위':^4} | {'추첨일(토요일)':^14} | {'일진':^6} | {'점수':^6} | {'당첨 운세 핵심 요약'}")
    print("-" * 70)

    for rank, item in enumerate(results[:10], 1):
        date_str = item['date'].strftime("%Y-%m-%d (토)")
        reasons_str = ", ".join(item['reasons'])
        print(f"{rank:^4} | {date_str:^14} |  {item['ganji']}일  | {item['score']:^6}점 | {reasons_str}")

    print("-" * 70)

if __name__ == "__main__":
    main()
