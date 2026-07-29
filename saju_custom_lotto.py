import datetime
from korean_lunar_calendar import KoreanLunarCalendar

# ---------------------------------------------------------
# 1. 천간 / 지지 및 명리학적 속성 정의
# ---------------------------------------------------------
CHEONGAN = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
JIJI = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

# 천간 오행 및 음양 (한글/한자 모두 등록)
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
# 지지 오행 (한글/한자 매핑)
ZI_ELEMENT = {
    # 한글
    "자": "수", "축": "토", "인": "목", "묘": "목",
    "진": "토", "사": "화", "오": "화", "미": "토",
    "신": "금", "유": "금", "술": "토", "해": "수",
    
    # 한자
    "子": "수", "丑": "토", "寅": "목", "卯": "목",
    "辰": "토", "巳": "화", "午": "화", "未": "토",
    "申": "금", "酉": "금", "戌": "토", "亥": "수"
}
# 오행 상극 (A가 B를 극함 -> 내가 극하는 오행이 '재성')
OVERCOMES = {"목": "토", "토": "수", "수": "화", "화": "금", "금": "목"}

# 천을귀인 (일간 기준)
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

# 지지 충(沖) - 깨지는 기운
ZI_CHUNG = {
    "자": "오", "子": "午",  "오": "자", "午": "子",
    "축": "미", "丑": "未",  "미": "축", "未": "丑",
    "인": "신", "寅": "申",  "신": "인", "申": "寅",
    "묘": "유", "卯": "酉",  "유": "묘", "酉": "卯",
    "진": "술", "辰": "戌",  "술": "진", "戌": "辰",
    "사": "해", "巳": "亥",  "해": "사", "亥": "巳"
}

calendar = KoreanLunarCalendar()

# ---------------------------------------------------------
# 2. korean-lunar-calendar 활용 일진(간지) 추출
# ---------------------------------------------------------
def get_exact_ganji(date_obj):
    """라이브러리를 이용해 해당 날짜의 일간과 일지를 추출"""
    calendar.setSolarDate(date_obj.year, date_obj.month, date_obj.day)
    ganji_str = calendar.getChineseGapJaString()  # 예: "병인년 을미월 경진일"
    
    # 일진(마지막 두 글자) 추출
    day_part = ganji_str.split()[-1]  # "경진일"
    gan = day_part[0]  # "경"
    zi = day_part[1]   # "진"
    return gan, zi

# ---------------------------------------------------------
# 3. 길일 운세 점수 계산 함수
# ---------------------------------------------------------
def evaluate_day(my_gan, my_zi, t_gan, t_zi):
    score = 0
    reasons = []

    my_elem, my_is_yang = GAN_INFO[my_gan]
    t_elem, t_is_yang = GAN_INFO[t_gan]
    t_zi_elem = ZI_ELEMENT[t_zi]

    # 1. 천간 편재 (내가 극하는 오행 + 같은 음양 -> 최고 횡재수)
    if OVERCOMES[my_elem] == t_elem and my_is_yang == t_is_yang:
        score += 40
        reasons.append("천간 편재(횡재수)")
    # 2. 천간 정재
    elif OVERCOMES[my_elem] == t_elem:
        score += 25
        reasons.append("천간 정재(재물운)")

    # 3. 지지 재성
    if OVERCOMES[my_elem] == t_zi_elem:
        score += 20
        reasons.append("지지 재성(결실운)")

    # 4. 천을귀인
    if t_zi in CHEON_EUL.get(my_gan, []):
        score += 30
        reasons.append("천을귀인(길신 작용)")

    # 5. 비등/합세 기운
    if my_elem == t_zi_elem:
        score += 10
        reasons.append("기운 보충")

    # 6. 감점: 일지 충(沖)
    if ZI_CHUNG.get(my_zi) == t_zi:
        score -= 50
        reasons.append("일지 충(沖) - 불안정")

    return score, reasons

# ---------------------------------------------------------
# 4. 실행 메인
# ---------------------------------------------------------
def main():
    print("=" * 60)
    print("  [ 사주 맞춤형 복권/횡재수 길일 추출기 (korean-lunar-calendar) ]")
    print("=" * 60)

    my_gan = input("본인의 일간을 입력하세요 (예: 갑, 을, 병, 정, 무, 기, 경, 신, 임, 계): ").strip()
    my_zi = input("본인의 일지를 입력하세요 (예: 자, 축, 인, 묘, 진, 사, 오, 미, 신, 유, 술, 해): ").strip()

    if my_gan not in CHEONGAN or my_zi not in JIJI:
        print("\n[오류] 올바른 천간 또는 지지를 입력해주세요.")
        return

    print(f"\n>> 입력된 내 일주: [{my_gan}{my_zi}일주]")
    print(">> 오늘부터 향후 60일간의 육십갑자 길일을 분석 중입니다...\n")

    today = datetime.date.today()
    results = []

    for i in range(60):
        target_date = today + datetime.timedelta(days=i)
        t_gan, t_zi = get_exact_ganji(target_date)
        score, reasons = evaluate_day(my_gan, my_zi, t_gan, t_zi)

        if score > 0:
            results.append({
                'date': target_date,
                'ganji': f"{t_gan}{t_zi}",
                'score': score,
                'reasons': reasons
            })

    results.sort(key=lambda x: x['score'], reverse=True)

    print("-" * 62)
    print(f"{'순위':^4} | {'날짜':^12} | {'일진':^6} | {'점수':^6} | {'운세 분석 요약'}")
    print("-" * 62)

    for rank, item in enumerate(results[:10], 1):
        date_str = item['date'].strftime("%Y-%m-%d")
        reasons_str = ", ".join(item['reasons'])
        print(f"{rank:^4} | {date_str} |  {item['ganji']}일  | {item['score']:^6}점 | {reasons_str}")

    print("-" * 62)

if __name__ == "__main__":
    main()