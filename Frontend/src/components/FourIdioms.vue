<template>
  <div>
    <!-- 검색어 입력 상자 -->
    <div>
      <input type="text" v-model="searchKeyword">
      <!-- 검색 버튼 -->
      <b-button @click="search">
        <!-- 돋보기 아이콘 -->
        <b-icon icon="search"></b-icon>
      </b-button>
    </div>
    <!-- 게시판 데이터 표시 -->
    <div>
      <b-table striped hover :items="items" :fields="fields">
      </b-table>
    </div>
    <!-- 페이지 번호 표시 및 변경 -->
    <div class="d-flex justify-content-end">
      <div>
        <b-button @click="changePage(pageNumber - 1)" :disabled="pageNumber <= 1">이전 페이지</b-button>
        <span>{{ pageNumber }} / {{ totalPage }}</span>
        <b-button @click="changePage(pageNumber + 1)" :disabled="pageNumber >= totalPage">다음 페이지</b-button>
     </div>
   </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      totalPage: 0,
      items: [],
      pageNumber: 1,
      searchKeyword: '',
      fields: [
        { key: 'id', label: 'No' },
        { key: 'category', label: '카테고리' },
        { key: 'contents_kr', label: '사자성어(한글)' },
        { key: 'contents_zh', label: '사자성어(한문)' },
        { key: 'contents_detail', label: '뜻풀이' },
      ]
    };
  },
  methods: {
    fetchData(page, keyword) {
      page = Number(page);

      let apiUrl = `http://192.168.0.149:8000/fourchar`;
      if (keyword) {
        apiUrl += `/filter/?keyword=${keyword}`;
      } else {
        apiUrl += `?p=${page}`;
      }

      axios.get(apiUrl)
        .then(response => {
          this.totalPage = response.data.total_page;
          this.items = response.data.content;
        })
        .catch(error => {
          console.error('데이터를 불러오는 중 오류 발생:', error);
        });
    },
    changePage(page) {
      if (page > 0 && page <= this.totalPage) {
        this.pageNumber = page;
        this.fetchData(page, this.searchKeyword); // 페이지 변경 시 검색어도 함께 전달
      }
    },
    search() {
      const trimmedKeyword = this.searchKeyword.trim();
      if (trimmedKeyword !== '') {
        this.pageNumber = 1; // 검색할 때 페이지 번호를 1로 초기화합니다.
        this.fetchData(this.pageNumber, trimmedKeyword); // 검색 시 검색어도 함께 전달
      }
    },
    editItem(item) {
      // 아이템 편집 로직 구현
    },
    deleteItem(item) {
      // 아이템 삭제 로직 구현
    }
  },
  mounted() {
    this.fetchData(this.pageNumber, this.searchKeyword); // 초기 데이터 불러오기
  }
};
</script>