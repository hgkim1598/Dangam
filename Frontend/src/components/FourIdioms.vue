<template>
  <div class="table-container">
    <b-button @click="showModal" class="nr_button">신규 등록</b-button>
    <b-dropdown v-if="categories.length > 0" ref="categoryDropdown" class="category-dropdown" variant="primary">
      <template #button-content>
        카테고리 선택
      </template>
      <b-form-group  class="category-dropdown-list">
        <b-form-checkbox-group v-model="selectedCategories">
          <b-form-checkbox v-for="(cat, index) in categories" :key="index" :value="cat">{{ cat }}</b-form-checkbox>
        </b-form-checkbox-group>
      </b-form-group>
      <b-button @click="closeDropdown">취소</b-button>
      <b-button @click="submitSelectedCategories" variant="success">확인</b-button>
    </b-dropdown>
    <b-modal v-model="modalVisible" :title="modalTitle" hide-footer>
      <!-- Create.vue 컴포넌트 렌더링 -->
      <Create :isEditMode="isEditMode" :editId="editId" @closeModal="closeModal" />
    </b-modal>
    <b-table striped hover :items="items" :fields="fields">
      <template #cell(actions)="row">
        <!-- 제어 버튼 -->
        <div class="btn-group" role="group">
          <b-button size="sm" @click="toggleDetails(row.item)" class="control-button">
            {{ row.item.detailsShowing ? '숨김' : '펼침' }}
          </b-button>
          <b-button size="sm" variant="warning" @click="editItem(row.item)" class="control-button">수정</b-button>
          <b-button size="sm" variant="danger" @click="deleteItem(row.item)" class="control-button last-button">삭제</b-button>
        </div>
      </template>

      <!-- 커스텀 컬럼 정의 -->
      <template #cell(contents_detail)="data">
        <div>
          <b-card v-if="data.item.detailsShowing">
            <p>{{ data.item.contents_detail }}</p>
          </b-card>
          <span v-else>{{ truncateText(data.item.contents_detail, 50) }}</span>
        </div>
      </template>

      <!-- 확장된 세부 정보 -->
      <template #row-details="row">
        <b-card v-if="row.item.detailsShowing">
          <ul>
            <li v-for="(value, key) in row.item" :key="key">{{ key }}: {{ value }}</li>
          </ul>
        </b-card>
      </template>
    </b-table>
  </div>
</template>

<script>
import axios from 'axios';
import Create from './Create.vue';

export default {
  components: {
    Create
  },
  data() {
    return {
      modalVisible: false,
      isEditMode: false,
      editId: null,
      fields: [
        { key: 'id', label: 'No' },
        { key: 'category', label: '카테고리' },
        { key: 'contents_kr', label: '사자성어(한글)' },
        { key: 'contents_zh', label: '사자성어(한문)' },
        { key: 'contents_detail', label: '뜻풀이' },
        { key: 'actions', label: '제어', class: 'text-center', thClass: 'text-center', sortable: false }
      ],
      items: [],
      rows: [],
      infoModal: { id: 'info-modal', title: '', content: '' },
      categories: [], // 카테고리 배열
      selectedCategories: [], // 선택된 카테고리 배열
      prevSelectedCategories: [], // 이전 선택된 카테고리 배열
    };
  },
  created() {
    this.fetchData();
    this.fetchCategories(); // 카테고리 데이터 가져오기
  },
  computed: {
    modalTitle() {
      return this.isEditMode ? '수정' : '신규 등록';
    }
  },
  methods: {
    async fetchData() {
      try {
        const apiUrl = 'http://192.168.0.149:8000/fourchar';
        const response = await axios.get(apiUrl);
        this.items = response.data.content;
        // 각 아이템에 detailsShowing 프로퍼티 추가
        this.items.forEach(item => {
          this.$set(item, 'detailsShowing', false);
        });
      } catch (error) {
        console.error('데이터를 불러오는 중 오류 발생:', error);
      }
    },
    async fetchCategories() {
      try {
        const apiUrl = 'http://192.168.0.149:8000/category/';
        const response = await axios.get(apiUrl);
        this.categories = response.data; // 카테고리 배열에 데이터 저장
      } catch (error) {
        console.error('카테고리를 불러오는 중 오류 발생:', error);
      }
    },
    async handleNewIdiom(newIdiom) {
      this.items.push(newIdiom);
      this.closeModal();
    },
    editItem(item) {
      this.isEditMode = true;
      this.editId = item.id;
      this.modalVisible = true; // 모달 열기
    },
    async deleteItem(item) {
      const confirmDelete = confirm('삭제하시겠습니까?');
      if (confirmDelete) {
        try {
          await axios.delete(`http://192.168.0.149:8000/fourchar/delete/${item.id}`);
          const index = this.items.findIndex(i => i.id === item.id);
          if (index !== -1) {
            this.items.splice(index, 1);
          }
          console.log('아이템 삭제 완료');
        } catch (error) {
          console.error('아이템 삭제 중 오류 발생:', error);
        }
        location.reload();
      }
    },
    showModal() {
      this.modalVisible = true;
      this.editId = null; // editId 초기화
    },
    closeModal() {
      this.modalVisible = false;
      // 모달을 닫습니다.
      this.hideModal();
      if (!this.isEditMode) {
        // 신규 등록 모드일 때만 초기화하고 새로고침합니다.
        this.editId = null;
        // 메인 페이지를 새로고침합니다.
        window.location.reload();
      }
      this.isEditMode = false;
      this.editId = null;
    },
    truncateText(text, maxLength) {
      if (text.length <= maxLength) {
        return text;
      } else {
        return text.substring(0, maxLength) + '...';
      }
    },
    toggleDetails(item) {
      item.detailsShowing = !item.detailsShowing;
    },
    closeDropdown() {
      // 드롭다운 박스를 닫습니다.
      this.$refs.categoryDropdown.hide();
      // 이전에 선택된 카테고리로 되돌립니다.
      this.selectedCategories = this.prevSelectedCategories;
    },
    submitSelectedCategories() {
  // 선택된 카테고리들을 백엔드에서 요구하는 형식에 맞게 가공합니다.
  const categoriesParams = this.selectedCategories.map(category => `categories=${encodeURIComponent(category)}`).join('&');

  axios.get(`http://192.168.0.149:8000/saying/filter/?${categoriesParams}`)
    .then(response => {
      console.log(response.data);
      // 성공적으로 요청을 보냈을 때의 처리를 추가할 수 있습니다.
      // 드롭다운 박스를 닫습니다.
      this.$refs.categoryDropdown.hide();
    })
    .catch(error => {
      console.error('GET 요청 중 오류가 발생했습니다.', error);
      // 오류 발생 시 처리할 내용을 추가할 수 있습니다.
    });
}
,
    toggleDropdown() {
      // 드롭다운 박스를 열거나 닫습니다.
      this.$refs.categoryDropdown.toggle();
      // 선택된 카테고리를 이전에 선택된 카테고리로 저장합니다.
      this.prevSelectedCategories = [...this.selectedCategories];
    }
  }
};
</script>

<style scoped>
.table-container {
  margin-top: 60px; /* 테이블 컨테이너의 상단 마진 설정 */
  position: relative;  /*부모 요소를 상대적으로 설정 */
}
.control-button {
  margin-right: 5px; /* 제어 버튼들 간의 오른쪽 마진 설정 */
}

/* 마지막 버튼에 대한 스타일 */
.last-button {
  margin-right: 0; /* 마지막 버튼에 오른쪽 마진을 설정하지 않음 */
}

.nr_button {
  position: absolute; /* 절대 위치로 설정 */
  top: 0; /* 부모 요소 상단에 위치 */
  right: 0; /* 부모 요소 오른쪽에 위치 */
  margin-top: -40px; /* 테이블과 겹치지 않도록 버튼을 위로 올림 */
  margin-right: 60px; /* 오른쪽 여백 설정 */
}

.category-dropdown {
  position: absolute; /* 절대 위치로 설정 */
  top: 0; /* 부모 요소 상단에 위치 */
  left: 0; /* 부모 요소 왼쪽에 위치 */
  margin-top: -40px; /* 테이블과 겹치지 않도록 드롭다운 박스를 위로 올림 */
  margin-left: 10px; /* 왼쪽 여백 설정 */
}

.category-checkbox {
  margin-right: 10px; /* 체크박스 간의 오른쪽 여백 설정 */
}

.category-dropdown-list {
  max-height: 200px; /* 드롭다운 박스의 최대 높이 설정 */
  overflow-y: auto; /* 수직 스크롤을 활성화합니다. */
}
</style>