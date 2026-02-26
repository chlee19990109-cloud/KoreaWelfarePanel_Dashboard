# 한국복지패널 데이터 분석 대시보드

이 프로젝트는 한국복지패널 데이터를 활용하여 성별, 연령대, 직업, 종교, 지역 등 다양한 요인에 따른 사회/경제적 특성(월급, 이혼율 등)을 분석하고 시각화한 Streamlit 기반 웹 대시보드입니다.

- **분석 대시보드 웹 앱 링크:** [한국복지패널 대시보드 바로가기](https://koreawelfarepaneldashboard-ny7el4ekhw6kwdrvmjqd6d.streamlit.app/)
- **작성자:** 이충환

---

## 📊 대시보드 주요 분석 주제 및 시각화

**1. 성별에 따른 월급 차이 - '성별에 따라 월급이 다를까?'**
- 성별에 따른 평균 막대 그래프 

**2. 나이와 월급의 관계 - '몇 살 때 월급을 가장 많이 받을까?'**
- 나이에 따른 평균 월급 선 그래프 

**3. 연령대에 따른 월급 차이 - 어떤 연령대의 월급이 가장 많을까?**
- 연령대에 따른 평균 월급 막대 그래프

**4. 연령대 및 성별 월급 차이 - 성별 월급 차이는 연령대별로 다를까?**
- 연령대 및 성별에 따른 평균 월급 막대 그래프

**5. 직업별 월급 차이 - 어떤 직업이 월급을 가장 많이 받을까?**
- 직업에 따른 상위 10개 평균 월급 막대 그래프

**6. 성별 직업 빈도 - 성별로 어떤 직업이 가장 많을까?**
- 남성 직업 빈도 막대 그래프
- 여성 직업 빈도 막대 그래프

**7. 종교 유무에 따른 이혼율 - 종교가 있으면 이혼을 덜 할까?**
- 종교에 따른 이혼율 막대 그래프
- 연령대에 따른 이혼율 막대 그래프
- 연령대 및 종교 유무에 따른 이혼율 막대 그래프

**8. 지역별 연령대 비율 - 어느 지역에 노년층이 많을까?**
- 지역별 연령대 비율 그래프

---

## 🛠 사용된 기술 및 주요 라이브러리 (Tech Stack)

본 프로젝트는 Python 생태계를 기반으로 구축되었으며, 주요 데이터 처리부터 반응형 인터랙티브 UI 구성 및 시각화까지 다음의 세분화된 기술 스택을 활용합니다.

### 🌐 Web Framework & UI
- **[Streamlit](https://streamlit.io/)**: 
  - `st.set_page_config`를 통한 페이지 메타데이터(타이틀, 파비콘) 및 Wide 레이아웃 설정
  - `st.sidebar` 내 위젯(`selectbox`, `slider`, `multiselect`) 렌더링을 통한 동적 유저 인터랙션 및 필터링 기능 구현
  - `@st.cache_data` 데코레이터를 이용한 원본 데이터 로드 시 성능 최적화(캐싱) 지원
  - `st.columns` 기반의 그리드 레이아웃 분할로 데이터프레임과 분석 시각화 차트를 효율적으로 병렬 배치

### 📊 Data Processing & Analysis
- **[Pandas](https://pandas.pydata.org/)**: 
  - `.csv` 및 `.xlsx` 등 다중 포맷 데이터 로드 및 데이터 병합(`merge`) 프로세스 수행
  - 다수의 결측치 정제(`dropna`, `replace`), 조건부 람다 함수(또는 `apply`, `map`)를 통한 새 파생 변수 생성
  - 고유한 집계 연산을 위한 그룹화(`groupby()`, `agg()`) 및 데이터 피벗(`pivot()`) 테이블 구축
- **[NumPy](https://numpy.org/)**:
  - `np.where()` 메서드를 이용한 강력한 조건부 값 치환 작업
  - `np.nan`을 적용하여 무응답이나 알 수 없는 예외 값들에 대한 결측치 모델링의 일관성 유지

### 📈 Data Visualization
- **[Matplotlib](https://matplotlib.org/)**:
  - 백엔드에서 `plt.subplots()`를 도출해 Figure 및 Axes 기반의 미시적이고 정교한 그래프 영역 제어
  - 누적 막대 그래프(`stacked=True`), 개별 바(Bar) 수치 Label 표기용 주석(`ax.annotate`) 같은 디테일 렌더링
- **[Seaborn](https://seaborn.pydata.org/)**:
  - Matplotlib 위에서 동작하는 고수준 API로 복잡도를 줄이면서 직관적인 차트(`sns.barplot`, `sns.lineplot`) 도출
  - `hue` 변수 및 다중 `order` 속성값 적용으로 여러 범주형 다변량 데이터의 추이를 직관적으로 비교 분석
- **[koreanize_matplotlib](https://github.com/ychoi-kr/koreanize-matplotlib)**:
  - 데이터 시각화 시 빈번히 발생하는 한글 폰트 깨짐 현상을 구동 중인 OS(Windows/Mac/Linux)에 구애받지 않고 자동으로 글로벌 방지 세팅

### 🖼️ Media & File Handling
- **[Pillow (PIL)](https://python-pillow.org/)**: 
  - 앱 메인에 적용될 로컬 이미지 리소스(`sample.png`)를 읽고 변환하여 브라우저 내 파비콘 이미지로 브릿지 렌더링
- **[openpyxl](https://openpyxl.readthedocs.io/)**:
  - Pandas `read_excel()` 함수가 `.xlsx` 포맷의 범주형 코드북(직종코드)을 읽고 파싱할 수 있도록 지원하는 백엔드 코어 엔진 작동

---

## ⚙️ 환경 설정 및 필수 요구사항 (Environment Requirements)

해당 대시보드의 원활한 코드 실행과 데이터 시각화를 구동하기 위해선 다음과 같은 로컬 환경 구축이 전제되어야 합니다.

### 1. 시스템 요구사항
- **OS**: Windows / macOS / Linux (크로스 플랫폼 지원)
- **Python 환경**: `Python 3.8` 이상의 인터프리터 (버전 `3.10` 강력 권장)

### 2. 패키지 의존성 (Dependencies)
모듈 충돌 방지를 위해 독립된 가상환경(venv 등)을 세팅한 후, 로컬 터미널(프롬프트)에 접속해 아래 패키지들을 다운로드합니다. `requirements.txt` 파일 설치를 권장합니다.
- **코어 모듈**: `streamlit`, `pandas`, `numpy`
- **시각화 모듈**: `matplotlib`, `seaborn`, `koreanize-matplotlib`
- **서포트 모듈**: `Pillow`, `openpyxl`

```bash
# 단일 명령어로 직접 전체 설치 시
pip install streamlit pandas numpy matplotlib seaborn Pillow openpyxl koreanize-matplotlib
```
*(또는 `pip install -r requirements.txt` 명령어로 간편히 자동 의존성 설치 가능)*

### 3. 디렉터리 및 필수 실행 에셋 구조
로컬 저장소에서 오류 없이 앱이 구동되려면 시작 스크립트인 `app.py`와 같은 레벨의 작업(루트) 디렉터리 경로 내에 **아래 에셋 파일들이 전부 존재**해야 합니다.
- `app.py`: Streamlit 대시보드의 전체 화면 구성, 시각화, 데이터 파이프라인 흐름을 제어하는 메인 실행 스크립트
- `welfare_2015.csv`: 대시보드에서 전역으로 필터링 및 분석되는 **복지패널 분석용 원본 데이터** (사이드바 기본 파일 경로 매핑용 데이터)
- `welfare_2015_codebook.xlsx`: 수치로 기록된 직업 코드(`job_code`) 등의 범주형 특성을 실제 한글 명칭으로 변환하기 위해 참조(`merge` 결합)하는 엑셀 기반 참조 코드북
- `sample.png`: 웹 페이지 상단 브라우저 탭 아이콘(파비콘)에 고유하게 반영하기 위해 호출하는 초기 진입 이미지 파일

---

## 📂 저장소 및 데이터 구조

프로젝트를 실행하기 위해 구조는 다음과 같이 구성되어 있습니다:

- `app.py`: Streamlit 대시보드의 실질적인 소스 코드가 포함된 메인 분석 스크립트.
- `welfare_2015.csv`: 메인으로 분석될 복지 패널 원본 데이터 (로컬 실행 시 같은 디렉터리에 위치해야 함).
- `welfare_2015_codebook.xlsx`: 직종 코드 등 데이터를 해석하기 위해 매핑할 때 사용되는 코드북.
- `sample.png`: Streamlit 웹 페이지 내의 파비콘 및 이미지 표시용.
- `requirements.txt`: Streamlit Cloud 배포 및 로컬 실행 시 의존성 관리에 사용되는 라이브러리 리스트.

> **데이터 출처:** 복지패널 데이터

---

## 🚀 로컬 환경에서 실행하는 방법 (Local Setup & Run)

이 프로젝트를 사용자의 PC에서 직접 실행해 보기 위해서는 아래 단계를 따라주시면 됩니다.

**1. 패키지 의존성 설치:**
다운로드한 폴더나 저장소 경로에서 터미널(명령 프롬프트)을 열고, 다음 명령어를 실행하여 필수 모듈을 설치합니다.
```bash
pip install -r requirements.txt
```

**2. Streamlit 대시보드 실행:**
설치가 완료되었다면, 터미널에서 아래의 명령어를 입력하여 앱을 실행합니다.
```bash
streamlit run app.py
```

**3. 웹 브라우저에서 확인:**
자동으로 브라우저가 실행되며, `http://localhost:8501` 이 열리면서 로컬에서도 대시보드를 직접 이용할 수 있습니다.

