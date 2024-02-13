<template>
  <div>
    <b-button @click="showModal">신규 등록</b-button>
    <b-modal v-model="modalVisible" :title="modalTitle">
      <!-- Create.vue 컴포넌트 렌더링 -->
      <Create :isEditMode="isEditMode" :editId="editId" @closeModal="closeModal" />
    </b-modal>
    <b-table striped hover :items="items" :fields="fields">
      <template #cell(actions)="row">
        <!-- 제어 버튼 -->
        <div class="btn-group" role="group">
          <b-button size="sm" @click="toggleDetails(row.item)">
            {{ row.detailsShowing ? '숨김' : '펼침' }}
          </b-button>
          <b-button size="sm"  variant="warning" @click="editItem(row.item)">수정</b-button>
          <b-button size="sm" variant="danger" @click="deleteItem(row.item)">삭제</b-button>
        </div>
      </template>

      <!-- 커스텀 컬럼 정의 -->
      <template #cell(contents_detail)="data">
        <div>
          <span v-if="!data.detailsShowing">{{ truncateText(data.item.contents_detail, 50) }}</span>
          <span v-else>{{ data.item.contents_detail }}</span>
        </div>
      </template>

      <!-- 확장된 세부 정보 -->
      <template #row-details="row">
        <b-card v-if="row.detailsShowing">
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
      infoModal: { id: 'info-modal', title: '', content: '' }
    };
  },
  created() {
    this.fetchData();
  },
  computed: {
    modalTitle() {
      return this.isEditMode ? '수정' : '신규 등록';
    }
  },
  methods: {
    async fetchData() {
      try {
        const apiUrl = 'http://192.168.0.149:8000/fourchar/';
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
      }
    },
    showModal() {
      this.modalVisible = true;
    },
    closeModal() {
      this.modalVisible = false;
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
    }
  }
};
</script>

