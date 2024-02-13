<template>
  <div>
    <search />
    <div>
      <div class="black-bg" v-if="modal_open == true">
        <div class="white-bg">
          <h4>등록및수정</h4>
          <p>Create.vue 내용</p>
          <button @click="modal_open = false">닫기</button>
        </div>
      </div>
      <b-table striped hover :items="pageItems" :fields="fields">
        <template #cell(actions)="row">
          <!-- 제어 버튼 -->
          <div class="btn-group" role="group">
            <b-button size="sm" variant="primary" @click="openItem(row.item)">펼침</b-button>
            <b-button size="sm" variant="primary" @click="editItem(row.item)">수정</b-button>
            <b-button size="sm" variant="danger" @click="deleteItem(row.item)">삭제</b-button>
          </div>
        </template>
      </b-table>
      <!-- 페이징 -->
      <b-pagination
        v-model="currentPage"
        :total-rows="totalRows"
        :per-page="perPage"
        align="right"
        @change="handlePageChange"
      ></b-pagination>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Search from './Search.vue';

export default {
  components: { 
    Search,
  },
  data() {
    return {
      fields: [
        {
          key: 'id',
          label: 'No'
        },
        {
          key: 'category',
          label: '카테고리'
        },
        {
          key: 'contents_kr',
          label: '사자성어(한글)'
        },
        {
          key: 'contents_zh',
          label: '사자성어(한문)'
        },
        {
          key: 'contents_detail',
          label: '뜻풀이'
        },
        {
          key: 'actions',
          label: '제어',
          class: 'text-center',
          thClass: 'text-center',
          sortable: false,
          formatter: this.formatActions,
        },
      ],
      items: [],
      modal_open: false,
      currentPage: 1, // 현재 페이지 번호를 나타내는 속성
      perPage: 15, // 한 페이지당 표시할 항목 수
    };
  },
  created() {
    const apiUrl = 'https://quotes.api.thegam.io/fourchar/';

    axios.get(apiUrl)
      .then(response => {
        this.items = response.data.content;
      })
      .catch(error => {
        console.error('데이터를 불러오는 중 오류 발생:', error);
      });
  },
  computed: {
    totalRows() {
      return this.items.length;
    },
    pageItems() {
      const start = (this.currentPage - 1) * this.perPage;
      const end = start + this.perPage;
      return this.items.slice(start, end);
    }
  },
  methods: {
    formatActions(value, key, item) {
      return `
        <div class="btn-group" role="group">
          <b-button size="sm" variant="primary" @click="openItem(item)">펼침</b-button>
          <b-button size="sm" variant="primary" @click="editItem(item)">수정</b-button>
          <b-button size="sm" variant="danger" @click="deleteItem(item)">삭제</b-button>
        </div>
      `;
    },
    openItem(item) {
      // 펼침 버튼을 누를 때 수행할 동작 정의
    },
    editItem(item) {
      this.modal_open = true;
    },
    deleteItem(item) {
      // 삭제 버튼을 누를 때 수행할 동작 정의
    },
    handlePageChange(page) {
      this.currentPage = page;
    }
  }
}
</script>

<style>
body {
  margin: 0
}
div {
  box-sizing: border-box;
}
.black-bg {
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  position: fixed;
  padding: 20px;
}
.white-bg {
  width: 100%;
  background: white;
  border-radius: 8px;
  padding: 20px;
}
</style>
