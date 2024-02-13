<template>
    <div class="container">
        <input
            v-model="title"
            class="form-control"
            type="text"
            @keyup.enter="apply" />
        <b-button
            class="btn btn-primary"
            @click="openCategoryPopup">
            카테고리 선택
        </b-button>
        <b-button
            class="btn btn-primary"
            @click="apply">
            검색
        </b-button>

        <!-- 카테고리 선택 팝업 -->
        <b-modal v-model="categoryModal" title="카테고리 선택">
            <div class="selects">
                <div v-for="(category, index) in filters" :key="index">
                    <input
                        type="checkbox"
                        :id="'category_' + index"
                        v-model="selectedCategories"
                        :value="category"
                    />
                    <label :for="'category_' + index">{{ category }}</label>
                </div>
            </div>
        </b-modal>
    </div>
</template>

<script>
export default {
    data() {
        return {
            title: '',
            type: 'category',
            filters: [
                '전체', '성공', '강건', '노력', '겸손', '출중', '효행', '예절', '의리', '공경', '충성', '미인', '연예', '교감', '결혼', '은혜', '평범', '청렴', '자애', '독서', '학문', '고전', '불교', '태평', '고향', '순리', '속담', '경박', '욕심', '횡포', '이중성', '우연', '배신', '교훈', '한탄', '원한', '위기', '외로움', '가난', '백중', '경조사', '나이', '절기', '편지', '호칭', '기타'
            ],
            categoryModal: false,
            selectedCategories: [] // 선택된 카테고리를 담을 배열
        }
    },
    methods: {
        openCategoryPopup() {
            // 카테고리 선택 팝업 열기
            this.categoryModal = true;
        },
        applyCategory() {
            // 확인 버튼 클릭 시 선택된 카테고리 적용
            console.log('Selected Categories:', this.selectedCategories);
            // 팝업 닫기
            this.categoryModal = false;
        },
        cancelCategory() {
            // 취소 버튼 클릭 시 팝업 닫기
            this.categoryModal = false;
            // 선택된 카테고리 초기화
            this.selectedCategories = [];
        },
        apply() {
            // Apply 버튼 클릭 시 수행할 동작 정의
        }
    }
}
</script>

<style scoped>
.container {
    display: flex;
    align-items: center;
}
.container > * {
    margin-right: 10px;
}
</style>

<style scoped>
.container {
  display: flex;
  align-items: center; /* 세로 중앙 정렬 */
}

.btn-group {
  position: relative;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  z-index: 1000;
  width: 200px; /* 드롭다운 너비 조절 */
  padding: 10px;
  background-color: #fff;
  border: 1px solid rgba(0, 0, 0, 0.15);
  border-radius: 5px;
}

.form-check {
  margin-bottom: 10px;
}

.btn-primary {
  margin-right: 10px; /* 카테고리 선택 버튼과 입력 필드 사이 간격 조절 */
}
</style>