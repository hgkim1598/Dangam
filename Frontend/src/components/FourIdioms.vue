<template>
  <div>
    &emsp;
    <h2>사자성어 데이터</h2>
    <!-- 자음 필터 -->
    <h6>사자성어(한글) 선택</h6>
    <div>
      <b-button
        v-for="consonants in consonants"
        :key="consonants"
        @click="toggleConsonants(consonants)"
        :variant="buttonVariant(consonants)"
      >
        {{ consonants }}
      </b-button>
    </div>
    <!-- 검색어 입력 상자 -->
    <div>
      <input type="text" v-model="searchKeyword" class="oval-input">
      <!-- 검색 버튼 -->
      <b-button @click="search">
        <!-- 돋보기 아이콘 -->
        <b-icon icon="search"></b-icon>
      </b-button>
    </div>
    
  <div class="table-container">
    <b-button @click="showModal" class="nr_button">신규 등록</b-button>
    <b-dropdown v-if="categories.length > 0" ref="categoryDropdown" class="category-dropdown" variant="primary">
      <template #button-content>
        카테고리 선택
      </template>
      <b-form-group  class="category-dropdown-list">
        <b-form-checkbox-group v-model="selectedCategories">
          <b-form-checkbox v-for="(cat, index) in categories" :key="index" :value="cat" v-model="selectedCategories">{{ cat }}</b-form-checkbox>
        </b-form-checkbox-group>
      </b-form-group>
      <b-button @click="closeDropdown">취소</b-button>
      <b-button @click="fetchDataWithSelectedCategories" variant="success">확인</b-button>
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
  <div>
          <!-- 페이지 번호 표시 및 변경 -->
    <div class="d-flex justify-content-end">
      <div>
        <b-button @click="changePage(pageNumber - 1)" :disabled="pageNumber <= 1">이전 페이지</b-button>
        <span>{{ pageNumber }} / {{ totalPage }}</span>
        <b-button @click="changePage(pageNumber + 1)" :disabled="pageNumber >= totalPage">다음 페이지</b-button>
     </div>
   </div>
        </div>
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
      totalPage: 0,
      pageNumber: 1,
      searchKeyword: '',
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
      consonants: ['전체', 'ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'], // 한글 자음
      items: [],
      rows: [],
      infoModal: { id: 'info-modal', title: '', content: '' },
      categories: [], // 카테고리 배열
      selectedCategories: [], // 선택된 카테고리 배열
      prevSelectedCategories: [], // 이전 선택된 카테고리 배열
      selectedConsonants: [] // 선택된 자음 배열
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
      buttonVariant(consonants) {
      // 선택된 자음 배열에 현재 버튼이 포함되어 있는지 확인
      const isSelected = this.selectedConsonants.includes(consonants);
      
      // 전체 버튼인 경우
      if (consonants === '전체') {
        // 전체가 선택된 상태이면 빨간색, 아니면 파란색
        return isSelected ? 'danger' : 'primary';
      } else {
        // 다른 자음 버튼인 경우
        // 선택된 상태이면 빨간색, 아니면 파란색
        return isSelected ? 'danger' : 'primary';
      }
    },

    fetchData1(page, keyword, consonants, categoriesParams) {
      page = Number(page);

      let apiUrl = `http://192.168.0.149:8000/fourchar`;

      if (keyword) {
        apiUrl += `/filter/?keyword=${keyword}&p=${page}`;
      
      } else if (this.selectedConsonants && this.selectedConsonants.length > 0) {
        if (this.selectedConsonants.includes('전체')) {
          apiUrl += `?p=${page}`;
        } else {
          const consonantString = this.selectedConsonants.join('&consonants=') // 선택된 자음을 쉼표로 구분된 문자열로 변환
          apiUrl += `/filter/?consonants=${consonantString}&p=${page}`;
        }
      }  else if (categoriesParams) {
        apiUrl += `/filter/?${categoriesParams}&p=${page}`; // page 변수를 사용합니다.
        this.$refs.categoryDropdown.hide();
      } else {
        apiUrl += `?p=${page}`;
      }
      console.log(apiUrl);
      axios.get(apiUrl)
        .then(response => {
          console.log(response.data);
          this.totalPage = response.data.total_page;
          this.items = response.data.content;
        })
        .catch(error => {
          console.error('데이터를 불러오는 중 오류 발생:', error);
        });
    },

    async toggleConsonants(consonants) {
      const index = this.selectedConsonants.indexOf(consonants);

      if (consonants === '전체') {
        // 전체 버튼일 경우
        if (index === -1) {
          // 전체 버튼이 선택되지 않은 경우, 선택된 자음 배열에 전체 버튼을 추가하고 다른 자음 버튼을 비활성화
          this.selectedConsonants = ['전체'];
        } else {
          // 전체 버튼이 이미 선택된 경우, 선택을 취소하고 모든 자음 버튼을 활성화
          this.selectedConsonants = [];
        }
      } else {
        // 다른 자음 버튼이 선택된 경우
        if (index === -1) {
          // 선택되지 않은 경우, 선택된 자음 배열에 해당 버튼 추가
          this.selectedConsonants.push(consonants);
          // 만약 전체 버튼이 선택된 상태였다면 전체 버튼 선택 취소
          const allIndex = this.selectedConsonants.indexOf('전체');
          if (allIndex !== -1) {
            this.selectedConsonants.splice(allIndex, 1);
          }
        } else {
          // 선택된 경우, 선택을 취소
          this.selectedConsonants.splice(index, 1);
        }
      }

      // 전체가 선택되었는지 확인
      const isAllSelected = this.selectedConsonants.includes('전체');

      // 전체가 선택되지 않은 경우
      if (!isAllSelected) {
        // 전체가 선택되지 않았을 때 데이터 가져오기
        await this.fetchData1(this.pageNumber, this.searchKeyword, this.selectedConsonants);
      } else {
        // 전체가 선택된 경우 전체 데이터 가져오기
        await this.fetchData();
      }
    },

    async fetchData(page) {
      try {
        page = 1;
        let apiUrl = 'http://192.168.0.149:8000/fourchar';
        const apiUrl1 = apiUrl += `?p=${page}`;
        const response = await axios.get(apiUrl1);
        this.totalPage = response.data.total_page;
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
        const apiUrl = 'http://192.168.0.149:8000/category/?select_category=fourchar';
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
    // submitSelectedCategories() {
    //   // 선택된 카테고리들을 백엔드에서 요구하는 형식에 맞게 가공합니다.
    //   const categoriesParams = this.selectedCategories.map(category => `categories=${encodeURIComponent(category)}`).join('&');

    //   axios.get(`http://192.168.0.149:8000/fourchar/filter/?${categoriesParams}&p=${this.pageNumber}`)
    //     .then(response => {
    //       console.log(response.data);
    //       this.totalPage = response.data.total_page;
    //       this.items = response.data.content; // 받아온 데이터를 items에 할당
    //       // 드롭다운 박스를 닫습니다.
    //       this.$refs.categoryDropdown.hide();
    //     })
    //     .catch(error => {
    //       console.error('GET 요청 중 오류가 발생했습니다.', error);
    //       // 오류 발생 시 처리할 내용을 추가할 수 있습니다.
    //     });
    // },
    fetchDataWithSelectedCategories() {
      const categoriesParams = this.selectedCategories.map(category => `categories=${encodeURIComponent(category)}`).join('&');
    console.log(categoriesParams); // 확인하고 싶은 변수를 콘솔에 출력
    this.fetchData1(this.pageNumber, this.searchKeyword, null, categoriesParams);
  },

    toggleDropdown() {
      // 드롭다운 박스를 열거나 닫습니다.
      this.$refs.categoryDropdown.toggle();
      // 선택된 카테고리를 이전에 선택된 카테고리로 저장합니다.
      this.prevSelectedCategories = [...this.selectedCategories];
    },


    changePage(page) {
  if (page > 0 && page <= this.totalPage) {
    this.pageNumber = page;
    if (this.selectedCategories.length > 0 || this.searchKeyword.trim() !== '') {
      // 카테고리가 선택되어 있거나 검색어가 입력되어 있는 경우에만 필터링된 데이터를 가져옵니다.
      const categoriesParams = this.selectedCategories.map(category => `categories=${encodeURIComponent(category)}`).join('&');
      this.fetchData1(page, this.searchKeyword, null, categoriesParams);
    } else {
      // 카테고리가 선택되어 있지 않고 검색어가 입력되어 있지 않은 경우 전체 데이터를 가져옵니다.
      this.fetchData1(page);
    }
  }
},

    search() {
      const trimmedKeyword = this.searchKeyword.trim();
      if (trimmedKeyword !== '') {
        this.pageNumber = 1; // 검색할 때 페이지 번호를 1로 초기화합니다.
        this.fetchData1(this.pageNumber, trimmedKeyword, null); // 검색 시 검색어도 함께 전달
      }
    },
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

.oval-input {
  border-radius: 50px; /* 타원형으로 만들기 위해 반지름 설정 */
  padding: 10px 20px; /* 내부 여백 설정 */
  width: 250px; /* 너비 설정 */
  border: 2px solid #ccc; /* 테두리 설정 */
}
</style>